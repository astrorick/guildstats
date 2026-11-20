from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QFormLayout, QGroupBox, QLineEdit, QMessageBox, QPushButton, QSpinBox, QVBoxLayout

from adapters.adapter_json import AdapterJSON
from model.table import Table

NEW_TABLE_LABEL = "+ New table"
TABLE_SIZE_MIN = 2
TABLE_SIZE_MAX = 8
TABLE_SIZE_DEFAULT = 4

class RegionTables(QGroupBox):
    Changed = Signal()

    def __init__(self, adapter: AdapterJSON):
        super().__init__("Tables")
        self._adapter = adapter
        self._tables: list[Table] = []

        # input fields
        self._selector = QComboBox()
        self._name = QLineEdit()
        self._size = QSpinBox()
        self._size.setRange(TABLE_SIZE_MIN, TABLE_SIZE_MAX)
        self._button = QPushButton()

        # signals
        self._selector.currentIndexChanged.connect(self._onSelected)
        self._name.textChanged.connect(self._updateButton)
        self._button.clicked.connect(self._onCommit)

        # layout
        form = QFormLayout()
        form.addRow("Table", self._selector)
        form.addRow("Name", self._name)
        form.addRow("Size", self._size)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch()
        layout.addWidget(self._button)

        self.Refresh()

    def Refresh(self) -> None:
        # refill the selector and go back to a new empty entry
        self._tables = self._adapter.TablesList()
        self._selector.blockSignals(True)
        self._selector.clear()
        self._selector.addItem(NEW_TABLE_LABEL)
        self._selector.addItems([tableLabel(table) for table in self._tables])
        self._selector.blockSignals(False)
        self._onSelected(0)

    def _onSelected(self, index: int) -> None:
        # entry 0 is a new table, the others are the existing tables
        if index > 0:
            table = self._tables[index - 1]
            self._name.setText(table.Name)
            self._size.setValue(table.Size)
        else:
            self._name.clear()
            self._size.setValue(TABLE_SIZE_DEFAULT)
        self._updateButton()

    def _updateButton(self) -> None:
        self._button.setText("Save" if self._selector.currentIndex() > 0 else "Add")
        self._button.setEnabled(len(self._name.text().strip()) > 0)

    def _onCommit(self) -> None:
        # index is -1 for a new table
        index = self._selector.currentIndex() - 1
        name = self._name.text().strip()
        if any(table.Name == name for i, table in enumerate(self._tables) if i != index):
            QMessageBox.warning(self, "Tables", f"A table named \"{name}\" already exists.")
            return

        table = Table(
            Name = name,
            Size = self._size.value(),
        )
        if index < 0:
            self._adapter.AddTable(table)
        else:
            self._adapter.UpdateTable(index, table)

        self.Refresh()
        self.Changed.emit()

def tableLabel(table: Table) -> str:
    # how tables are shown in dropdowns, e.g. "A (4)"
    return f"{table.Name} ({table.Size})"
