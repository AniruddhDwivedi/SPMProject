from src.services.supabase_client import supabase
from src.models.user import User


class AuthService:

    def login(self, email, password):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })

            auth_user = response.user

            if auth_user is None:
                print("AUTH: No user returned")
                return None

            print("AUTH: Login successful")
            print("AUTH USER ID:", auth_user.id)
            print("AUTH EMAIL:", auth_user.email)

            profile_response = (
                supabase
                .table("users")
                .select("id, username, role")
                .eq("id", auth_user.id)
                .single()
                .execute()
            )

            profile = profile_response.data

            print("PROFILE:", profile)

            if profile is None:
                print("AUTH: No profile found")
                return None

            return User(
                username=profile["username"],
                role=profile["role"],
            )

        except Exception as e:
            print("AUTH ERROR:", repr(e))
            return None