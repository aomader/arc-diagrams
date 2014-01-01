# -*- coding: utf-8 -*-

from binascii import hexlify
from math import sqrt
from multiprocessing import Process, Queue
from pkg_resources import resource_filename

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .naive_algorithm import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setWindowTitle('ArcDiagrams')
        self.resize(800, 600)

        # the central ui component
        self.view = view = SceneView()
        view.setStyleSheet('border: 0;')

        # top bar
        text = QLineEdit()
        self.text = text
        text.setStyleSheet('''border: 2px solid #eee; border-radius: 0;
            height: 26px; font-size: 12pt; color: #666; padding: 0px 5px;
            background: #f7f7f7;''')
        text.textChanged.connect(lambda: view.setText(text.text()))
        openFile = QPushButton()
        openFile.setStyleSheet('background: #ffffff; border: 0; outline: 0;')
        openFile.setIcon(QIcon(resource_filename(__name__,
            'pixmaps/open.png')))
        openFile.setIconSize(QSize(30, 30))
        openFile.clicked.connect(self.openFile)
        topLayout = QHBoxLayout(); topLayout.setMargin(18); topLayout.setSpacing(18)
        topLayout.addWidget(text)
        topLayout.addWidget(openFile)
        top = QWidget(); top.setLayout(topLayout)
        top.setStyleSheet('background: #fff')
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 50))
        top.setGraphicsEffect(shadow)

        # main layout containing input and graphics view
        layout = QVBoxLayout(self); layout.setSpacing(0); layout.setMargin(0)
        layout.addWidget(top)
        layout.addWidget(view)
        view.stackUnder(top)

        # info label
        infoLabel = QLabel()
        infoLabel.setStyleSheet('''color: #544721; background: #fff6bf;
            border-radius: 8px; border: 2px solid #ffd324; padding: 4px 6px;
            font-size: 10pt;''')
        view.infoText.connect(infoLabel.setText)
        view.infoText.connect(lambda x: infoLabel.show() if x != '' else
                                        infoLabel.hide())

        # detail buttons
        detailsOut = QPushButton('-')
        detailsOut.setStyleSheet('''border-top-left-radius:10px;
                border-bottom-left-radius:10px; border-right:0;''')
        detailsOut.clicked.connect(lambda: view.setDetails(1))
        detailsIn = QPushButton('+')
        detailsIn.setStyleSheet('''border-top-right-radius:10px;
                border-bottom-right-radius:10px; border-left:0;''')
        detailsIn.clicked.connect(lambda: view.setDetails(-1))
        details = QPushButton()
        details.setStyleSheet('border-left:0; border-right:0;')
        details.setIcon(QIcon(resource_filename(__name__, 'pixmaps/details.png')))
        details.setIconSize(QSize(30, 30))
        details.clicked.connect(lambda: view.setDetails(None))
        view.canIncreaseDetails.connect(detailsIn.setEnabled)
        view.canDecreaseDetails.connect(detailsOut.setEnabled)

        # zoom buttons
        zoomOut = QPushButton('-')
        zoomOut.setStyleSheet(detailsOut.styleSheet())
        zoomOut.clicked.connect(lambda: view.setZoom(-1))
        zoomIn = QPushButton('+')
        zoomIn.setStyleSheet(detailsIn.styleSheet())
        zoomIn.clicked.connect(lambda: view.setZoom(+1))
        zoom = QPushButton()
        zoom.setStyleSheet(details.styleSheet())
        zoom.setIcon(QIcon(resource_filename(__name__, 'pixmaps/zoom.png')))
        zoom.setIconSize(QSize(30, 30))
        zoom.clicked.connect(lambda: view.setZoom(None))

        # layout containing info text, zoom and detail buttons
        bottomLayout = QHBoxLayout(); bottomLayout.setMargin(18)
        bottomLayout.setSpacing(0)
        bottomLayout.addWidget(infoLabel)
        bottomLayout.addStretch()
        bottomLayout.addWidget(detailsOut)
        bottomLayout.addWidget(details)
        bottomLayout.addWidget(detailsIn)
        bottomLayout.addSpacing(25)
        bottomLayout.addWidget(zoomOut)
        bottomLayout.addWidget(zoom)
        bottomLayout.addWidget(zoomIn)
        self.bottom = QWidget(self); self.bottom.setLayout(bottomLayout)
        self.bottom.setStyleSheet('''
            QPushButton { border: 1px solid #ccc; background: #fff;
                color: #666; outline: none; font-size: 16pt; height: 30px;
                width:30px; }
            QPushButton:disabled { color: #ccc; }''')

        # loading indicator
        movie = QMovie(resource_filename(__name__, 'pixmaps/loading.gif'),
                       QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(150)
        movie.start()
        self.loading = loading = QLabel(self)
        loading.setStyleSheet('''background: transparent; border: 0;
            padding: 0; margin: 0;''')
        loading.setMovie(movie)
        loading.resize(32, 32)
        loading.hide()

        view.findingArcs.connect(self.findingArcs)
        self.working = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.working and (self.view.clean()
            or self.loading.show()))
        self.timer.setInterval(1000)
        self.timer.setSingleShot(True)

        text.setText('11111000110111001001011110001101110001010')

    def setInfo(self, info):
        if info is None:
            self.infoLabel.hide()
        else:
            self.infoLabel.setText(info)
            self.infoLabel.show()

    def findingArcs(self, working):
        self.working = working
        self.timer.stop()
        self.timer.start() if working else self.loading.hide()

    def openFile(self):
        dialog = QFileDialog(self)
        dialog.open()
        dialog.fileSelected.connect(self.readFile)
    
    def readFile(self, path):
        with open(path, 'rb') as f:
            content = f.read()
        self.text.setText(hexlify(content))

    def resizeEvent(self, event):
        super(Window, self).resizeEvent(event)
        self.bottom.setGeometry(0, self.size().height() - 66,
                self.size().width(), 66)
        self.loading.move(self.size().width()/2 - 16,
                          self.size().height()/2 - 16)

    def closeEvent(self, event):
        super(Window, self).closeEvent(event)
        self.view.stopThreads()


