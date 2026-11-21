import multiprocessing
import os
import sys

from PySide6.QtWidgets import QApplication

from adapters.adapter_json import AdapterJSON
from gui.statmanager import StatManager

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

    # StatView runs in its own process, so redrawing it never stalls StatManager; closing StatManager ends it too
    statView = multiprocessing.get_context("spawn").Process(target = runStatView, args = (databasePath,), daemon = True)
    statView.start()

    # StatManager runs in this process
    app = QApplication(argv)
    statManager = StatManager(adapter)
    statManager.show()
    return app.exec()

def runStatView(databasePath: str) -> None:
    # imported here, so only the StatView process loads matplotlib
    from gui.statview import StatView

    app = QApplication([])
    statView = StatView(databasePath)
    statView.show()
    app.exec()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
