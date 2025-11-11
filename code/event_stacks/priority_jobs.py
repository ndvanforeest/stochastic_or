"""The effect of priority service in multi-server queues."""

from collections import defaultdict

import numpy as np

import mmc
from priority_job import PriorityJob
from simulator import Simulation

num = 10000
labda, mu = 3, 3.2

rng = np.random.default_rng(3)
X = rng.exponential(scale=1 / labda, size=num)
X[0] = 0
A = X.cumsum()
loads = rng.exponential(scale=1 / mu, size=num)
priorities = rng.binomial(1, 0.1, size=num)
jobs = []
for i in range(1, num):
    job = PriorityJob(id=i, arrival_time=A[i], load=loads[i])
    job.priority = priorities[i]
    jobs.append(job)


sim = Simulation()
sim.initialize_jobs(jobs)
sim.initialize_servers(server_rates=[1])
sim.run()

mm1 = mmc.MMC(labda, mu, c=1)
print(f"W: {sim.stats.mean_waiting_time():0.2f}, {mm1.EW:0.2f}")
print(f"J: {sim.stats.mean_sojourn_time():0.2f}, {mm1.EJ:0.2f}")
print(f"Q: {sim.stats.mean_queue_length():0.2f}, {mm1.EQ:0.2f}")

wait = defaultdict(float)
nums = defaultdict(float)
for j in sim.stats:
    nums[j.priority] += 1
    wait[j.priority] += j.waiting_time
for k in sorted(nums.keys()):
    print(f"Priority: {k}, EW: {wait[k] / nums[k]:.2f}")
