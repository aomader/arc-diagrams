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
        super().__init__()
        self.substring = substring
        self.starts = starts
        self.brush = QColor(randint(0, 255), randint(0, 255), randint(0, 255))

        self.setPos(self.starts[0] * SubstringView.CHAR_WIDTH, 0)

    def boundingRect(self):
        return QRectF(0, 0, (self.starts[-1] + len(self.substring) - self.starts[0]) * 
                      SubstringView.CHAR_WIDTH, SubstringView.CHAR_HEIGHT)

    def paint(self, painter, objects, widget):
        # draw text
        painter.setPen(SubstringView.LETTER_PEN)
        painter.setFont(SubstringView.FONT)
        for start in self.starts:
            region = QRect((start - self.starts[0]) * SubstringView.CHAR_WIDTH, 0,
                           len(self.substring) * SubstringView.CHAR_WIDTH,
                           SubstringView.CHAR_HEIGHT)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.brush)
            painter.drawRect(region)
            painter.setPen(SubstringView.LETTER_PEN)
            painter.drawText(region, Qt.AlignCenter | Qt.AlignTop,
                             self.substring)

        # draw arcs
        painter.setPen(QPen(QColor(0, 0, 0, 50), len(self.substring) * SubstringView.CHAR_WIDTH, Qt.SolidLine))
        for left, right in zip(self.starts, self.starts[1:]):
            width = (right - left) * SubstringView.CHAR_WIDTH
            region = QRect((left - self.starts[0] + len(self.substring)/2.) * SubstringView.CHAR_WIDTH, -width/2., width, width)
            painter.drawArc(region, 0 * 16, 180 * 16)


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

        SubstringView.FONT_METRICS = QFontMetrics(SubstringView.FONT, view)
        SubstringView.CHAR_WIDTH = SubstringView.FONT_METRICS.width('A')
        SubstringView.CHAR_HEIGHT = SubstringView.FONT_METRICS.height()

        LettersView.FONT_METRICS = QFontMetrics(LettersView.FONT, view)

        s = SubstringView('test', [1, 7, 13])
        self.scene.addItem(s)

        #x = 0
        #for s in ['das', 'ist', 'ein', 'test']:
        #    l = LettersView(s)
        #    l.setPos(x, 0)
        #    x += l.boundingRect().width()
        #    self.scene.addItem(l)



        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(view)

        self.setLayout(layout)
        self.show()

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
