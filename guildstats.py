import os
import sys

from model.adapters import AdapterJSON
from plot.colordist import plotColorDistribution
from plot.sidequests import plotSidequestPies

OUTPUT_FOLDER = "output"

def main(argv: list[str]):
    # load database
    adapter = AdapterJSON(argv[1])
    databaseInfo = adapter.DatabaseInfo()
    playersList = adapter.PlayersList()

    # generate plots
    os.makedirs(OUTPUT_FOLDER, exist_ok = True)
    plotColorDistribution(playersList, os.path.join(OUTPUT_FOLDER, "deck_color_distribution.png"))
    plotSidequestPies(playersList, os.path.join(OUTPUT_FOLDER, "sidequest_pies.png"))

if __name__ == "__main__":
    main(sys.argv)
