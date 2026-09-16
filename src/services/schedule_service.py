class ScheduleService:

    def get_matches(self):
        return [
            {
                "id": 1,
                "sport": "Football",
                "team_a": "IIT Bombay",
                "team_b": "IIT Delhi",
                "date": "Dec 12, 2026",
                "venue": "Ground 1",
                "status": "Scheduled",
            },
            {
                "id": 2,
                "sport": "Cricket",
                "team_a": "IIT Madras",
                "team_b": "IIT Kanpur",
                "date": "Dec 13, 2026",
                "venue": "Main Stadium",
                "status": "Scheduled",
            },
            {
                "id": 3,
                "sport": "Basketball",
                "team_a": "IIT Kharagpur",
                "team_b": "IIT Roorkee",
                "date": "Dec 14, 2026",
                "venue": "Basketball Court",
                "status": "Scheduled",
            },
            {
                "id": 4,
                "sport": "Badminton",
                "team_a": "IIT Delhi",
                "team_b": "IIT Bombay",
                "date": "Dec 15, 2026",
                "venue": "Indoor Hall",
                "status": "Scheduled",
            },
        ]