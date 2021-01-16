import os
import sys
import json
from pathlib import Path

from cc3d import CompuCellSetup

from steppables import ThreeLayer, Screenshots, Mitosis

params_path = Path(sys.path[0]).parent/'genome.json'
params = json.load(params_path.open())
CompuCellSetup.register_steppable(ThreeLayer(params, params_path.parent))

CompuCellSetup.register_steppable(Screenshots(params_path.parent, frequency=params['frequency']))
CompuCellSetup.register_steppable(Mitosis())

CompuCellSetup.run()
