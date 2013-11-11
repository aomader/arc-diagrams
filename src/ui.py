# -*- coding: utf-8 -*-

from random import seed, randint

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SubstringView(QGraphicsItem):
    LETTER_PEN = QPen(QColor('#000000'), 1, Qt.SolidLine)
    FONT = QFont('DejaVu Sans Mono', 12)
    CHAR_WIDTH = None
    CHAR_HEIGHT = None

    def __init__(self, substring, starts):
        super(QGraphicsItem, self).__init__()
        self.substring = substring
        self.starts = sorted(starts)
        self.highlighted = False
        self.brush = QColor(randint(0, 255), randint(0, 255), randint(0, 255))

        self.maxRadius = 0 if len(starts) == 1 else \
                         (max(r-l for l,r in zip(self.starts, self.starts[1:]))
                          + len(self.substring)) * SubstringView.CHAR_WIDTH/2.

        # generate text rects
        self.rects = [QRectF((s - self.starts[0]) * SubstringView.CHAR_WIDTH,
                             self.maxRadius, len(self.substring) *
                             SubstringView.CHAR_WIDTH,
                             SubstringView.CHAR_HEIGHT) for s in starts]

        # generate arc paths
        self.arcs = []
        for left, right in zip(self.rects, self.rects[1:]):
            diameter1 = right.x() + right.width() - left.x()
            diameter2 = right.x() - left.x() - left.width()
            path = QPainterPath(QPointF(left.x(), self.maxRadius))
            path.arcTo(QRectF(left.x(), self.maxRadius - diameter1/2.,
                              diameter1, diameter1), -180, -180)
            path.lineTo(right.x(), self.maxRadius)
            path.arcTo(QRectF(left.x() + left.width(), self.maxRadius -
                              diameter2/2., diameter2, diameter2), 0, 180)
            self.arcs.append(path)

        self.setAcceptHoverEvents(True)
        self.setPos(self.starts[0] * SubstringView.CHAR_WIDTH, -self.maxRadius)

    def boundingRect(self):
        return QRectF(0, 0, self.rects[-1].right() - self.rects[0].left(),
                      self.maxRadius + SubstringView.CHAR_HEIGHT)

    def paint(self, painter, objects, widget):
        # DEBUG: draw text background
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        for rect in self.rects:
            painter.drawRect(rect)

        # draw text
        painter.setPen(SubstringView.LETTER_PEN)
        painter.setFont(SubstringView.FONT)
        for rect in self.rects:
            painter.drawText(rect, Qt.AlignCenter | Qt.AlignTop,
                             self.substring)

        # draw arcs
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 150 if self.highlighted else 50))
        for arc in self.arcs:
            painter.drawPath(arc)

    def hoverEnterEvent(self, event):
        self.testHighlight(event)

    def hoverMoveEvent(self, event):
        self.testHighlight(event)

    def hoverLeaveEvent(self, event):
        self.highlighted = False
        self.update()

    def testHighlight(self, event):
        p = self.mapFromScene(event.scenePos())
        highlight = any(r.contains(p) for r in self.rects) or \
                    any(a.contains(p) for a in self.arcs)
        if highlight != self.highlighted:
            self.highlighted = highlight
            self.update()



class Window(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.setWindowTitle('ArcDiagrams')
        self.resize(800, 600)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QColor('#00FF00')))
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.Antialiasing)
        view.setRenderHint(QPainter.TextAntialiasing)
        view.setRenderHint(QPainter.HighQualityAntialiasing)

        view.resetMatrix()
        view.scale(2, 2)

        SubstringView.FONT_METRICS = QFontMetrics(SubstringView.FONT, view)
        SubstringView.CHAR_WIDTH = SubstringView.FONT_METRICS.width('A')
        SubstringView.CHAR_HEIGHT = SubstringView.FONT_METRICS.height()

        s1 = SubstringView('1234567', [0, 12, 24])
        s2 = SubstringView('abcde', [7])
        s3 = SubstringView('fghij', [19])

        self.scene.addItem(s1)
        self.scene.addItem(s2)
        self.scene.addItem(s3)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(view)

        self.setLayout(layout)
        self.show()

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
