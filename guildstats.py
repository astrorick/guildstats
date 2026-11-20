import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from adapters.adapter_json import AdapterJSON
from gui.statmanager import StatManager
from gui.statview import StatView

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: python3 {os.path.basename(argv[0])} <database.json>")
        return 1

    # load the database, or create an empty one
    databasePath = argv[1]
    if os.path.isfile(databasePath):
        adapter = AdapterJSON(databasePath)
    else:
        adapter = AdapterJSON.CreateEmpty(databasePath)
        print(f"Created new database: {databasePath}")

    # open both windows, closing the manager quits the app
    app = QApplication(argv)
    statView = StatView(databasePath)
    statView.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
    statManager = StatManager(adapter)
    statView.show()
    statManager.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
