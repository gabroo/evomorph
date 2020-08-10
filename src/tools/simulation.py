from os import environ, makedirs
from pathlib import Path
from shutil import copytree
import json
import multiprocessing
import concurrent.futures

from typing import List

from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller, CC3DCallerWorker
import numpy as np

#from viz import make_gif


class Simulation:
    def __init__(self, model: str, params: List[str], out_folder: Path):
        d_models = Path(__file__).parent.parent.parent/'models'
        self.d_model = d_models/model
        self.d_out = out_folder
        self.d_stage = out_folder/'stage'
        ncpus = environ.get("SLURM_CPUS_PER_TASK") 
        self.ncores = ncpus if ncpus else multiprocessing.cpu_count()
        self.params = params

    def gen(self, betas):
        makedirs(self.d_stage, exist_ok=True)
        def gen_dir(i):
            d_sim = self.d_stage / f"sim_{i:03}"
            makedirs(d_sim, exist_ok=True)
            shutil.copytree(self.d_model, d_sim)
            f_genome = d_sim/'genome.json'
            params = json.load(f_genome)
            params["signaling"]["halfexpress"] = float(betas[i])
            json.dump(params, f_genome)
            print(".", end="")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.ncores) as executor:
            try:
                for i in range(len(betas)):
                    executor.submit(gen_dir, i)
            except Exception as e:
                print(e)
                return False
        
        return True

    def run(self, n_runs):
        print(f"running {n_runs} sims on {self.ncores} CPUs")
        print(f"using model {self.d_model} with {self.params} as variables")
        betas = np.random.uniform(low=-10000, high=10000, size=(n_runs,))

        print("generating files")
        self.gen(betas)

        return

        print("running sim")
        makedirs(self.out_folder, exist_ok=True)
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        workers = [CC3DCallerWorker(tasks, results) for i in range(self.ncores)]
        genomes = {}
        datas = {}

        for w in workers:
            w.start()

        for i, path in enumerate(sim_paths):
            sim_out = self.out_folder / f"sim_{i:04}"
            cc3d_caller = CC3DCaller(
                cc3d_sim_fname=path, output_dir=str(sim_out), result_identifier_tag=i,
            )
            tasks.put(cc3d_caller)
            # preserve genome
            genomes[Path(path).parent / "Simulation" / "genome.json"] = (
                sim_out / "genome.json"
            )
            # preserve data FIXME this is horrible
            datas[Path(path).parent / "Simulation" / "data.json"] = (
                sim_out / "data.json"
            )

        for i in range(n_workers):
            tasks.put(None)  # "poison pill"
        tasks.join()  # wait for all tasks to complete

        # write genomes
        for src, dst in genomes.items():
            shutil.copy(src, dst)

        # write datas
        for src, dst in datas.items():
            shutil.copy(src, dst)

        print("res okay!")
        print("cleaning up")
        clean(Path(".").resolve() / "stage")
        np.save(Path(".").resolve() / "output" / "data", data, allow_pickle=True)
        print("making gifs ...")
        with concurrent.futures.ProcessPoolExecutor(max_workers=ncores) as executor:
            for i in range(len(sim_files)):
                base = output_folder / f"sim_{i:03}"
                executor.submit(
                    make_gif(str(base / "screenshots"), str(base / "movie.gif"))
                )
        print("done")
