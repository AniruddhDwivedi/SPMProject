class AuthService:
    def __init__(self):
        self.users = {
            "player": {
                "password": "player123",
                "role": "player",
                "name": "Demo Player",
            },
            "organizer": {
                "password": "organizer123",
                "role": "organizer",
                "name": "Demo Organizer",
            },
        }

    def login(self, username, password):
        user = self.users.get(username)

        if user and user["password"] == password:
            return {
                "username": username,
                "role": user["role"],
                "name": user["name"],
            }

        return None