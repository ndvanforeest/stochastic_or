"""Queueing behavior under an N policy."""

import numpy as np

from event import ArrivalEvent, DepartureEvent
from events import Events
from job import Job
from queues import Queue
from server import Server
from servers import Servers
from stats import Statistics
from simulator import Simulation

import matplotlib.pyplot as plt
from latex_figures import fig_in_latex_format


class N_policy(Simulation):
    def __init__(self, events, queue, statistics, servers, thres_N):
        self.thres_N = thres_N
        super().__init__(events, queue, statistics, servers)

    def handle_arrival(self, job: Job):
        job.q_length_at_arrival = self.queue.length()
        self.queue.push(job)
        if (
            self.queue.length() >= self.thres_N
            and self.servers.is_server_available()
        ):
            self.serve_job(self.queue.pop())


num = 300
labda, mu = 3, 4
thres_N = 20

rng = np.random.default_rng(3)
X = rng.exponential(scale=1 / labda, size=num)
X[0] = 0
A = X.cumsum()
loads = rng.exponential(scale=1 / mu, size=num)
jobs = [Job(id=i, arrival_time=A[i], load=loads[i]) for i in range(1, num)]
servers = Servers()
servers.push(Server(id=1, rate=1))
sim = N_policy(Events(), Queue(), Statistics(), servers, thres_N=thres_N)
sim.initialize_jobs(jobs)
sim.run()


fig_in_latex_format.apply_figure_settings()
plt.figure(figsize=(6, 3))  # cm to inch
# plot queue at arrival times
x = [job.arrival_time for job in sim.stats]
y = [job.q_length_at_arrival for job in sim.stats]
plt.plot(x, y, 'o', ms=2, label="Arrivals")

# plot queue at departure times
x = [job.departure_time for job in sim.stats]
y = [job.q_lenght_at_departure for job in sim.stats]
plt.plot(x, y, 'x', ms=2, label="Departures")

plt.title("Queue length under N policy")
plt.xlabel("Time")
plt.ylabel("Jobs in system")
plt.legend()
plt.tight_layout()

plt.savefig("../../figures/n_policies.pdf")
