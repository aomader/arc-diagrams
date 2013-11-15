# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .naive_algorithm import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.setWindowTitle('ArcDiagrams')
        self.resize(800, 600)
        self.setStyleSheet('''
            #top { background: #fff; }
            QLineEdit { border: 2px solid #eee;
                        border-radius: 0;
                        height: 26px;
                        font-size: 12pt;
                        color: #666;
                        padding: 0px 5px;
                        background: #f7f7f7; }
            QGraphicsView { border: 0; }
            QPushButton { border: 0; background: #aaa; color: #fff;
            font-size:20pt; height: 30px; width:30px;}''')

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setMargin(0)

        view = SceneView()

        text = QLineEdit()
        text.textChanged.connect(lambda: view.setText(text.text()))

        initial = '11111000110111001001011110001101110001010'
        view.setText(initial)
        text.setText(initial)

        h = QHBoxLayout()
        h.setMargin(18)
        h.setSpacing(18)
        h.addWidget(text)

        zoomOut = QPushButton('-')
        h.addWidget(zoomOut)

        zoomIn = QPushButton('+')
        h.addWidget(zoomIn)

        top = QWidget()
        top.setLayout(h)
        top.setObjectName('top')

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 50))
        top.setGraphicsEffect(shadow)

        layout.addWidget(top)
        layout.addWidget(view)
        view.stackUnder(top)


class SceneView(QGraphicsView):
    CHAR_WIDTH = None
    CHAR_HEIGHT = None

    def __init__(self, *args, **kwargs):
        super(QGraphicsView, self).__init__(*args, **kwargs)
        self.setBackgroundBrush(QColor('#f7f7f7'))
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setMouseTracking(True)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        metrics = QFontMetrics(TextView.FONT, self)
        SceneView.CHAR_WIDTH = metrics.width('W')
        SceneView.CHAR_HEIGHT = metrics.height()

        self.textView = TextView()
        self.arcViews = []

        self.highlighted = set()

        self.scene.addItem(self.textView)

    def setText(self, text):
        self.textView.setText(text)

        for arc in self.arcViews:
            self.scene.removeItem(arc)
        self.arcViews = []

        for start, end, width in essential_matching_pairs(unicode(text)):
            arc = ArcView(start, end, width)
            self.scene.addItem(arc)
            self.arcViews.append(arc)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

    def mouseMoveEvent(self, event):
        new_highlighted = set(item for item in self.items(event.pos())
                     if isinstance(item, ArcView) and
                     item.path.contains(item.mapFromScene(self.mapToScene(event.pos()))))

        for i in self.highlighted - new_highlighted:
            i.setHighlighted(False)
        for i in new_highlighted - self.highlighted:
            i.setHighlighted(True)

        self.highlighted = new_highlighted

        return super(QGraphicsView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.delta() > 0:
            self.scale(1.15, 1.15)
        else:
            self.scale(1.0/1.15, 1.0/1.15)


class TextView(QGraphicsItem):
    FONT = QFont('DejaVu Sans Mono', 12)
    PEN = QPen(QColor('#333333'), 1, Qt.SolidLine)

    def __init__(self, *args, **kwargs):
        super(QGraphicsItem, self).__init__(*args, **kwargs)
        self.text = ''

    def setText(self, text):
        self.text = text
        self.prepareGeometryChange()
        self.update()

    def boundingRect(self):
        return QRectF(0, 0, len(self.text) * SceneView.CHAR_WIDTH,
                      SceneView.CHAR_HEIGHT + 5)

    def paint(self, painter, objects, widget):
        inset = SceneView.CHAR_WIDTH / 8.
        painter.setPen(TextView.PEN)
        painter.setFont(TextView.FONT)
        for i,c in enumerate(self.text):
            rect = QRectF(i * SceneView.CHAR_WIDTH, 5., SceneView.CHAR_WIDTH,
                          SceneView.CHAR_HEIGHT)
            painter.drawText(rect, Qt.AlignCenter | Qt.AlignTop, c)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 25))
        for i in range(0, len(self.text)):
            painter.drawRect(QRectF(i * SceneView.CHAR_WIDTH + inset, 3,
                                    SceneView.CHAR_WIDTH - 2*inset, 1))


class ArcView(QGraphicsItem):
    BRUSH = QColor(0, 67, 136, 23)
    BRUSH_HIGHLIGHTED = QColor(255, 0, 0, 150)

    def __init__(self, start, end, width, *args, **kwargs):
        super(QGraphicsItem, self).__init__(*args, **kwargs)
        inset = SceneView.CHAR_WIDTH / 8.
        outer = (end - start + width) * SceneView.CHAR_WIDTH
        inner = (end - start - width) * SceneView.CHAR_WIDTH

        self.rect = QRectF(0, 0, (end - start + width) * SceneView.CHAR_WIDTH,
                           (end - start + width) * SceneView.CHAR_WIDTH / 2.)

        width = width * SceneView.CHAR_WIDTH
        self.path = QPainterPath(QPointF(inset, self.rect.bottom()))
        self.path.arcTo(inset, inset, outer - 2*inset, outer - 2*inset, -180, -180)
        self.path.lineTo(inner + width + inset, self.rect.bottom())
        self.path.arcTo(width - inset, width - inset, inner + 2*inset, inner +
                        2*inset, 0, 180)

        self.highlighted = False
        self.setPos(start * SceneView.CHAR_WIDTH, -outer / 2.)

    def setHighlighted(self, highlighted):
        self.highlighted = highlighted
        self.update()

    def boundingRect(self):
        return self.rect

    def paint(self, painter, objects, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(ArcView.BRUSH_HIGHLIGHTED if self.highlighted else
                ArcView.BRUSH)
        painter.drawPath(self.path)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
