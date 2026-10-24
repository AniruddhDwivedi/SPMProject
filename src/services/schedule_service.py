class ScheduleService:

    def get_matches(self):
        return [
            {
                "id": 1,
                "sport": "Football",
                "team_a": "VIT AP",
                "team_b": "VIT Vellore",
                "date": "Dec 12, 2026",
                "venue": "Ground 1",
                "status": "Scheduled",
            },
            {
                "id": 2,
                "sport": "Cricket",
                "team_a": "VIT Vellore",
                "team_b": "VIT Chennai",
                "date": "Dec 13, 2026",
                "venue": "Main Stadium",
                "status": "Scheduled",
            },
            {
                "id": 3,
                "sport": "Basketball",
                "team_a": "VIT Chennai",
                "team_b": "VIT Vellore",
                "date": "Dec 14, 2026",
                "venue": "Basketball Court",
                "status": "Scheduled",
            },
            {
                "id": 4,
                "sport": "Badminton",
                "team_a": "VIT AP",
                "team_b": "VIT Chennai",
                "date": "Dec 15, 2026",
                "venue": "Indoor Hall",
                "status": "Scheduled",
            },
        ]
