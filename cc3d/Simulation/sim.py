import os
import sys
from pathlib import Path

from cc3d import CompuCellSetup

from steppables import LateralInhibition, Screenshots

sim_folder_path = sys.path[0]
print(sim_folder_path)
CompuCellSetup.register_steppable(LateralInhibition(params_path=sim_folder_path+'/genome.json'))

CompuCellSetup.register_steppable(Screenshots(frequency=100))

CompuCellSetup.run()