class Worker(QObject):
    arcsReady = pyqtSignal(dict)

    @pyqtSlot(unicode)
    def findArcs(self, text):
        text = unicode(text)

        queue = Queue()
        process = Process(target=self.solve, args=(text, queue))
        process.start()
        while process.is_alive():
            if not self.running:
                return process.terminate()
            process.join(0.001)

        infos = {}
        for x,y,l in queue.get():
            if not self.running:
                return
            sub = text[x:x+l]
            if sub not in infos:
                infos[sub] = {'arcs': [], 'xs': set()}
            arc = ArcView(x, y, l)
            arc.sub = sub
            info = infos[sub]
            info['arcs'].append(arc)
            info['xs'].update([x, y])

        self.arcsReady.emit(infos)

    def solve(self, text, queue):
        queue.put(list(essential_matching_pairs(text)))


class SceneView(QGraphicsView):
    CHAR_WIDTH = None
    CHAR_HEIGHT = None

    canIncreaseDetails = pyqtSignal(bool)
    canDecreaseDetails = pyqtSignal(bool)
    infoText = pyqtSignal(str)
    findingArcs = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(SceneView, self).__init__(*args, **kwargs)
        self.setBackgroundBrush(QColor('#f7f7f7'))
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        metrics = QFontMetrics(TextView.FONT, self)
        SceneView.CHAR_WIDTH = metrics.width('W')
        SceneView.CHAR_HEIGHT = metrics.height()

        self.textView = TextView()
        self.arcViews = {}
        self.scene.addItem(self.textView)

        self.detailLevels = []
        self.details = 0
        self.highlighted = None
        self.marked = None
        self.pressedAt = None
        self.workerThread = None

    def stopThreads(self):
        if self.workerThread is not None:
            self.worker.running = False
            self.workerThread.quit()
            self.workerThread.wait()

    def setText(self, text):
        self.text = text
        self.setEnabled(False)
        self.findingArcs.emit(True)

        if self.workerThread is not None and self.workerThread.isRunning():
            self.worker.arcsReady.disconnect(self.update)
            self.worker.running = False
            self.workerThread.quit()
            self.workerThread.wait()

        self.workerThread = QThread()
        self.worker = Worker()
        self.worker.running = True
        self.worker.moveToThread(self.workerThread)
        self.worker.arcsReady.connect(self.update)
        self.workerThread.start()

        QMetaObject.invokeMethod(self.worker, "findArcs",
            Qt.QueuedConnection, Q_ARG(unicode, unicode(text)))

    def clean(self):
        for info in self.arcViews.itervalues():
            for arc in info['arcs']:
                self.scene.removeItem(arc)
        self.textView.setText('')
        self.arcViews = {}
        self.detailLevels = []
        self.marked = None
        self.infoText.emit('')
        self.setZoom(None)
        self.setDetails(None)

    @pyqtSlot(dict)
    def update(self, arcs):
        self.clean()
        self.findingArcs.emit(False)
        self.textView.setText(self.text)

        self.marked = None
        self.infoText.emit('')
        self.arcViews = arcs
        self.detailLevels = sorted(set(len(s) for s in arcs.iterkeys()))
        for info in arcs.itervalues():
            for arc in info['arcs']:
                self.scene.addItem(arc)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.setZoom(None)
        self.setDetails(None)
        self.setEnabled(True)
    
    def setDetails(self, level):
        level = 0 if level is None else self.details + level
        self.details = min(max(level, 0), len(self.detailLevels))
        for k,v in self.arcViews.iteritems():
            for arc in v['arcs']:
                arc.setVisible(len(k) >= self.detailLevels[self.details])
        self.canIncreaseDetails.emit(self.details > 0)
        self.canDecreaseDetails.emit(self.details < len(self.detailLevels) - 1)
        if self.marked and len(self.marked) < self.detailLevels[self.details]:
            self.setMarked(None)

    def setZoom(self, level):
        if level is None:
            self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            level = 1/1.15
        else:
            level = 1.15 if level == 1 else 1/1.15
        self.scale(level, level)

    def setMarked(self, arc):
        if (not arc or arc.sub != self.marked) and self.marked in \
                                                   self.arcViews:
            for a in self.arcViews[self.marked]['arcs']:
                a.setMarked(False)
            self.infoText.emit('')
        if arc and arc.sub != self.marked:
            self.marked = arc.sub
            for a in self.arcViews[self.marked]['arcs']:
                a.setMarked(True)
            self.infoText.emit('Substring "%s" appears %i times.' %
                    (arc.sub, len(self.arcViews[arc.sub]['xs'])))
        self.marked = arc.sub if arc else None

    def mousePressEvent(self, event):
        self.pressedAt = event.pos()
        return super(SceneView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(SceneView, self).mouseMoveEvent(event)
        if not self.pressedAt:
            highlighted = self.arcFromPoint(event.pos())
            if highlighted != self.highlighted:
                self.highlighted and self.highlighted.setHighlighted(False)
                highlighted and highlighted.setHighlighted(True)
                self.highlighted = highlighted

    def mouseReleaseEvent(self, event):
        if self.distance(self.pressedAt, event.pos()) < 8:
            arc = self.arcFromPoint(self.pressedAt)
            self.setMarked(arc)
        self.pressedAt = None
        return super(SceneView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        self.setZoom(+1 if event.delta() > 0 else -1)

    def arcFromPoint(self, point):
        arc = None
        dist = self.scene.sceneRect().width()
        for item in self.items(point):
            p = item.mapFromScene(self.mapToScene(point))
            if isinstance(item, ArcView) and item.isVisible() and \
                    item.path.contains(p):
                d = self.distance(p, item.center)
                if d < dist:
                    dist = d
                    arc = item
        return arc

    def distance(self, p1, p2):
        return sqrt((p1.x() - p2.x())**2 + (p1.y() - p2.y())**2)


class TextView(QGraphicsItem):
    FONT = QFont('DejaVu Sans Mono', 12)
    PEN = QPen(QColor('#333333'), 1, Qt.SolidLine)
    BRUSH_MARKED = QColor(214, 233, 0, 150)

    def __init__(self, *args, **kwargs):
        super(TextView, self).__init__(*args, **kwargs)
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
    BRUSH_HIGHLIGHTED = QColor(200, 0, 0, 100)
    BRUSH_MARKED_HIGHLIGHTED = QColor(200, 0, 0, 150)

    def __init__(self, start, end, width, *args, **kwargs):
        super(ArcView, self).__init__(*args, **kwargs)
        inset = SceneView.CHAR_WIDTH / 8.
        outer = (end - start + width) * SceneView.CHAR_WIDTH
        inner = (end - start - width) * SceneView.CHAR_WIDTH
        width = width * SceneView.CHAR_WIDTH

        self.rect = QRectF(0, 0, outer, outer / 2.)
        self.path = QPainterPath(QPointF(inset, self.rect.bottom()))
        self.path.arcTo(inset, inset, outer - 2*inset, outer - 2*inset, -180, -180)
        self.path.lineTo(inner + width + inset, self.rect.bottom())
        self.path.arcTo(width - inset, width - inset, inner + 2*inset, inner +
                        2*inset, 0, 180)
        self.center = QPointF(outer / 2., (outer - inner) / 4.)
        self.setPos(start * SceneView.CHAR_WIDTH, -outer / 2.)

        self.highlighted = False
        self.marked = False

    def setHighlighted(self, highlighted):
        self.highlighted = highlighted
        self.setZValue(1 if highlighted or self.marked else 0)
        self.update()

    def setMarked(self, marked):
        self.marked = marked
        self.setZValue(1 if self.highlighted or marked else 0)
        self.update()

    def boundingRect(self):
        return self.rect

    def paint(self, painter, objects, widget):
        painter.setPen(Qt.NoPen)
        if self.highlighted and self.marked:
            painter.setBrush(ArcView.BRUSH_MARKED_HIGHLIGHTED)
        elif self.highlighted or self.marked:
            painter.setBrush(ArcView.BRUSH_HIGHLIGHTED)
        else:
            painter.setBrush(ArcView.BRUSH)
        painter.drawPath(self.path)

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
