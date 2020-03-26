import os
import glob
import shutil
import tempfile
import json
import multiprocessing

#import cc3d 
#from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller, CC3DCallerWorker

def run_sims(sim_paths):
    #sim_paths = glob.glob(os.path.join('.', 'cc3d', '*.cc3d'))
    output_folder = os.path.join('.', 'output')

    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    n_workers = 8 # try this?
    n_consumers = 2*multiprocessing.cpu_count()
    print(f'Creating {n_consumers} consumers')
    workers = [CC3DCallerWorker(tasks, results) for i in range(n_workers)]
    for w in workers:
        w.start()
    for i, path in enumerate(sim_paths):
        cc3d_caller = CC3DCaller(
            cc3d_sim_fname=path,
            screenshot_output_frequency=100,
            output_dir=os.path.join(output_folder, f'sim_{i}'),
            result_identifier_tag=i
        )
        tasks.put(cc3d_caller)

    for i in range(n_workers):
        tasks.put(None) # poison pill
    tasks.join() # wait

    data = []
    for _ in range(len(sim_paths)):
        data.append(results.get())
    return data

def generate_sim_files(betas, epsilons):
    stage_path = os.path.join('.', 'stage')
    os.makedirs(stage_path, exist_ok=True)
    sim_files = []
    # TODO how to handle this ...
    for i, (beta, epsilon) in enumerate(zip(betas, epsilons)):
        params_template = json.load(open('genome/params.json'))
        params_template['signaling']['halfexpress'] = beta
        params_template['signaling']['sharpness'] = epsilon
        sim_dir_path = os.path.join(stage_path, f'sim_{i}')
        os.makedirs(sim_dir_path, exist_ok=True)
        print(f'Spawning {sim_dir_path} files in stage {stage_path}')
        genome_path = os.path.join(sim_dir_path, 'genome.json')
        json.dump(str(params_template), open(genome_path, 'w'))
        shutil.copytree('cc3d/Simulation', sim_dir_path+'/Simulation', dirs_exist_ok=True)
        cc3d_path = sim_dir_path+'/sim.cc3d'
        shutil.copyfile('cc3d/sim.cc3d', cc3d_path)
        sim_files.append(cc3d_path)
    return sim_files

def clean_sims():
    shutil.rmtree('stage')