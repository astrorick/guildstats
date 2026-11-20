import os
import sys

from model.adapters import AdapterJSON
from plot.colordist import plotColorDistribution
from plot.sidequestsgnr import plotGenericSidequestHist
from plot.sidequeststhm import plotThematicSidequestHist
from plot.tablepoints import plotTablePoints
from plot.totalpoints import plotTotalPoints

OUTPUT_FOLDER = "output"

def main(argv: list[str]):
    # load database
    adapter = AdapterJSON(argv[1])
    databaseInfo = adapter.DatabaseInfo()
    playersList = adapter.PlayersList()

    # generate plots
    os.makedirs(OUTPUT_FOLDER, exist_ok = True)
    plotColorDistribution(playersList, OUTPUT_FOLDER)
    plotGenericSidequestHist(playersList, OUTPUT_FOLDER)
    plotThematicSidequestHist(playersList, OUTPUT_FOLDER)
    plotTablePoints(playersList, OUTPUT_FOLDER)
    plotTotalPoints(playersList, OUTPUT_FOLDER)

if __name__ == "__main__":
    main(sys.argv)
