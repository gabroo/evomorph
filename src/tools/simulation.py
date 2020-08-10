from os import environ, makedirs
from os.path import exists
from pathlib import Path
from shutil import copytree, rmtree
import xml.etree.ElementTree as ET
import json
import re
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import traceback

from typing import List

from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller, CC3DCallerWorker
import numpy as np

from .viz import make_gif


class Simulation:
    def __init__(self, model: str, params: List[str], out_folder: Path):
        d_models = Path(__file__).parent.parent/'models'
        self.d_model = d_models/model
        self.d_out = out_folder
        ncpus = environ.get("SLURM_CPUS_PER_TASK") 
        self.ncores = int(ncpus) if ncpus else multiprocessing.cpu_count()
        self.params = params

    def gen(self, stage: Path, n_steps: int, betas: List):
        makedirs(stage, exist_ok=True)
        def gen_dir(i):
            try:
                d_sim = stage / f"sim_{i:03}"
                if exists(d_sim):
                    rmtree(d_sim)
                copytree(self.d_model, d_sim)
                f_genome = d_sim/'genome.json'
                params = json.load(f_genome.open())
                params["signaling"]["halfexpress"] = float(betas[i])
                json.dump(params, f_genome.open('w'))
                config = ET.parse(d_sim/'Simulation'/'config.xml')
                config.getroot().find('Potts').find('Steps').text = str(n_steps)
                config.write(d_sim/'Simulation'/'config.xml')
                print(".", end="")
            except Exception as e:
                print(e)

        with ThreadPoolExecutor(max_workers=self.ncores) as executor:
            for i in range(len(betas)):
                executor.submit(gen_dir, i)
        
        return True

    def run(self, n_runs: int, n_steps: int):
        print(f"using model {self.d_model} with {self.params} as variables ...")
        print(f"running {n_runs} sims for {n_steps} steps on {self.ncores} CPUs ...")
        betas = np.random.uniform(low=-10000, high=10000, size=(n_runs,))

        print("generating files", end=" ")
        self.gen(self.d_out, n_steps, betas)

        print("running sims ...")
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        workers = [CC3DCallerWorker(tasks, results) for i in range(self.ncores)]
        genomes = {}
        datas = {}


        for p in self.d_out.iterdir():
            i = int(re.match(".*_0+(\d+)", str(p)).groups()[0])
            cc3d_caller = CC3DCaller(
                cc3d_sim_fname=p/'sim.cc3d', output_dir=str(p), result_identifier_tag=i,
            )
            tasks.put(cc3d_caller)

        for i in range(self.ncores):
            tasks.put(None)  # "poison pill"

        for w in workers:
            w.start()

        tasks.join()  # wait for all tasks to complete

        for i in range(n_runs):
            res = results.get()
            if res['result'] != 1:
                print(f"issue with {res['tag']}")
            
        print("sims are done ...")
        print("making gifs ...")
        with ProcessPoolExecutor(max_workers=self.ncores) as executor:
            for p in self.d_out.iterdir():
                executor.submit(
                    make_gif(str(p/'screenshots'), str(p/'movie.gif'))
                )
        print("exiting ...")
