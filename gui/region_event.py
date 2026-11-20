from PySide6.QtWidgets import QFormLayout, QGroupBox, QLineEdit, QPushButton, QVBoxLayout

from adapters.adapter_json import AdapterJSON
from model.event import Event

class RegionEvent(QGroupBox):
    def __init__(self, adapter: AdapterJSON):
        super().__init__("Event")
        self._adapter = adapter

        # input fields
        self._name = QLineEdit()
        self._date = QLineEdit()
        self._date.setPlaceholderText("YYYY-MM-DD")
        self._location = QLineEdit()
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self._onSave)

        # layout
        form = QFormLayout()
        form.addRow("Name", self._name)
        form.addRow("Date", self._date)
        form.addRow("Location", self._location)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch()
        layout.addWidget(saveButton)

        self.Refresh()

    def Refresh(self) -> None:
        event = self._adapter.EventInfo()
        self._name.setText(event.Name)
        self._date.setText(event.Date)
        self._location.setText(event.Location)

    def _onSave(self) -> None:
        self._adapter.UpdateEventInfo(
            Event(
                Name = self._name.text().strip(),
                Date = self._date.text().strip(),
                Location = self._location.text().strip(),
            )
        )
        self.Refresh()
