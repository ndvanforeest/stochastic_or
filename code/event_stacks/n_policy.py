"""Queueing behavior under an N policy."""

import numpy as np

from job import Job
from simulator import Simulation


class N_policy(Simulation):
    def __init__(self, thres_N):
        self.thres_N = thres_N
        super().__init__()

    def handle_arrival(self, job: Job):
        job.q_length_at_arrival = self.queue.length()
        self.queue.push(job)
        if (
            self.queue.length() >= self.thres_N
            and self.servers.is_server_available()
        ):
            self.serve_job(self.queue.pop(), self.servers)
