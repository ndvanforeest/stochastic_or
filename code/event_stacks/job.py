from dataclasses import dataclass

from server import Server


@dataclass
class Job:
    id: int
    arrival_time: float
    load: float
    service_time: float = 0
    departure_time: float = 0
    q_length_at_arrival: int = 0
    q_length_at_departure: int = 0
    free_servers: int = 0
    server: Server = None

    @property
    def sojourn_time(self):
        return self.departure_time - self.arrival_time

    @property
    def waiting_time(self):
        return self.sojourn_time - self.service_time

    def __str__(self):
        return (
            f"{self.id},  load={self.load:.2f}, service={self.service_time:.2f},"
            f" arr={self.arrival_time:.2f}, dep={self.departure_time:.2f}"
        )

    def __hash__(self):
        return self.id

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time
