import sys
import cc3d 
from os.path import join
from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller
import json

def run():
    simulation_fname = join('.', 'cc3d', 'sim.cc3d')
    output_folder = join('.', 'output')
    cc3d_caller = CC3DCaller(
        cc3d_sim_fname=simulation_fname,
        screenshot_output_frequency=100,
        output_dir=output_folder,
    )
    data = cc3d_caller.run()
    with open('output/data.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    run()
