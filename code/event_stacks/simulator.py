from event import ArrivalEvent, DepartureEvent
from job import Job


class Simulation:
    def __init__(self, events, queue, statistics, servers):
        self.events = events
        self.queue = queue
        self.stats = statistics
        self.servers = servers
        self.now = 0

    def initialize_jobs(self, jobs):
        for job in jobs:
            self.events.push(ArrivalEvent(job.arrival_time, job))

    def serve_job(self, job: Job):
        server = self.servers.pop()
        job.server = server
        job.service_time = job.load / server.rate
        job.departure_time = self.now + job.service_time
        job.free_servers = self.servers.num_free()
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
        job.q_lenght_at_departure = self.queue.length()

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
