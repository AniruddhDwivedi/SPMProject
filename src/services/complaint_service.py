
from datetime import datetime, timezone

from src.services.supabase_client import supabase


class ComplaintService:
    def _current_user(self):
        response = supabase.auth.get_user()
        user = response.user

        if user is None:
            raise RuntimeError("You must be logged in.")

        return user

    def _current_role(self, user_id):
        response = (
            supabase.table("users")
            .select("role")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return response.data["role"]

    def submit_complaint(
        self,
        team_name,
        category,
        subject,
        description,
    ):
        user = self._current_user()

        if self._current_role(user.id) != "team_manager":
            raise PermissionError(
                "Only team managers can submit complaints."
            )

        team_name = team_name.strip()
        subject = subject.strip()
        description = description.strip()

        if not team_name or not category.strip():
            raise ValueError("Team name and category are required.")

        if not subject or not description:
            raise ValueError("Subject and description are required.")

        response = (
            supabase.table("complaints")
            .insert({
                "submitted_by": user.id,
                "team_name": team_name,
                "category": category.strip(),
                "subject": subject,
                "description": description,
            })
            .execute()
        )

        if not response.data:
            raise RuntimeError("The complaint was not saved.")

        return response.data[0]

    def get_my_complaints(self):
        user = self._current_user()

        if self._current_role(user.id) != "team_manager":
            raise PermissionError(
                "This view is for team managers."
            )

        response = (
            supabase.table("complaints")
            .select("*")
            .eq("submitted_by", user.id)
            .order("created_at", desc=True)
            .execute()
        )

        return response.data or []

    def get_all_complaints(self):
        user = self._current_user()

        if self._current_role(user.id) != "organizer":
            raise PermissionError(
                "Only organizers can view all complaints."
            )

        response = (
            supabase.table("complaints")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data or []

    def update_complaint(self, complaint_id, status, resolution):
        user = self._current_user()

        if self._current_role(user.id) != "organizer":
            raise PermissionError(
                "Only organizers can update complaints."
            )

        if status not in ("Submitted", "Under Review", "Resolved"):
            raise ValueError("Invalid complaint status.")

        resolution = resolution.strip()

        if status == "Resolved" and not resolution:
            raise ValueError(
                "Enter a resolution before resolving the complaint."
            )

        now = datetime.now(timezone.utc).isoformat()

        payload = {
            "status": status,
            "resolution": resolution or None,
            "updated_at": now,
            "resolved_at": now if status == "Resolved" else None,
        }

        response = (
            supabase.table("complaints")
            .update(payload)
            .eq("id", complaint_id)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "No complaint was updated. Refresh and try again."
            )

        return response.data[0]
