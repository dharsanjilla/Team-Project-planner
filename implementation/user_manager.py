import json
import os
from datetime import datetime
from base_classes.user_base import UserBase

class UserManager(UserBase):
    def __init__(self):
        self.users_file = "db/users.json"
        self.teams_file = "db/teams.json"
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.users_file):
            self.users = []
            self.save_data()
        else:
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)

        if not os.path.exists(self.teams_file):
            self.teams = []
        else:
            with open(self.teams_file, 'r') as file:
                self.teams = json.load(file)

    def save_data(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def create_user(self, request: str) -> str:
        user_data = json.loads(request)
        if len(user_data['name']) > 64 or len(user_data['display_name']) > 64:
            raise ValueError("Name or display name exceeds maximum length")
        if any(user['name'] == user_data['name'] for user in self.users):
            raise ValueError("User name must be unique")

        user_id = len(self.users) + 1
        user = {
            "id": user_id,
            "name": user_data['name'],
            "display_name": user_data['display_name'],
            "creation_time": datetime.now().isoformat()
        }
        self.users.append(user)
        self.save_data()
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        return json.dumps(self.users, indent=4)

    def describe_user(self, request: str) -> str:
        user_id = json.loads(request)['id']
        for user in self.users:
            if user['id'] == user_id:
                return json.dumps(user, indent=4)
        raise ValueError("User not found")

    def update_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data['id']
        user_data = data['user']
        
        for user in self.users:
            if user['id'] == user_id:
                if 'display_name' in user_data:
                    if len(user_data['display_name']) > 64:
                        raise ValueError("Display name exceeds maximum length")
                    user['display_name'] = user_data['display_name']
                self.save_data()
                return json.dumps({"status": "success"})
        raise ValueError("User not found")

    def get_user_teams(self, request: str) -> str:
        user_id = json.loads(request)['id']
        user_teams = [
            {
                "name": team['name'],
                "description": team['description'],
                "creation_time": team['creation_time']
            }
            for team in self.teams if user_id in team['users']
        ]
        return json.dumps(user_teams, indent=4)
    
    