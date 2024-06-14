import json
import os
from datetime import datetime
from base_classes.team_base import TeamBase

class TeamManager(TeamBase):
    def __init__(self):
        self.teams_file = "db/teams.json"
        self.users_file = "db/users.json"
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.teams_file):
            self.teams = []
            self.save_data()
        else:
            with open(self.teams_file, 'r') as file:
                self.teams = json.load(file)

        if not os.path.exists(self.users_file):
            self.users = []
            self.save_users()
        else:
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)

    def save_data(self):
        with open(self.teams_file, 'w') as file:
            json.dump(self.teams, file, indent=4)

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def create_team(self, request: str) -> str:
        team_data = json.loads(request)
        if len(team_data['name']) > 64 or len(team_data['description']) > 128:
            raise ValueError("Name or description exceeds maximum length")
        if any(team['name'] == team_data['name'] for team in self.teams):
            raise ValueError("Team name must be unique")
        if not any(user['id'] == team_data['admin'] for user in self.users):
            raise ValueError("Admin user does not exist")

        team_id = len(self.teams) + 1
        team = {
            "id": team_id,
            "name": team_data['name'],
            "description": team_data['description'],
            "creation_time": datetime.now().isoformat(),
            "admin": team_data['admin'],
            "users": [team_data['admin']]
        }
        self.teams.append(team)
        self.save_data()
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        return json.dumps(self.teams, indent=4)

    def describe_team(self, request: str) -> str:
        team_id = json.loads(request)['id']
        for team in self.teams:
            if team['id'] == team_id:
                return json.dumps(team, indent=4)
        raise ValueError("Team not found")

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data['id']
        team_data = data['team']
        
        for team in self.teams:
            if team['id'] == team_id:
                if 'name' in team_data:
                    if len(team_data['name']) > 64:
                        raise ValueError("Name exceeds maximum length")
                    if any(t['name'] == team_data['name'] for t in self.teams if t['id'] != team_id):
                        raise ValueError("Team name must be unique")
                    team['name'] = team_data['name']
                if 'description' in team_data:
                    if len(team_data['description']) > 128:
                        raise ValueError("Description exceeds maximum length")
                    team['description'] = team_data['description']
                if 'admin' in team_data:
                    if not any(user['id'] == team_data['admin'] for user in self.users):
                        raise ValueError("Admin user does not exist")
                    team['admin'] = team_data['admin']
                self.save_data()
                return json.dumps({"status": "success"})
        raise ValueError("Team not found")

    def add_users_to_team(self, request: str):
        data = json.loads(request)
        team_id = data['id']
        users = data['users']
        
        for team in self.teams:
            if team['id'] == team_id:
                if len(team['users']) + len(users) > 50:
                    raise ValueError("Cannot add more than 50 users to a team")
                for user_id in users:
                    if not any(user['id'] == user_id for user in self.users):
                        raise ValueError(f"User {user_id} does not exist")
                    if user_id not in team['users']:
                        team['users'].append(user_id)
                self.save_data()
                return json.dumps({"status": "success"})
        raise ValueError("Team not found")

    def remove_users_from_team(self, request: str):
        data = json.loads(request)
        team_id = data['id']
        users = data['users']
        
        for team in self.teams:
            if team['id'] == team_id:
                for user_id in users:
                    if user_id in team['users']:
                        team['users'].remove(user_id)
                self.save_data()
                return json.dumps({"status": "success"})
        raise ValueError("Team not found")

    def list_team_users(self, request: str) -> str:
        team_id = json.loads(request)['id']
        
        for team in self.teams:
            if team['id'] == team_id:
                team_users = [
                    {
                        "id": user['id'],
                        "name": user['name'],
                        "display_name": user['display_name']
                    }
                    for user in self.users if user['id'] in team['users']
                ]
                return json.dumps(team_users, indent=4)
        raise ValueError("Team not found")
