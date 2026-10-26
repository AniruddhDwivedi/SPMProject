from datetime import datetime, timedelta, timezone

from src.services.supabase_client import supabase


class KitService:
    def _current_user(self):
        response = supabase.auth.get_user()
        user = response.user

        if user is None:
            raise RuntimeError("You must be logged in.")

        return user

    def _require_role(self, expected_role):
        user = self._current_user()
        profile = (
            supabase.table("users")
            .select("role, username")
            .eq("id", user.id)
            .single()
            .execute()
        ).data

        if profile["role"] != expected_role:
            raise PermissionError(
                f"This action requires the {expected_role} role."
            )

        return user, profile

    def get_inventory(self):
        response = (
            supabase.table("kit_inventory")
            .select("*")
            .order("sport")
            .order("kit_type")
            .execute()
        )
        return response.data or []

    def get_my_requests(self):
        user, _ = self._require_role("player")

        response = (
            supabase.table("kit_requests")
            .select("*")
            .eq("player_id", user.id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data or []

    def submit_request(
        self, player_name, vit_name, sport, kit_type, quantity
    ):
        user, profile = self._require_role("player")

        player_name = player_name.strip()
        vit_name = vit_name.strip()
        sport = sport.strip()
        kit_type = kit_type.strip()

        if not all([player_name, vit_name, sport, kit_type]):
            raise ValueError("All fields are required.")

        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("Quantity must be at least one.")

        response = (
            supabase.table("kit_requests")
            .insert({
                "player_id": user.id,
                "player_name": player_name,
                "vit_name": vit_name,
                "sport": sport,
                "kit_type": kit_type,
                "quantity": quantity,
            })
            .execute()
        )

        if not response.data:
            raise RuntimeError("The kit request was not saved.")

        return response.data[0]

    def get_all_requests(self):
        self._require_role("organizer")

        response = (
            supabase.table("kit_requests")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return response.data or []

    def review_request(
        self,
        request_id,
        decision,
        message="",
        collection_at=None,
    ):
        self._require_role("organizer")

        allowed = {
            "Available for Collection",
            "Unavailable - Resubmit Tomorrow",
            "Fulfilled",
        }
        if decision not in allowed:
            raise ValueError("Invalid kit request decision.")

        current = (
            supabase.table("kit_requests")
            .select("*")
            .eq("id", request_id)
            .single()
            .execute()
        ).data

        if current["status"] == "Fulfilled":
            raise ValueError("This request has already been fulfilled.")

        payload = {
            "status": decision,
            "organizer_message": message.strip() or None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        if decision == "Available for Collection":
            if collection_at is None:
                raise ValueError(
                    "Choose a collection date and time."
                )

            if collection_at <= datetime.now():
                raise ValueError(
                    "Collection time must be in the future."
                )

            if current["status"] != "Available for Collection":
                # Find stock for the requested sport and kit type.
                inventory_response = (
                    supabase.table("kit_inventory")
                    .select("*")
                    .eq("sport", current["sport"])
                    .eq("kit_type", current["kit_type"])
                    .limit(1)
                    .execute()
                )
                inventory_rows = inventory_response.data or []

                if not inventory_rows:
                    raise ValueError(
                        "No matching inventory record exists."
                    )

                inventory = inventory_rows[0]
                available = int(inventory["available_quantity"])
                quantity = int(current["quantity"])

                if available < quantity:
                    raise ValueError(
                        f"Insufficient stock: {available} available, "
                        f"{quantity} requested."
                    )

                updated_inventory = (
                    supabase.table("kit_inventory")
                    .update({
                        "available_quantity": available - quantity,
                        "updated_at": datetime.now(
                            timezone.utc
                        ).isoformat(),
                    })
                    .eq("id", inventory["id"])
                    .eq("available_quantity", available)
                    .execute()
                )

                if not updated_inventory.data:
                    raise RuntimeError(
                        "Inventory changed during review. Refresh "
                        "and try again."
                    )

            payload["collection_at"] = (
                collection_at.astimezone(timezone.utc).isoformat()
            )
            payload["resubmit_after"] = None

        elif decision == "Unavailable - Resubmit Tomorrow":
            # This closes the current request; it does not delete it.
            payload["collection_at"] = None
            payload["resubmit_after"] = (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).isoformat()

        elif decision == "Fulfilled":
            if current["status"] != "Available for Collection":
                raise ValueError(
                    "Only requests approved for collection can "
                    "be marked fulfilled."
                )
            payload["fulfilled_at"] = (
                datetime.now(timezone.utc).isoformat()
            )

        response = (
            supabase.table("kit_requests")
            .update(payload)
            .eq("id", request_id)
            .execute()
        )

        if not response.data:
            raise RuntimeError("The kit request could not be updated.")

        return response.data[0]


    def set_inventory(self, sport, kit_type, quantity):
        self._require_role("organizer")

        sport = sport.strip()
        kit_type = kit_type.strip()
        quantity = int(quantity)

        if not sport or not kit_type:
            raise ValueError("Sport and kit type are required.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        response = (
            supabase.table("kit_inventory")
            .upsert(
                {
                    "sport": sport,
                    "kit_type": kit_type,
                    "available_quantity": quantity,
                    "updated_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                },
                on_conflict="sport,kit_type",
            )
            .execute()
        )

        if not response.data:
            raise RuntimeError("Inventory could not be saved.")

        return response.data[0]
