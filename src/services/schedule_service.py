from src.services.supabase_client import supabase


class ScheduleService:
    def get_matches(self):
        response = (
            supabase
            .table("matches")
            .select("*")
            .order("match_date")
            .order("match_time")
            .execute()
        )

        return response.data or []

    def get_sports(self):
        matches = self.get_matches()

        sports = {
            match["sport"]
            for match in matches
            if match.get("sport")
        }

        return sorted(sports)