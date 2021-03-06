from argparse import ArgumentParser
from pathlib import Path
from os import listdir
from os.path import exists
from shutil import rmtree
from tools.simulate import Simulation
from typing import List

import json
import re

import numpy as np


def get_scores(d_out: Path) -> List[float]:
    print(f"fetching scores from {d_out}")
    scores = {}
    for p in d_out.iterdir():
        print(p)
        if p.suffix == "":
            i = int(re.search("sim_(\d\d\d)", str(p)).groups()[0])
            try:
                data = np.array(json.load((p / "data.json").open()))[:, 1]
                mu = np.mean(data)
                sd = np.std(data)
                scores[i] = mu - sd / mu
            except:
                scores[i] = 0
    return scores


def cycle(s: Simulation, N: int, G: int, t: int, o: Path, f: int, p: List):
    D = len(p)
    trials = np.ndarray((N, D), dtype=np.float64)
    for i, v in enumerate(p):
        trials[:, i] = np.random.uniform(v["from"], v["to"], size=N)
    print(trials)
    for g in range(G):
        print(f"generation {g+1}")
        out = o / f"gen_{g+1:03}"
        s.run_experiment(trials, t, out, f)
        json.dump(trials.tolist(), (out / "trials.json").open("w"))
        scores = get_scores(out)
        json.dump(scores, (out / "scores.json").open("w"))
        Fmu = np.mean(list(scores.values()))
        good = {i for i, v in scores.items() if v > Fmu}
        good_trials = trials[[i in good for i in sorted(scores)]]
        Nmu = np.mean(good_trials, axis=0)
        Nsd = np.ptp(good_trials, axis=0) / 4
        json.dump(good_trials.tolist(), (out / "good_sims.json").open("w"))
        json.dump({"mu": Nmu.tolist(), "sd": Nsd.tolist()}, (out / "new_dist.json").open("w"))
        print(Nmu.shape, Nsd.shape)
        trials = np.random.multivariate_normal(Nmu, np.identity(len(p)), size=N)
        print(trials)


if __name__ == "__main__":
    parser = ArgumentParser(description="Optimizes `n` simulations for `g` iterations.")
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="Configuration file for the experiment.",
        default="config.json",
    )
    parser.add_argument(
        "-n",
        "--individuals",
        metavar="N",
        type=int,
        required=True,
        help="Number of simulations that influence a single parametric update.",
    )
    parser.add_argument(
        "-g",
        "--generations",
        metavar="G",
        type=int,
        required=True,
        help="Number of parametric updates in this run.",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="Model to simulate.",
        choices=listdir("src/models"),
        required=True
    )
    parser.add_argument(
        "-t",
        "--time",
        type=int,
        required=True,
        help="Number of Monte Carlo steps per simualtion.",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        help="Output folder for screenshots and data.",
        required=True
    )
    parser.add_argument(
        "-f",
        "--frequency",
        type=int,
        required=True,
        help="Screenshot output frequency in Monte Carlo steps.",
    )
    args = parser.parse_args()
    config = json.load(args.config.open())
    variables = config["variables"]
    s = Simulation(args.model, variables)
    if exists(args.out):
        rmtree(args.out)
    cycle(
        s,
        args.individuals,
        args.generations,
        args.time,
        args.out,
        args.frequency,
        variables,
    )
