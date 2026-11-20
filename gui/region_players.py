from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QGroupBox, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QVBoxLayout

from adapters.adapter_json import AdapterJSON
from model.deck import DECK_COLORS, Deck
from model.player import Player

NEW_PLAYER_LABEL = "+ New player"

class RegionPlayers(QGroupBox):
    Changed = Signal()

    def __init__(self, adapter: AdapterJSON):
        super().__init__("Players")
        self._adapter = adapter
        self._players: list[Player] = []

        # input fields
        self._selector = QComboBox()
        self._name = QLineEdit()
        self._deckName = QLineEdit()
        self._commander = QLineEdit()
        self._colors = {color: QCheckBox(color) for color in DECK_COLORS}
        self._button = QPushButton()

        # signals
        self._selector.currentIndexChanged.connect(self._onSelected)
        self._name.textChanged.connect(self._updateButton)
        self._button.clicked.connect(self._onCommit)

        # layout
        colorsRow = QHBoxLayout()
        for checkBox in self._colors.values():
            colorsRow.addWidget(checkBox)
        colorsRow.addStretch()
        form = QFormLayout()
        form.addRow("Player", self._selector)
        form.addRow("Name", self._name)
        form.addRow("Deck", self._deckName)
        form.addRow("Commander", self._commander)
        form.addRow("Colors", colorsRow)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch()
        layout.addWidget(self._button)

        self.Refresh()

    def Refresh(self) -> None:
        # refill the selector and go back to a new empty entry
        self._players = self._adapter.PlayersList()
        self._selector.blockSignals(True)
        self._selector.clear()
        self._selector.addItem(NEW_PLAYER_LABEL)
        self._selector.addItems([player.Name for player in self._players])
        self._selector.blockSignals(False)
        self._onSelected(0)

    def _onSelected(self, index: int) -> None:
        # entry 0 is a new player, the others are the existing players
        if index > 0:
            player = self._players[index - 1]
            self._name.setText(player.Name)
            self._deckName.setText(player.Deck.Name)
            self._commander.setText(player.Deck.Commander)
            for color, checkBox in self._colors.items():
                checkBox.setChecked(color in player.Deck.Colors)
        else:
            self._name.clear()
            self._deckName.clear()
            self._commander.clear()
            for checkBox in self._colors.values():
                checkBox.setChecked(False)
        self._updateButton()

    def _updateButton(self) -> None:
        self._button.setText("Save" if self._selector.currentIndex() > 0 else "Add")
        self._button.setEnabled(len(self._name.text().strip()) > 0)

    def _onCommit(self) -> None:
        # index is -1 for a new player
        index = self._selector.currentIndex() - 1
        name = self._name.text().strip()
        if any(player.Name == name for i, player in enumerate(self._players) if i != index):
            QMessageBox.warning(self, "Players", f"A player named \"{name}\" already exists.")
            return

        deck = Deck(
            Name = self._deckName.text().strip(),
            Commander = self._commander.text().strip(),
            Colors = [color for color, checkBox in self._colors.items() if checkBox.isChecked()],
        )
        if index < 0:
            self._adapter.AddPlayer(name, deck)
        else:
            self._adapter.UpdatePlayer(index, name, deck)

        self.Refresh()
        self.Changed.emit()
