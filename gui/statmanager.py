import os

from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from adapters.adapter_json import AdapterJSON
from gui.region_event import RegionEvent
from gui.region_games import RegionGames
from gui.region_players import RegionPlayers
from gui.region_tables import RegionTables

WINDOW_WIDTH = 1000

class StatManager(QWidget):
    def __init__(self, adapter: AdapterJSON):
        super().__init__()
        self._adapter = adapter
        self.setWindowTitle(f"GuildStats - StatManager ({os.path.basename(adapter.DatabasePath)})")

        # header: database name and reload button
        self._databaseName = QLabel(adapter.DatabaseInfo().Name)
        font = self._databaseName.font()
        font.setBold(True)
        self._databaseName.setFont(font)
        reloadButton = QPushButton("Reload")
        reloadButton.clicked.connect(self._onReload)
        header = QHBoxLayout()
        header.addWidget(self._databaseName)
        header.addStretch()
        header.addWidget(reloadButton)

        # regions, with the games dropdowns following tables and players
        self._regions = [RegionEvent(adapter), RegionTables(adapter), RegionPlayers(adapter), RegionGames(adapter)]
        regionEvent, regionTables, regionPlayers, regionGames = self._regions
        regionTables.Changed.connect(regionGames.RefreshDropdowns)
        regionPlayers.Changed.connect(regionGames.RefreshDropdowns)

        # layout: header, then event, tables and players side by side, then games
        topRow = QHBoxLayout()
        for region in (regionEvent, regionTables, regionPlayers):
            topRow.addWidget(region, 1)
        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addLayout(topRow)
        layout.addWidget(regionGames)
        self.resize(WINDOW_WIDTH, self.sizeHint().height())

    def _refresh(self) -> None:
        self._databaseName.setText(self._adapter.DatabaseInfo().Name)
        for region in self._regions:
            region.Refresh()

    def _onReload(self) -> None:
        # sync the adapter with the file, e.g. after editing it by hand
        previousData = self._adapter.RawData
        try:
            self._adapter.Reload()
            self._refresh()
        except Exception as error:
            # unreadable or malformed file: go back to the data we had
            self._adapter.RawData = previousData
            self._refresh()
            QMessageBox.warning(self, "Reload", f"Could not reload the database, nothing was changed.\n\n{error!r}")
