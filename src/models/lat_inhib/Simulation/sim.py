import os
import sys
from pathlib import Path

from cc3d import CompuCellSetup

from steppables import LateralInhibition, Screenshots

CompuCellSetup.register_steppable(LateralInhibition(params_path=sys.path[0]+'/genome.json'))

CompuCellSetup.register_steppable(Screenshots(frequency=500))

CompuCellSetup.run()
