import matplotlib.pyplot as plt
import numpy as np
from latex_figures import apply_figure_settings

from job import Job
from n_policy import N_policy

num = 300
labda, mu = 3, 4
thres_N = 20

rng = np.random.default_rng(3)
X = rng.exponential(scale=1 / labda, size=num)
X[0] = 0
A = X.cumsum()
loads = rng.exponential(scale=1 / mu, size=num)
jobs = [Job(id=i, arrival_time=A[i], load=loads[i]) for i in range(1, num)]

sim = N_policy(thres_N=thres_N)
sim.initialize_jobs(jobs)
sim.initialize_servers(server_rates=[1])
sim.run()


apply_figure_settings(use=True)
plt.figure(figsize=(6, 3))
x = [job.arrival_time for job in sim.stats]
y = [job.q_length_at_arrival for job in sim.stats]
plt.plot(x, y, 'o', ms=2, label="Arrivals")

x = [job.departure_time for job in sim.stats]
y = [job.q_length_at_departure for job in sim.stats]
plt.plot(x, y, 'x', ms=2, label="Departures")

plt.title("Queue length under N policy")
plt.xlabel("Time")
plt.ylabel("Jobs in system")
plt.legend()
plt.tight_layout()

plt.savefig("../../figures/n_policies.pdf")
plt.savefig("../../figures/n_policies.png", dpi=300)
