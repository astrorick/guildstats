from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout, QWidget

from adapters.adapter_json import AdapterJSON
from gui.region_tables import tableLabel
from model.game import GENERIC_SQ_NAMES, THEMATIC_SQ_NAMES, Game
from model.table import Table

THEMATIC_SQ_COLUMNS = 5
ROW_SPACING = 16

class RegionGames(QGroupBox):
    def __init__(self, adapter: AdapterJSON):
        super().__init__("Games")
        self._adapter = adapter
        self._tables: list[Table] = []

        # input fields
        self._player = QComboBox()
        self._player.setPlaceholderText("Select player")
        self._player.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self._skipped = QCheckBox("Skipped")
        self._table = QComboBox()
        self._table.setPlaceholderText("Select table")
        self._table.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self._won = QCheckBox("Won")
        self._altWin = QCheckBox("Alt Win")
        self._draw = QCheckBox("Draw")
        self._scooped = QCheckBox("Scooped")
        self._kills = QSpinBox()
        self._gnrSq = {name: QCheckBox(name) for name in GENERIC_SQ_NAMES}
        self._thmSq = {name: QCheckBox(name) for name in THEMATIC_SQ_NAMES}
        self._basePoints = QSpinBox()
        self._questPoints = QSpinBox()
        self._farmingPoints = QSpinBox()
        self._stylePoint = QLineEdit()
        self._saveButton = QPushButton("Save")

        # signals
        self._player.currentIndexChanged.connect(self._updateSaveButton)
        self._skipped.toggled.connect(self._onSkippedToggled)
        self._table.currentIndexChanged.connect(self._updateSaveButton)
        self._saveButton.clicked.connect(self._onSave)

        # layout: everything after the skipped flag is a game detail
        tablePair = _pair("Table", self._table)
        thmSqGrid = QWidget()
        thmSqLayout = QGridLayout(thmSqGrid)
        thmSqLayout.setContentsMargins(0, 0, 0, 0)
        thmSqLayout.setHorizontalSpacing(ROW_SPACING)
        for i, checkBox in enumerate(self._thmSq.values()):
            thmSqLayout.addWidget(checkBox, i // THEMATIC_SQ_COLUMNS, i % THEMATIC_SQ_COLUMNS)
        thmSqLayout.setColumnStretch(THEMATIC_SQ_COLUMNS, 1)
        detailRows = {
            "Result": _row(self._won, self._altWin, self._draw, self._scooped, _pair("Kills", self._kills)),
            "Generic": _row(*self._gnrSq.values()),
            "Thematic": thmSqGrid,
            "Points": _row(_pair("Base", self._basePoints), _pair("Quest", self._questPoints), _pair("Farming", self._farmingPoints)),
            "Style": self._stylePoint,
        }

        form = QFormLayout()
        form.addRow("Player", _row(self._player, self._skipped, tablePair))
        self._details: list[QWidget] = [tablePair]
        for label, field in detailRows.items():
            labelWidget = QLabel(label)
            form.addRow(labelWidget, field)
            self._details += [labelWidget, field]
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self._saveButton)

        self.Refresh()

    def Refresh(self) -> None:
        # refill the dropdowns and empty the form
        self.RefreshDropdowns()
        self._reset()

    def RefreshDropdowns(self) -> None:
        # keep the current selections: players and tables are only added or edited while the app runs
        self._tables = self._adapter.TablesList()
        _refill(self._player, [player.Name for player in self._adapter.PlayersList()])
        _refill(self._table, [tableLabel(table) for table in self._tables])
        self._updateSaveButton()

    def _reset(self) -> None:
        self._player.setCurrentIndex(-1)
        self._skipped.setChecked(False)
        self._clearDetails()

    def _clearDetails(self) -> None:
        self._table.setCurrentIndex(-1)
        for checkBox in [self._won, self._altWin, self._draw, self._scooped, *self._gnrSq.values(), *self._thmSq.values()]:
            checkBox.setChecked(False)
        for spinBox in [self._kills, self._basePoints, self._questPoints, self._farmingPoints]:
            spinBox.setValue(0)
        self._stylePoint.clear()

    def _onSkippedToggled(self, skipped: bool) -> None:
        # a skipped game has no details
        if skipped:
            self._clearDetails()
        for widget in self._details:
            widget.setEnabled(not skipped)
        self._updateSaveButton()

    def _updateSaveButton(self) -> None:
        # a player is always required, a table only for played games
        playerSelected = self._player.currentIndex() >= 0
        tableSelected = self._table.currentIndex() >= 0
        self._saveButton.setEnabled(playerSelected and (tableSelected or self._skipped.isChecked()))

    def _onSave(self) -> None:
        tableIndex = self._table.currentIndex()
        self._adapter.AddGame(
            self._player.currentIndex(),
            Game(
                Skipped = self._skipped.isChecked(),
                Table = self._tables[tableIndex].Name if tableIndex >= 0 else "",
                Won = self._won.isChecked(),
                AltWin = self._altWin.isChecked(),
                Draw = self._draw.isChecked(),
                Scooped = self._scooped.isChecked(),
                Kills = self._kills.value(),
                GnrSq = [name for name, checkBox in self._gnrSq.items() if checkBox.isChecked()],
                ThmSq = [name for name, checkBox in self._thmSq.items() if checkBox.isChecked()],
                BasePoints = self._basePoints.value(),
                QuestPoints = self._questPoints.value(),
                FarmingPoints = self._farmingPoints.value(),
                StylePoint = self._stylePoint.text().strip(),
            ),
        )
        self._reset()

def _row(*widgets: QWidget) -> QWidget:
    # widgets side by side in one container, so the row can be disabled at once
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(ROW_SPACING)
    for widget in widgets:
        layout.addWidget(widget)
    layout.addStretch()
    return row

def _pair(label: str, widget: QWidget) -> QWidget:
    # a label right before its widget
    pair = QWidget()
    layout = QHBoxLayout(pair)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(QLabel(label))
    layout.addWidget(widget)
    return pair

def _refill(comboBox: QComboBox, items: list[str]) -> None:
    # replace the entries, keeping the selected index if it still exists
    index = comboBox.currentIndex()
    comboBox.blockSignals(True)
    comboBox.clear()
    comboBox.addItems(items)
    comboBox.setCurrentIndex(index if index < len(items) else -1)
    comboBox.blockSignals(False)
