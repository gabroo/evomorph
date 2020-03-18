import sys
import math
import random
import numpy as np
from cc3d.core.PySteppables import SteppableBasePy
from cc3d import CompuCellSetup
from utils.config import load_json
from utils.calculations import sphere_vol, sphere_sa

class Type:
    MEDIUM = 0
    GREEN = 2
    RED = 4

class Screenshots(SteppableBasePy):
    def __init__(self, frequency=1):
        super().__init__(self, frequency)

    def step(self, t):
        self.request_screenshot(mcs=t, screenshot_label='screenshots')

class LateralInhibition(SteppableBasePy):
    def __init__(self, frequency=1, params_path=''):
        super().__init__(frequency)
        self.params = load_json(params_path)
        if not self.params:
            raise ValueError('error: returned parameters are empty (check the path)')
        self.cell_types = [Type.GREEN, Type.RED, Type.MEDIUM]
        self.t_max = self.params['simulation']['t_max']
        self.data = []

    def start(self):
        for cell in self.cell_list:
            # TODO better way to access these values
            r = random.gauss(self.params['shape']['rad_avg'], self.params['shape']['rad_std'])
            cell.lambdaSurface = 2.5 # FIXME magic number
            cell.lambdaVolume = 2.5
            cell.targetVolume = sphere_vol(r)
            cell.targetSurface = sphere_sa(r)
            cell.dict['pts'] = 0

            # red cells start activated
            if cell.type == Type.RED:
                cell.dict['pts'] = 7000

    # updates cell attributes at each timestep `t`
    def step(self, t):
        for cell in self.cell_list:
            points = 0
            csas = {tp: 0 for tp in self.cell_types}
            neighbors = self.get_cell_neighbor_data_list(cell)
            # n: neighbor, csa: common surface area
            for n, csa in neighbors:
                if n is None: # medium
                    csas[Type.MEDIUM] += csa
                elif n.type == Type.GREEN:
                    csas[n.type] += csa
                elif n.type == Type.RED:
                    csas[n.type] += csa
                    points += csa*n.dict['pts']/n.surface
            # update signaling (ie, points) for the cell
            signaling = self.params['signaling']
            if cell.type == Type.GREEN or cell.type == Type.RED:
                d_rep = (1/(signaling['magnitude']+math.exp(-1*(points-signaling['halfexpress'])/signaling['sharpness']))) - (cell.dict['pts']/signaling['decay'])
                cell.dict['pts'] += d_rep
                # TODO simple threshold for this example 
                if cell.dict['pts'] >= signaling['threshold']:
                    cell.type = 4
                else:
                    cell.type = 2

            motility = self.params['motility']
            adhesion = self.params['adhesion']
            if cell.type == Type.GREEN:
                cell.lambdaSurface = 2.2
                cell.lambdaVolume = 2.2
                cell.fluctAmpl = motility['constant'] + motility['factor']*(motility['adhesion']*csas[Type.MEDIUM] + adhesion['gg']*csas[Type.GREEN] + adhesion['gr']*csas[Type.RED])/cell.surface
                self.data.append([t, 'green', cell.dict['pts']])
        
            elif cell.type == Type.RED:
                cell.lambdaSurface = 2.2
                cell.lambdaVolume = 2.2
                cell.fluctAmpl = motility['constant'] + motility['factor']*(motility['adhesion']*csas[Type.MEDIUM] + adhesion['gr']*csas[Type.GREEN] + adhesion['rr']*csas[Type.RED])/cell.surface
                self.data.append([t, 'red', cell.dict['pts']])
    
    def finish(self):
        pg = CompuCellSetup.persistent_globals
        pg.return_object = self.data
