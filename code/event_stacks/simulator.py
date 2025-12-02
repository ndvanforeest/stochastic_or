import events
import queues
import server
import servers
import stats
from event import ArrivalEvent, DepartureEvent
from job import Job


class Simulation:
    def __init__(self):
        self.events = events.Events()
        self.queue = queues.Queue()
        self.stats = stats.Statistics()
        self.servers = servers.Servers()
        self.now = 0

    def initialize_jobs(self, jobs):
        for job in jobs:
            self.events.push(ArrivalEvent(job.arrival_time, job))

    def initialize_servers(self, server_rates):
        for i, rate in enumerate(server_rates):
            self.servers.push(server.Server(id=i, rate=rate))

    def serve_job(self, job: Job, server_pool=None):
        "Serve job from a free server of the server pool."
        if server_pool is None:
            server_pool = self.servers
        server = server_pool.pop()
        job.free_servers = server_pool.num_free()
        job.server = server
        job.service_time = job.load / server.rate
        job.departure_time = self.now + job.service_time
        self.events.push(DepartureEvent(job.departure_time, job))

    def handle_arrival(self, job):
        job.q_length_at_arrival = self.queue.length()
        if self.servers.is_server_available():
            self.serve_job(job)
        else:
            self.queue.push(job)

    def handle_departure(self, job):
        self.servers.push(job.server)
        self.stats.push(job)
        if not self.queue.is_empty():
            self.serve_job(self.queue.pop())
        job.q_length_at_departure = self.queue.length()

    def run(self):
        while not self.events.is_empty():
            event = self.events.pop()
            self.now, job = event.time, event.job
            if isinstance(event, ArrivalEvent):
                self.handle_arrival(job)
            elif isinstance(event, DepartureEvent):
                self.handle_departure(job)
            else:
                raise ValueError("Unknown event")
