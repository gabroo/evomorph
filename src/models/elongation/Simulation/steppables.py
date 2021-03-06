import sys
import math
import random

from pathlib import Path

import numpy as np
import json

from cc3d.core.PySteppables import SteppableBasePy, MitosisSteppableBase
from cc3d import CompuCellSetup


def sphere_vol(r):
    """
    Volume of a sphere
    """
    return (4 / 3) * math.pi * (r ** 3)


def sphere_sa(r):
    """
    Surface area of a sphere
    """
    return 4 * math.pi * (r ** 2)


class Type:
    MEDIUM = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    RED = 4


RNG = random.SystemRandom()  # draw true random sequence, overkill but why not?
# Motility Variables
CtoM = 52  # cell to adhesion value, self-consistent across simulations as 26 but x2 due to double interface formation
BASALYB = 100  # baseline motility for L929, due to their extremely motile behaviour
BASALGR = 1
SCF = 0.5  # self-attenuator weighing basal motility vs loss of motility due to adhesion
# Self-Cutoff
ENDMCS = 50000  # call runtime here directly
# Mitosis Variables
RADAVG = 3  # average radius of the gaussian distribution to choose random radius
RADDEV = 0.5  # standard deviation of target radius, too low and division couples, too high and you'll lose cells at the start
MTFORCEMIN = -3 * 10 ** (
    -3.88
)  # negative mitosis driving force fluctuation, usually only need to change the exponential part
MTFORCEMAX = 4 * 10 ** (
    -3.88
)  # positive mitosis driving force fluctuation, usually change only the exponential part
# Signaling Variables
CONEXPSCF = 10000  # Steady state expression of ligand expressed on a sender cell. This ligand is unaffected by signaling.
THETA = 0  # time lag for expression of your constitutive, non-signaling affected ligand, start at 0 for simplicity, but can be adjusted depending on experiment results if known for generalizability
XI = 1000  # controls how fast the sender cells reaches steady state for your constitutive, non-signaling affected ligand
FASTAPPROX = 5000  # force approx for function of above variables at the time step, saves calling the mcs and doing the caluclation, purely computational speed effeciency

ALPHAYG = 1  # controls how much your reporter synthesis magnitude due to signal S; can be set to 1 if decay is set properly
BETAYG = 921.181  # threshold of signal required to generate a response in your cell due to signaling
EPSILONYG = 526.389  # modulates how sharp the response is due to signaling, can turn synthesis to linear or heavi-side theta like if desired
KAPPAYG = 25000  # general decay constant
THRESHOLDUPYG = 4500  # activation threshold to change state
THRESHOLDDOYG = 0  # deactivation threshold to revert state, as no clear deactivation/unsorting occured in reference experiments

ALPHABR = 1  # controls how much your reporter synthesis magnitude due to signal S; can be set to 1 if decay is set properly
BETABR = 921.181  # threshold of signal required to generate a response in your cell due to signaling
EPSILONBR = 526.389  # modulates how sharp the response is due to signaling, can turn synthesis to linear or heavi-side theta like if desired
KAPPABR = 25000  # general decay constant
THRESHOLDUPBR = 4500  # activation threshold to change state, the choice of paramters in this paragraph render it similar to that of the previous paragraph
THRESHOLDDOBR = 0  # deactivation threshold to revert state, as no clear deactivation/unsorting occured in reference experiments

# Single Cell Trace Variables
MARKEDCELLS = [
    11,
    112,
    247,
    277,
]  # ID of cells to track if you desire single cell points tracked, change to fit setup

# Sampling and Comp Speed
RESOL = 100  # Data sampling rate, choose to satisfy nyquist theorem if necessary
USEDNODES = 8  # Choose a power of 2, otherwise the grids overlap and your simulation will eventually randomly crash, follow the recommendations given in the manual by developers


class Screenshots(SteppableBasePy):
    def __init__(self, frequency=1):
        super().__init__(self, frequency)

    def step(self, t):
        self.request_screenshot(mcs=t, screenshot_label="screenshots")


