import os
from pathlib import Path
import glob
import shutil
import tempfile
import json
import multiprocessing

import numpy as np

from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller, CC3DCallerWorker

def run_sim(sim_path, n_runs):
    '''
    Runs a single simulation file a specified number of times. Output folder is at the same leve of the specified cc3d file.

    params:
        sim_path - path to `.cc3d` file of the simulation
        n_runs - # of times to run the simulation
    '''
    output_folder = os.path.join(os.path.dirname(sim_path), 'output')
    data = []
    cc3d_caller = CC3DCaller(
        cc3d_sim_fname=sim_path,
        screenshot_output_frequency=100, #FIXME magic number
        output_dir=output_folder
    )
    data.append(cc3d_caller.run())
    data_file = open(os.path.join(output_folder, 'data.json'))
    data_file.write(json.dumps(data))

def run_sims(sim_paths, generation):
    output_folder = os.path.join('.', 'output', 'evolution')
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    n_workers = len(sim_paths) # try this?
    n_consumers = multiprocessing.cpu_count()
    workers = [CC3DCallerWorker(tasks, results) for i in range(n_workers)]
    for w in workers:
        w.start()
    for i, path in enumerate(sim_paths):
        cc3d_caller = CC3DCaller(
            cc3d_sim_fname=path,
            screenshot_output_frequency=100, #FIXME magic number
            output_dir=os.path.join(output_folder, f'gen_{generation}', f'sim_{i}'),
            result_identifier_tag=i
        )
        tasks.put(cc3d_caller)

    for i in range(n_workers):
        tasks.put(None) # "poison pill"
    tasks.join() # wait for all tasks to complete
    data = []
    for _ in range(len(sim_paths)):
        data.append(results.get())
    json.dump(data, open(os.path.join(output_folder, 'data.json'), 'w'))
    return np.array(data)

def generate_sim_files(betas):
    stage_path = Path('.').resolve()/'stage'
    os.makedirs(stage_path, exist_ok=True)
    sim_files = []
    param_files = []
    # TODO how to handle this ...
    for i, beta in enumerate(betas):
        params_template = json.loads(open('genome/params.json').read())
        params_template['signaling']['halfexpress'] = float(beta)
        #params_template['signaling']['sharpness'] = float(epsilon)
        sim_dir_path = stage_path/f'sim_{i}'
        os.makedirs(sim_dir_path, exist_ok=True)
        print(f'Spawning {sim_dir_path} files in stage {stage_path}')
        if not (sim_dir_path/'Simulation').exists():
            shutil.copytree('cc3d/Simulation', sim_dir_path/'Simulation')
        if not (sim_dir_path/'screenshot_data').exists():
            shutil.copytree('cc3d/screenshot_data', sim_dir_path/'screenshot_data')
        cc3d_path = sim_dir_path/'sim.cc3d'
        shutil.copyfile('cc3d/sim.cc3d', cc3d_path)
        sim_files.append(cc3d_path)
        genome_path = sim_dir_path/'Simulation'/'genome.json'
        open(genome_path, 'w').write(json.dumps(params_template))
        param_files.append(genome_path)
    return sim_files, param_files

def clean_sims():
    shutil.rmtree('stage')

if __name__ == '__main__':
    # tests of run_sim
    for i in range(3):
        run_sim(f'./tests/{i}/sim.cc3d', 1)