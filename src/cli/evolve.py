import os
import threading
import argparse
import json

import numpy as np

from run import generate_sim_files, run_sims, clean_sims
from utils.calculations import bond_angle_order
from utils.optimize import GravitationalSearchOptimizer as GSO

G = 0
def fitness(betas, epsilons):
    global G
    sim_files, params = generate_sim_files(betas)
    data = run_sims(sim_files, G)
    #clean_sims()
    #order_scores = []
    #for d in data:
        #coms = d['result']
        #score = bond_angle_order(coms)
        #order_scores.append(score)
    #print(order_scores)
    #G += 1
    return np.array([1.0]*len(data), dtype=float)

def cycle(n, g):
    x = ['beta', 'epsilon']
    lb = [-2000, -2000]
    ub = [2000, 2000]
    optimizer = PSO(fitness, x, lb, ub, pop=n, max_gen=g)
    optimizer.solve()

if __name__ == '__main__':
    n_default, g_default = (100, 0)
    parser = argparse.ArgumentParser(description='Optimizes `n` simulations for up to `g` iterations.')
    parser.add_argument('--n', metavar='n', type=int, nargs=1, default=n_default, help=f'Number of simulations to optimize (default is {n_default})')
    parser.add_argument('--g', metavar='g', type=int, nargs=1, default=g_default, help=f'Number of iterations to optimize for (default is {g_default})')
    args = parser.parse_args()
    cycle(args.n, args.g)