class Elongation(SteppableBasePy):
    def __init__(self, params, d_out, frequency=1):
        super().__init__(frequency)
        self.dir = d_out
        self.params = params
        self.cell_types = [Type.GREEN, Type.YELLOW, Type.BLUE, Type.RED, Type.MEDIUM]
        self.data = []

    def start(self):
        for cell in self.cellList:
            r = random.gauss(
                self.params["shape"]["rad_avg"], self.params["shape"]["rad_std"]
            )
            cell.lambdaSurface = 2.5  # FIXME magic numbers
            cell.lambdaVolume = 2.5
            cell.targetVolume = sphere_vol(r)
            cell.targetSurface = sphere_sa(r)
            cell.dict["pts"] = 0
            cell.dict["RDM"] = r

    def step(self, mcs):
        for cell in self.cellList:  # iterate over cell list
            csas = {tp: 0 for tp in self.cell_types}

            PTSY = 0  # each cell gains points from neighbor type Y
            PTSG = 0  # each cell gains points from neighbor type G
            PTSB = 0  # each cell gains points from neighbor type B
            PTSR = 0  # each cell gains points from neighbor type R
            DTRES = 0  # change in reporter due to signal S
            SECLPTSR = 0  # second signaling loop green points
            SECLPTSG = 0  # second signaling loop red points

            neighbors = self.get_cell_neighbor_data_list(cell)
            for n, csa in neighbors:
                if n is None:
                    csas[Type.MEDIUM] += csa
                elif n.type == Type.YELLOW:
                    csas[Type.YELLOW] += csa
                    PTSY += (
                        csa
                        * (CONEXPSCF / (1 + math.exp(-(mcs - THETA) / XI)))
                        / n.surface
                    )
                elif n.type == Type.GREEN:
                    csas[Type.GREEN] += csa
                    PTSG += (
                        csa
                        * (CONEXPSCF / (1 + math.exp(-(mcs - THETA) / XI)))
                        / n.surface
                    )
                    SECLPTSG += csa * n.dict["pts"] / (n.surface)
                elif n.type == Type.BLUE:
                    csas[Type.BLUE] += csa
                    PTSB += (
                        csa
                        * (CONEXPSCF / (1 + math.exp(-(mcs - THETA) / XI)))
                        / n.surface
                    )
                elif n.type == Type.RED:
                    csas[Type.RED] += csa
                    PTSR += (
                        csa
                        * (CONEXPSCF / (1 + math.exp(-(mcs - THETA) / XI)))
                        / n.surface
                    )
                    SECLPTSR += csa * n.dict["pts"] / (n.surface)

            # end of neighbor loop

            if cell.type == 1 or cell.type == 2:
                DTRES = (
                    1
                    / (
                        ALPHAYG
                        + math.exp(-((PTSB + PTSR + SECLPTSG) - BETAYG) / EPSILONYG)
                    )
                ) - (1 / KAPPAYG) * cell.dict["pts"]
                cell.dict["pts"] += DTRES
            if cell.type == 3 or cell.type == 4:
                DTRES = (
                    1
                    / (
                        ALPHABR
                        + math.exp(-((PTSY + PTSG + SECLPTSR) - BETABR) / EPSILONBR)
                    )
                ) - (1 / KAPPABR) * cell.dict["pts"]
                cell.dict["pts"] += DTRES

            thresholds = self.params["thresholds"]

            if cell.type == Type.YELLOW:
                if cell.dict["pts"] >= thresholds['yg_up']:
                    cell.type = 2
            if cell.type == Type.GREEN:
                if cell.dict["pts"] < thresholds['yg_down']:
                    cell.type = 1
            if cell.type == Type.BLUE:
                if cell.dict["pts"] >= thresholds['br_up']:
                    cell.type = 4
            if cell.type == Type.RED:
                if cell.dict["pts"] < thresholds['br_down']:
                    cell.type = 3

            adhesion = self.params["adhesion"]
            if cell.type == 1:  # gray cells
                cell.lambdaSurface = 1.0  # change depending on cell adhesitivity
                cell.lambdaVolume = 1.0  # change depending on cell adhesitivity
                cell.fluctAmpl = (
                    BASALYB
                    + SCF
                    * (
                        CtoM * csas[Type.MEDIUM]
                        + adhesion["yy"] * csas[Type.YELLOW]
                        + adhesion["yg"] * csas[Type.GREEN]
                        + adhesion["yb"] * csas[Type.BLUE]
                        + adhesion["yr"] * csas[Type.RED]
                    )
                    / cell.surface
                )  # corrected cell motility, tune based on adhesive neighbors, vetted

            if cell.type == 2:  # green cells
                cell.lambdaSurface = 1.0  # change depending on cell adhesitivity
                cell.lambdaVolume = 1.0  # change depending on cell adhesitivity
                cell.fluctAmpl = (
                    BASALGR
                    + SCF
                    * (
                        CtoM * csas[Type.MEDIUM]
                        + adhesion["yg"] * csas[Type.YELLOW]
                        + adhesion["gg"] * csas[Type.GREEN]
                        + adhesion["gb"] * csas[Type.BLUE]
                        + adhesion["gr"] * csas[Type.RED]
                    )
                    / cell.surface
                )  # corrected cell motility, tune based on adhesive neighbors, vetted

            if cell.type == 3:  # blue cells
                cell.lambdaSurface = 1.0  # change depending on cell adhesitivity
                cell.lambdaVolume = 1.0  # change depending on cell adhesitivity
                cell.fluctAmpl = (
                    BASALYB
                    + SCF
                    * (
                        CtoM * csas[Type.MEDIUM]
                        + adhesion["yb"] * csas[Type.YELLOW]
                        + adhesion["gb"] * csas[Type.GREEN]
                        + adhesion["bb"] * csas[Type.BLUE]
                        + adhesion["br"] * csas[Type.RED]
                    )
                    / cell.surface
                )  # corrected cell motility, vetted

            if cell.type == 4:  # red cells
                cell.lambdaSurface = 1.0  # change depending on cell adhesitivity
                cell.lambdaVolume = 1.0  # change depending on cell adhesitivity
                cell.fluctAmpl = (
                    BASALGR
                    + SCF
                    * (
                        CtoM * csas[Type.MEDIUM]
                        + adhesion["yr"] * csas[Type.YELLOW]
                        + adhesion["gr"] * csas[Type.GREEN]
                        + adhesion["br"] * csas[Type.BLUE]
                        + adhesion["rr"] * csas[Type.RED]
                    )
                    / cell.surface
                )  # corrected cell motility, vetted

    def finish(self):
        pass


