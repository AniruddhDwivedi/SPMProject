from src.services.supabase_client import supabase

class ScoreboardService:
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

    def save_result(
        self,
        match_id,
        team_a_score,
        team_b_score,
        result_details="",
    ):
        response = (
            supabase
            .table("matches")
            .update({
                "team_a_score": team_a_score,
                "team_b_score": team_b_score,
                "result_details": result_details.strip() or None,
                "status": "Completed",
            })
            .eq("id", match_id)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "No match was updated. Check the match ID "
                "and organizer permissions."
            )

        return response.data[0]
