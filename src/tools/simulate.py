from os import environ, makedirs
from os.path import exists
from pathlib import Path
from shutil import copytree, rmtree
import xml.etree.ElementTree as ET
import json
import re
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from typing import List

from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller, CC3DCallerWorker

from .viz import make_gif


class Simulation:
    def __init__(self, model: str):
        d_models = Path(__file__).parent.parent / "models"
        self.d_model = d_models / model
        ncpus = environ.get("SLURM_CPUS_PER_TASK")
        self.ncores = int(ncpus) if ncpus else multiprocessing.cpu_count()
        self.variables = json.load((self.d_model / "genome.json").open())

    def gen(self, stage: Path, n_steps: int, trials: List, freq: int):
        makedirs(stage, exist_ok=True)

        def gen_dir(i):
            try:
                d_sim = stage / f"sim_{i:03}"
                if exists(d_sim):
                    rmtree(d_sim)
                copytree(self.d_model, d_sim)
                f_genome = d_sim / "genome.json"
                params = json.load(f_genome.open())
                params["signaling"]["halfexpress"] = float(trials[i])
                params["frequency"] = freq
                json.dump(params, f_genome.open("w"))
                config = ET.parse(d_sim / "Simulation" / "config.xml")
                config.getroot().find("Potts").find("Steps").text = str(n_steps)
                config.write(d_sim / "Simulation" / "config.xml")
                print(".", end="")
            except Exception as e:
                print(e)

        with ThreadPoolExecutor(max_workers=self.ncores) as executor:
            for i in range(len(trials)):
                executor.submit(gen_dir, i)

        return True

    def run_experiment(self, trials: List, n_steps: int, d_out: Path, freq: int):
        """
        Run an experiment (a group of trials) for this model.
        
        `trials`: list containing the parameter sets for each trial.
        eg, if optimizing on two parameters:
            s = Simulation(...)
            # 10k time steps per simulation

        `n_steps`: number of Monte Carlo steps to run each trial

        `d_out`: the output directory for this experiment
        
        `freq`: screenshot output frequency

        """
        print(f"using model {self.d_model} with {self.params} as variables ...")
        print(
            f"running {len(trials)} sims for {n_steps} steps on {self.ncores} CPUs ..."
        )
        print(f"outputting every {freq} mcs to {d_out} ...")

        print("generating files", end=" ")
        self.gen(d_out, n_steps, trials, freq)

        print("running sims ...")
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        workers = [CC3DCallerWorker(tasks, results) for i in range(self.ncores)]

        for p in d_out.iterdir():
            if p.suffix == "":
                i = int(re.search("sim_(\d\d\d)", str(p)).groups()[0])
                cc3d_caller = CC3DCaller(
                    cc3d_sim_fname=p / "sim.cc3d",
                    output_dir=str(p),
                    result_identifier_tag=i,
                )
                tasks.put(cc3d_caller)

        for i in range(self.ncores):
            tasks.put(None)  # "poison pill"

        for w in workers:
            w.start()

        tasks.join()  # wait for all tasks to complete

        for i in range(len(trials)):
            res = results.get()
            if res["result"] != 1:
                print(f"issue with {res['tag']}")

        print("sims are done ...")
        print("making gifs ...")
        try:
            with ProcessPoolExecutor(max_workers=self.ncores) as executor:
                for p in d_out.iterdir():
                    if p.suffix == "":
                        executor.submit(
                            make_gif(str(p / "screenshots"), str(p / "movie.gif"))
                        )
        except Exception as e:
            print(f"error with making gifs: {e}")
        print("exiting ...")