class Mitosis(MitosisSteppableBase):
    def __init__(self, frequency=1):
        super().__init__(frequency)
        # randomize child cell position, see developer manual
        self.set_parent_child_position_flag(0) 

    def step(self, mcs):
        cells_to_divide = []  # gen cells to divide list
        for cell in self.cellList:
            if cell.type == 1 or cell.type == 3:
                cell.dict["RDM"] += RNG.uniform(
                    MTFORCEMIN, MTFORCEMAX
                )  # make cells grow in target radius by this much
                cell.targetSurface = (
                    4 * math.pi * cell.dict["RDM"] ** 2
                )  # spherical surface area
                cell.targetVolume = (
                    (4 / 3) * math.pi * cell.dict["RDM"] ** 3
                )  # spherical volume
                if (
                    cell.volume > 2 * (4 / 3) * math.pi * RADAVG ** 3
                ):  # divide at two times the mean radius initialized with
                    cells_to_divide.append(cell)  # add these cells to divide list

        for cell in cells_to_divide:
            self.divideCellRandomOrientation(cell)  # divide the cells

    def updateAttributes(self):
        self.parentCell.dict["RDM"] = RNG.gauss(
            RADAVG, RADDEV
        )  # reassign new target radius
        self.parentCell.targetVolume = (
            (4 / 3) * math.pi * self.parentCell.dict["RDM"] ** 3
        )  # new target volume
        self.parentCell.targetSurface = (
            4 * math.pi * self.parentCell.dict["RDM"] ** 2
        )  # new target surface area
        self.cloneParent2Child()  # copy characterstics to child cell, indlucig signaling
