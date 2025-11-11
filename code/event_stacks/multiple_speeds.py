"""Simulate a multi-server queue with different speeds and compare
to an M/M/C queue."""

from collections import Counter

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
sim.initialize_servers(server_rates=[1, 0.1, 0.01])
sim.run()

mm1 = mmc.MMC(labda, mu, c=1)
print(f"W: {sim.stats.mean_waiting_time():0.2f}, {mm1.EW:0.2f}")
print(f"J: {sim.stats.mean_sojourn_time():0.2f}, {mm1.EJ:0.2f}")
print(f"Q: {sim.stats.mean_queue_length():0.2f}, {mm1.EQ:0.2f}")

count = Counter([j.free_servers for j in sim.stats])
print(count)
