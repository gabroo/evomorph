import sys
import math
import random

from pathlib import Path

import numpy as np
import json

from cc3d.core.PySteppables import SteppableBasePy
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
    GREEN = 2
    RED = 4


class Screenshots(SteppableBasePy):
    def __init__(self, frequency=1):
        super().__init__(self, frequency)

    def step(self, t):
        self.request_screenshot(mcs=t, screenshot_label="screenshots")


class LateralInhibition(SteppableBasePy):
    def __init__(self, params_path, frequency=1):
        super().__init__(frequency)
        self.dir = params_path.parent
        self.params = json.load(params_path.open())
        self.cell_types = [Type.GREEN, Type.RED, Type.MEDIUM]
        self.data = []

    def start(self):
        for cell in self.cell_list:
            # TODO better way to access these values
            r = random.gauss(
                self.params["shape"]["rad_avg"], self.params["shape"]["rad_std"]
            )
            cell.lambdaSurface = 2.5  # FIXME magic numbers
            cell.lambdaVolume = 2.5
            cell.targetVolume = sphere_vol(r)
            cell.targetSurface = sphere_sa(r)
            cell.dict["pts"] = 0

            # red cells start activated (pts is how red it is)
            if cell.type == Type.RED:
                cell.dict["pts"] = 7000

    # updates cell attributes at each timestep `t`
    def step(self, t):
        # data collection
        n_red = 0
        csa_rg, csa_red = (0, 0)
        for cell in self.cell_list:
            points = 0
            csas = {tp: 0 for tp in self.cell_types}
            neighbors = self.get_cell_neighbor_data_list(cell)
            # n: neighbor, csa: common surface area
            for n, csa in neighbors:
                if n.type != cell.type and cell.type == Type.RED:  # don't double count
                    csa_rg += csa
                if n is None:  # medium
                    csas[Type.MEDIUM] += csa
                elif n.type == Type.GREEN:
                    csas[n.type] += csa
                elif n.type == Type.RED:
                    csas[n.type] += csa
                    points += csa * n.dict["pts"] / n.surface
            # update signaling (ie, points) for the cell
            signaling = self.params["signaling"]
            if cell.type == Type.GREEN or cell.type == Type.RED:
                # notes: this sigmoid should decrease over the x axis (points). ensure that [sharpness] > 0
                # ie, if everything is positive just use 1/(a+e^((x-b)/s)) <- downward facing sigmoid
                d_rep = (
                    1
                    / (
                        signaling["magnitude"]
                        + math.exp(
                            (points - signaling["halfexpress"]) / signaling["sharpness"]
                        )
                    )
                ) - (cell.dict["pts"] / signaling["decay"])
                cell.dict["pts"] += d_rep
                # TODO simple threshold for this example
                if cell.dict["pts"] >= signaling["threshold"]:
                    cell.type = Type.RED  # 4
                else:
                    cell.type = Type.GREEN  # 2

            motility = self.params["motility"]
            adhesion = self.params["adhesion"]
            if cell.type == Type.GREEN:
                cell.lambdaSurface = 2.2
                cell.lambdaVolume = 2.2
                cell.fluctAmpl = (
                    motility["constant"]
                    + motility["factor"]
                    * (
                        motility["adhesion"] * csas[Type.MEDIUM]
                        + adhesion["gg"] * csas[Type.GREEN]
                        + adhesion["gr"] * csas[Type.RED]
                    )
                    / cell.surface
                )

            elif cell.type == Type.RED:
                cell.lambdaSurface = 2.2
                cell.lambdaVolume = 2.2
                cell.fluctAmpl = (
                    motility["constant"]
                    + motility["factor"]
                    * (
                        motility["adhesion"] * csas[Type.MEDIUM]
                        + adhesion["gr"] * csas[Type.GREEN]
                        + adhesion["rr"] * csas[Type.RED]
                    )
                    / cell.surface
                )
                csa_red += cell.surface
                n_red += 1

        if csa_red != 0:
            fitness = csa_rg / csa_red
        else:
            fitness = 0
        self.data.append([t, fitness])

    def finish(self):
        pg = CompuCellSetup.persistent_globals
        pg.return_object = 1
        json.dump(self.data, (self.dir/'data.json').open('w'))
