from os import environ, makedirs
from pathlib import Path
import glob
import shutil
import tempfile
import json
import multiprocessing
import concurrent.futures
import builtins
import argparse

import numpy as np

from typing import List

from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller, CC3DCallerWorker

# from viz import make_gif


class Simulation:
    def __init__(self, model: str, params: List[str], out_folder: Path):
        self.model = model
        self.out_folder = out_folder
        self.ncores = environ.get("SLURM_CPUS_PER_TASK")
        self.params = params

    def gen(betas, stage_path=Path(".").resolve() / "stage"):
        os.makedirs(stage_path, exist_ok=True)
        sim_files = []
        param_files = []

        def gen_dir(i):
            params_template = json.loads(open("templates/genome.json").read())
            params_template["signaling"]["halfexpress"] = float(betas[i])
            sim_dir_path = stage_path / f"sim_{i:03}"
            os.makedirs(sim_dir_path, exist_ok=True)
            print(".", end="")
            if not (sim_dir_path / "Simulation").exists():
                shutil.copytree("templates/Simulation", sim_dir_path / "Simulation")
            if not (sim_dir_path / "screenshot_data").exists():
                shutil.copytree(
                    "templates/screenshot_data", sim_dir_path / "screenshot_data"
                )
            cc3d_path = sim_dir_path / "sim.cc3d"
            shutil.copyfile("templates/sim.cc3d", cc3d_path)
            genome_path = sim_dir_path / "Simulation" / "genome.json"
            open(genome_path, "w").write(json.dumps(params_template))
            return cc3d_path, genome_path

        with concurrent.futures.ThreadPoolExecutor(max_workers=ncores) as executor:
            fs = [executor.submit(gen_dir, i) for i in range(len(betas))]
            for f in concurrent.futures.as_completed(fs):
                tp = f.result()
                sim_files.append(tp[0])
                param_files.append(tp[1])

    return sim_files, param_files

    def run(self, n_runs):
        print(f"running {n_runs} sims on {self.ncores} CPUs")
        print(f"using {self.model} with {self.params} as variables")
        return
        betas = np.random.uniform(low=-10000, high=10000, size=(nsims,))
        print(f"this is what {nsims} dots looks like:")
        print("".join(["." for i in range(nsims)]))
        print("generating files")
        sim_files, params = generate_sim_files(betas)
        print("running sim")
        res = run_sims(sim_files, ncores, output_folder)
        makedirs(self.out_folder, exist_ok=True)
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        print(f"using {self.ncores} workers")
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
