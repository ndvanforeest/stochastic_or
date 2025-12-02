"""Test of multi-server queue simulation with exact results of an M/M/c queue."""

import numpy as np

import mmc
from job import Job
from simulator import Simulation

num = 10000
labda, mu = 3, 4

rng = np.random.default_rng(3)
X = rng.exponential(scale=1 / labda, size=num)
X[0] = 0
A = X.cumsum()
loads = rng.exponential(scale=1 / mu, size=num)
jobs = [Job(id=i, arrival_time=A[i], load=loads[i]) for i in range(1, num)]


sim = Simulation()
sim.initialize_jobs(jobs)
sim.initialize_servers(server_rates=[1, 1])
sim.run()


mm2 = mmc.MMC(labda, mu, c=2)
print(f"W: {sim.stats.mean_waiting_time():0.4f}, {mm2.EW=:.4f}")
print(f"J: {sim.stats.mean_sojourn_time():0.4f}, {mm2.EJ=:.4f}")
print(f"Q: {sim.stats.mean_queue_length():0.4f}, {mm2.EQ=:.4f}")
