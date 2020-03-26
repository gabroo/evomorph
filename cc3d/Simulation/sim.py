from cc3d import CompuCellSetup

from steppables import LateralInhibition, Screenshots

CompuCellSetup.register_steppable(LateralInhibition(params_path='../genome.json'))
CompuCellSetup.register_steppable(Screenshots(frequency=100))

CompuCellSetup.run()
