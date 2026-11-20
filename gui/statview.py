import os

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from adapters.adapter_json import AdapterJSON

POLL_INTERVAL_MS = 1000

class StatView(QWidget):
    DatabasePath: str

    def __init__(self, databasePath: str):
        super().__init__()
        self.DatabasePath = os.path.abspath(databasePath)
        self.setWindowTitle("GuildStats - StatView")
        self.resize(1280, 720)

        # placeholder content: the event name in the middle
        self._eventName = QLabel()
        self._eventName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._eventName.setWordWrap(True)
        font = self._eventName.font()
        font.setPointSize(48)
        font.setBold(True)
        self._eventName.setFont(font)
        layout = QVBoxLayout(self)
        layout.addWidget(self._eventName)

        # poll the database file: change notifications don't reach WSL for files on /mnt/c
        self._fileSignature = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._checkFile)
        self._timer.start(POLL_INTERVAL_MS)
        self._checkFile()

    def _checkFile(self) -> None:
        # reload when the file changes, retrying until it can be read
        try:
            stat = os.stat(self.DatabasePath)
        except OSError:
            return
        signature = (stat.st_mtime_ns, stat.st_size)
        if signature == self._fileSignature:
            return
        try:
            self._refresh(AdapterJSON(self.DatabasePath))
        except (OSError, ValueError, KeyError):
            # missing, half-written or malformed file: keep the last good content
            return
        self._fileSignature = signature

    def _refresh(self, adapter: AdapterJSON) -> None:
        self._eventName.setText(adapter.EventInfo().Name or "GuildStats")
