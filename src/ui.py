# -*- coding: utf-8 -*-

from random import seed, randint

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class LettersView(QGraphicsItem):
    LETTER_PEN = QPen()
    LETTER_BRUSH = QColor(randint(0, 255), randint(0, 255),
            randint(0, 255))
    FONT = QFont('DejaVu Sans Mono', 12)
    FONT_METRICS = QFontMetrics(QFont('DejaVu Sans Mono', 12))

    def __init__(self, letters):
        super().__init__()
        seed()
        self.LETTER_BRUSH = QColor(randint(0, 255), randint(0, 255),
                randint(0, 255))
        self.letters = letters

    def boundingRect(self):
        return QRectF(0, 0, self.FONT_METRICS.width(self.letters),
                      self.FONT_METRICS.height() + 50)
    
    def paint(self, painter, objects, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.LETTER_BRUSH)
        painter.drawRect(self.boundingRect())


        painter.setFont(self.FONT)
        painter.setPen(self.LETTER_PEN)
        painter.drawText(0, 0, self.boundingRect().width(),
                self.FONT_METRICS.height(),
                         Qt.AlignCenter | Qt.AlignTop,
                         self.letters)

        painter.setPen(QPen(QColor(0, 0, 0, 50), 5, Qt.SolidLine))
        painter.drawArc(0, self.boundingRect().height(),
                self.boundingRect().width(), 50, 0 * 16, 180*
          16)


class Window(QWidget):
    def __init__(self):
        super().__init__()

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
        view.scale(5, 5)

        LettersView.FONT_METRICS = QFontMetrics(LettersView.FONT, view)

        x = 0
        for s in ['das', 'ist', 'ein', 'test']:
            l = LettersView(s)
            l.setPos(x, 0)
            x += l.boundingRect().width()
            self.scene.addItem(l)



        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(view)

        self.setLayout(layout)
        self.show()

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
