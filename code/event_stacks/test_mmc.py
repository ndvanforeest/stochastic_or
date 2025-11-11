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
print("W: ", sim.stats.mean_waiting_time(), mm2.EW)
print("J: ", sim.stats.mean_sojourn_time(), mm2.EJ)
print("Q: ", sim.stats.mean_queue_length(), mm2.EQ)
