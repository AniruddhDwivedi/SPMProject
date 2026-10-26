from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class Match:
    match_id: int
    sport: str
    team_a: str
    team_b: str
    match_date: date
    match_time: time
    venue: str
    status: str = "Scheduled"

    @property
    def date_display(self) -> str:
        return self.match_date.strftime("%d %b %Y")

    @property
    def time_display(self) -> str:
        return self.match_time.strftime("%I:%M %p")