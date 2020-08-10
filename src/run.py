from argparse import ArgumentParser
from pathlib import Path
from os import listdir
from tools.simulation import Simulation


def cycle(m, n, g):
    print(f"optimizing {n} of {m} for {g} generations")
    r = Runner()


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
        default=(Path(__file__).parent.parent / "out").resolve()
    )
    args = parser.parse_args()
    s = Simulation(args.model, ["beta"], Path(args.out))
    s.run(args.individuals, args.time)
