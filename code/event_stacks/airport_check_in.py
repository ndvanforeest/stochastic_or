"""Queueing at an airport check-in desk with business and economy customers."""

from dataclasses import dataclass

import numpy as np

import events
import job
import queues
import server
import servers
import simulator
import stats

ECONOMY = 0
BUSINESS = 1


@dataclass
class Job(job.Job):
    type: int = ECONOMY


@dataclass
class Server(server.Server):
    type: int = ECONOMY

class Simulation(simulator.Simulation):
    def __init__(self, num_e_servers, num_b_servers, share=False):
        self.share = share
        self.events = events.Events()
        self.stats = stats.Statistics()
        self.now = 0
        # ECONOMY
        self.e_queue = queues.Queue()
        self.e_servers = servers.Servers()
        for i in range(num_e_servers):
            self.e_servers.push(Server(id=i, rate=1, type=ECONOMY))
        # BUSINESS
        self.b_queue = queues.Queue()
        self.b_servers = servers.Servers()
        for i in range(num_b_servers):
            self.b_servers.push(Server(id=i, rate=1, type=BUSINESS))

    def handle_arrival(self, job):
        if job.type == ECONOMY:
            if self.e_servers.is_server_available():
                self.serve_job(job, self.e_servers)
            elif self.share and self.b_servers.is_server_available():
                self.serve_job(job, self.b_servers)
            else:
                self.e_queue.push(job)
        elif job.type == BUSINESS:
            if self.b_servers.is_server_available():
                self.serve_job(job, self.b_servers)
            else:
                self.b_queue.push(job)
        else:
            raise ValueError("Unknown job type")

    def handle_departure(self, job):
        self.stats.push(job)
        if job.server.type == ECONOMY:
            self.e_servers.push(job.server)
            if not self.e_queue.is_empty():
                self.serve_job(self.e_queue.pop(), self.e_servers)
        elif job.server.type == BUSINESS:
            self.b_servers.push(job.server)
            if not self.b_queue.is_empty():
                self.serve_job(self.b_queue.pop(), self.b_servers)
            elif self.share and not self.e_queue.is_empty():
                self.serve_job(self.e_queue.pop(), self.b_servers)
        else:
            raise ValueError("Unknown job type")

rng = np.random.default_rng(3)
check_in_window = 120  # minutes
desks_open = check_in_window + 30


# Make ECONOMY jobs
num = 300
A = np.sort(rng.uniform(low=0, high=check_in_window, size=num))
loads = rng.exponential(scale=2, size=num)
e_jobs = [
    Job(id=i, arrival_time=A[i], load=loads[i], type=ECONOMY)
    for i in range(1, num)
]


# BUSINESS jobs
num = 100
A = np.sort(rng.uniform(low=0, high=check_in_window, size=num))
loads = rng.exponential(scale=2, size=num)
# loads = rng.uniform(low=1, high=3, size=num)
b_jobs = [
    Job(id=i, arrival_time=A[i], load=loads[i], type=BUSINESS)
    for i in range(1, num)
]

num_e_servers, num_b_servers = 4, 2

e_work = sum(j.load for j in e_jobs)
e_service_available = num_e_servers * desks_open
print(f"Check e capacity: {e_work=:.0f}, {e_service_available=:.0f}")
b_work = sum(j.load for j in b_jobs)
b_service_available = num_b_servers * desks_open
print(f"Check b capacity: {b_work=:.0f}, {b_service_available=:.0f}")
tot_work = e_work + b_work
tot_service_available = (num_e_servers + num_b_servers) * desks_open
print(f"Check b capacity: {tot_work=:.0f}, {tot_service_available=:.0f}")

sim = Simulation(num_e_servers, num_b_servers, share=False)
sim.initialize_jobs(e_jobs)
sim.initialize_jobs(b_jobs)
sim.run()

def mean(iterable):
    "Compute mean of values in an iterable."
    total = count = 0
    for value in iterable:
        total += value
        count += 1
    if count == 0:
        raise ValueError("iterable is empty.")
    return total / count


print(f"Last departure e job: {e_jobs[-1].departure_time:.2f}")
print(f"Last departure b job: {b_jobs[-1].departure_time:.2f}")
print(f"Largest waiting time e job: {max(j.waiting_time for j in e_jobs):.2f}")
print(f"Largest waiting time b job: {max(j.waiting_time for j in b_jobs):.2f}")
print(f"Overall mean waiting time: {sim.stats.mean_waiting_time():.2f}")
print(f"mean waiting e jobs: {mean(job.waiting_time for job in e_jobs):.2f}")
print(f"mean waiting b jobs: {mean(job.waiting_time for job in b_jobs):.2f}")

sim = Simulation(num_e_servers + 1, num_b_servers, share=False)
sim.initialize_jobs(e_jobs)
sim.initialize_jobs(b_jobs)
sim.run()

print(f"Last departure e job: {e_jobs[-1].departure_time:.2f}")
print(f"Last departure b job: {b_jobs[-1].departure_time:.2f}")
print(f"Largest waiting time e job: {max(j.waiting_time for j in e_jobs):.2f}")
print(f"Largest waiting time b job: {max(j.waiting_time for j in b_jobs):.2f}")
print(f"Overall mean waiting time: {sim.stats.mean_waiting_time():.2f}")
print(f"mean waiting e jobs: {mean(job.waiting_time for job in e_jobs):.2f}")
print(f"mean waiting b jobs: {mean(job.waiting_time for job in b_jobs):.2f}")

sim = Simulation(num_e_servers, num_b_servers, share=True)
sim.initialize_jobs(e_jobs)
sim.initialize_jobs(b_jobs)
sim.run()

print(f"Last departure e job: {e_jobs[-1].departure_time:.2f}")
print(f"Last departure b job: {b_jobs[-1].departure_time:.2f}")
print(f"Largest waiting time e job: {max(j.waiting_time for j in e_jobs):.2f}")
print(f"Largest waiting time b job: {max(j.waiting_time for j in b_jobs):.2f}")
print(f"Overall mean waiting time: {sim.stats.mean_waiting_time():.2f}")
print(f"mean waiting e jobs: {mean(job.waiting_time for job in e_jobs):.2f}")
print(f"mean waiting b jobs: {mean(job.waiting_time for job in b_jobs):.2f}")
