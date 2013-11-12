# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from algorithm import *

class TextView(QGraphicsObject):
    FONT = QFont('DejaVu Sans Mono', 12)
    PEN = QPen(QColor('#333333'), 1, Qt.SolidLine)

    def __init__(self, text=''):
        super(QGraphicsObject, self).__init__()
        self.text = text

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



class ArcView(QGraphicsObject):
    BRUSH = QColor(0, 67, 136, 23)

    def __init__(self, start, end, width):
        super(QGraphicsObject, self).__init__()
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

        self.setPos(start * SceneView.CHAR_WIDTH, -outer / 2.)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, objects, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(ArcView.BRUSH)
        painter.drawPath(self.path)


class SceneView(QGraphicsView):
    CHAR_WIDTH = None
    CHAR_HEIGHT = None

    def __init__(self):
        super(QGraphicsView, self).__init__()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.setBackgroundBrush(QColor('#f7f7f7'))

        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        metrics = QFontMetrics(TextView.FONT, self)
        SceneView.CHAR_WIDTH = metrics.width('W')
        SceneView.CHAR_HEIGHT = metrics.height()

        self.textView = TextView()
        self.arcViews = []

        self.scene.addItem(self.textView)

    def setText(self, text):
        self.textView.setText(text)

        for arc in self.arcViews:
            self.scene.removeItem(arc)
        self.arcViews = []

        for start, end, width in arc_pairs(text):
            arc = ArcView(start, end, width)
            self.scene.addItem(arc)
            self.arcViews.append(arc)


    def wheelEvent(self, event):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.delta() > 0:
            self.scale(1.15, 1.15)
        else:
            self.scale(1.0/1.15, 1.0/1.15)


class Window(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.setWindowTitle('ArcDiagrams')
        self.resize(800, 600)

        view = SceneView()

        text = QLineEdit()
        text.textChanged.connect(lambda: view.setText(text.text()))

        initial = '11111000110111001001011110001101110001010'
        view.setText(initial)
        text.setText(initial)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(view)
        layout.addWidget(text)

        self.setLayout(layout)
        self.show()


# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
