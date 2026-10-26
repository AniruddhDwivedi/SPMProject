
from src.services.supabase_client import supabase


class PlayerReportingService:
    def get_players(self):
        response = (
            supabase
            .table("player_reports")
            .select("*")
            .order("reported_at", desc=True)
            .execute()
        )
        return response.data or []

    def register_player(self, data):
        player_name = data.get("player_name", "").strip()
        vit_name = data.get("vit_name", "").strip()
        sport = data.get("sport", "").strip()

        if not player_name or not vit_name or not sport:
            raise ValueError(
                "Player name, VIT/team, and sport are required."
            )

        payload = {
            "player_name": player_name,
            "player_id": data.get("player_id", "").strip() or None,
            "vit_name": vit_name,
            "sport": sport,
            "email": data.get("email", "").strip() or None,
            "phone": data.get("phone", "").strip() or None,
            "notes": data.get("notes", "").strip() or None,
            "documents_received": False,
            "hall_allocated": False,
            "id_card_issued": False,
            "credentials_created": False,
            "reporting_status": "Pending",
        }

        # Attribute the registration to the currently authenticated user.
        try:
            auth_response = supabase.auth.get_user()
            auth_user = auth_response.user
            if auth_user:
                payload["reported_by"] = auth_user.id
        except Exception:
            # The database policy still validates the authenticated role.
            pass

        response = (
            supabase
            .table("player_reports")
            .insert(payload)
            .execute()
        )

        if not response.data:
            raise RuntimeError("The player registration was not saved.")

        return response.data[0]

    def update_player(self, player_report_id, data):
        payload = {
            "documents_received": data["documents_received"],
            "hall_allocated": data["hall_allocated"],
            "hall_name": data["hall_name"].strip() or None,
            "id_card_issued": data["id_card_issued"],
            "credentials_created": data["credentials_created"],
            "reporting_status": data["reporting_status"],
            "notes": data["notes"].strip() or None,
            "updated_at": "now()",
        }

        # Supabase REST updates expect a concrete timestamp, not a SQL expression.
        from datetime import datetime, timezone
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()

        response = (
            supabase
            .table("player_reports")
            .update(payload)
            .eq("id", player_report_id)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "No player report was updated. Check the record and permissions."
            )

        return response.data[0]
