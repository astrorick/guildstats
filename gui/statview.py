import os
import traceback

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QVBoxLayout, QWidget

from adapters.adapter_json import AdapterJSON
from gui.dashboard import drawDashboard

POLL_INTERVAL_MS = 1000
RESIZE_DELAY_MS = 150

class StatView(QWidget):
    DatabasePath: str

    def __init__(self, databasePath: str):
        super().__init__()
        self.DatabasePath = os.path.abspath(databasePath)
        self.setWindowTitle("GuildStats - StatView")
        self.resize(1280, 720)

        # the dashboard is one matplotlib figure filling the window
        self._canvas = FigureCanvasQTAgg(Figure(layout = "constrained"))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._canvas)

        # redraw once resizing settles, so everything keeps its size relative to the window
        self._resizeTimer = QTimer(self)
        self._resizeTimer.setSingleShot(True)
        self._resizeTimer.setInterval(RESIZE_DELAY_MS)
        self._resizeTimer.timeout.connect(self._redraw)
        self._canvas.mpl_connect("resize_event", self._onResize)

        # F11 toggles full screen on the big screen
        self._fullScreenShortcut = QShortcut(QKeySequence("F11"), self)
        self._fullScreenShortcut.activated.connect(self._toggleFullScreen)

        # poll the database file: change notifications don't reach WSL for files on /mnt/c
        self._data = None
        self._fileSignature = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._checkFile)
        self._timer.start(POLL_INTERVAL_MS)
        self._checkFile()

    def _onResize(self, event) -> None:
        # until the dashboard is rebuilt for the new size, keep the old picture without redoing its layout
        self._canvas.figure.set_layout_engine("none")
        self._resizeTimer.start()

    def _toggleFullScreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _checkFile(self) -> None:
        # reload when the file changes
        try:
            stat = os.stat(self.DatabasePath)
        except OSError:
            return
        signature = (stat.st_mtime_ns, stat.st_size)
        if signature == self._fileSignature:
            return
        self._fileSignature = signature
        try:
            adapter = AdapterJSON(self.DatabasePath)
            data = (adapter.EventInfo(), adapter.TablesList(), adapter.PlayersList())
        except Exception as error:
            # missing, half-written or malformed file: keep the last good picture
            print(f"StatView: could not read the database ({error!r})")
            return
        self._show(data)

    def _redraw(self) -> None:
        if self._data is not None:
            self._show(self._data)

    def _show(self, data: tuple) -> None:
        try:
            drawDashboard(self._canvas.figure, *data)
            self._data = data
        except Exception:
            # a drawing error puts the last good picture back
            traceback.print_exc()
            if self._data is not None and self._data is not data:
                drawDashboard(self._canvas.figure, *self._data)
        self._canvas.draw_idle()
