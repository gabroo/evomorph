import os
import sys
import json
from pathlib import Path

from cc3d import CompuCellSetup

from steppables import LateralInhibition, Screenshots

params_path = Path(sys.path[0]).parent/'genome.json'
params = json.load(params_path.open())
CompuCellSetup.register_steppable(LateralInhibition(params, params_path.parent))

CompuCellSetup.register_steppable(Screenshots(frequency=params['frequency']))

CompuCellSetup.run()
