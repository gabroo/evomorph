from argparse import ArgumentParser
from pathlib import Path
from os import listdir
from tools.simulation import Simulation

import json

import numpy as np


def get_scores(d_out: Path) -> List[float]:
    print(f"fetching scores from {d_out}")
    scores = {}
    for p in d_out.iterdir():
        i = int(re.match(".*_0+(\d+)", str(p)).groups()[0])
        data = json.load((p / "data.json").open())
        mu = np.mean(data)
        sd = np.std(data)
        scores[i] = mu - sd / mu
    return scores


def cycle(s: Simulation, N: int, G: int, T: int, o: Path):
    trials = np.random.uniform(-10000, 10000, N)
    for g in range(G):
        print(f"generation {g+1}")
        out = o / f"gen_{g+1:03}"
        s.run_experiment(trials, t, out)
        scores = get_scores(out)
        json.dump(scores, (out / "scores.json").open("w"))
        if g+1 != G:
            Fmu = np.mean(np.array(scores.values()))
            good = {i for i, v in scores.items() if v > Fmu}
            good_trials = trials[i in good for i in scores]
            Nmu = np.mean(good_trials)
            Nsg = np.ptp(good_trials)
            trials = np.random.normal(Nmu, Nsg, N)


if __name__ == "__main__":
    parser = ArgumentParser(description="Optimizes `n` simulations for `g` iterations.")
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
        required=True,
        help="Model to simulate.",
        choices=listdir(Path(__file__).parent / "models"),
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
        type=str,
        help="Output folder.",
        default=(Path(__file__).parent.parent / "out").resolve(),
    )
    args = parser.parse_args()
    s = Simulation(args.model, ["beta"])
    cycle(s, args.individuals, args.generations, args.time, args.out)
