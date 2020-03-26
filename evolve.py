import os
import threading
import argparse

#from EvoOpt.solvers.ParticleSwarmOptimization import ParticleSwarmOptimization as PSO
from utils.optimize import ParticleSwarmOptimizer as PSO

from run import generate_sim_files, run_sims, clean_sims
from utils.calculations import bond_angle_order

def fitness(betas, epsilons):
    sim_files = generate_sim_files(betas, epsilons)
    #data = run_sims(sim_files)
    #clean_sims()
    return []

def cycle(n, g):
    x = ['beta', 'epsilon']
    lb = [-2000, -2000]
    ub = [2000, 2000]
    optimizer = PSO(fitness, x, lb, ub, pop=n, max_gen=g)
    optimizer.solve()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optimizes `n` simulations in a ParticleSwarmOptimizer for up to `g` iterations.')
    parser.add_argument('--n', metavar='n', type=int, nargs=1, default=3, help='Number of simulations to optimize (default is 25)')
    parser.add_argument('--g', metavar='g', type=int, nargs=1, default=1, help='Number of iterations to optimize for (default is 10)')
    args = parser.parse_args()
    cycle(args.n, args.g)