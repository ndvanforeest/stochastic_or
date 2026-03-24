import numpy as np
import mmc
from job import Job
from simulator import Simulation


def run_mmc(num, labda=3, mu=4, server_rates=[1, 1]):
    rng = np.random.default_rng(3)
    X = rng.exponential(scale=1 / labda, size=num)
    X[0] = 0
    A = X.cumsum()
    loads = rng.exponential(scale=1 / mu, size=num)
    jobs = [Job(id=i, arrival_time=A[i], load=loads[i]) for i in range(1, num)]

    sim = Simulation()
    sim.initialize_jobs(jobs)
    sim.initialize_servers(server_rates=server_rates)
    sim.run()

    c = len(server_rates)
    mm = mmc.MMC(labda, mu, c=c)

    print(f"W: {sim.stats.mean_waiting_time():0.4f}, {mm.EW=:.4f}")
    print(f"J: {sim.stats.mean_sojourn_time():0.4f}, {mm.EJ=:.4f}")
    print(f"Q: {sim.stats.mean_queue_length():0.4f}, {mm.EQ=:.4f}")
