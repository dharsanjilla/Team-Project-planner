# Team Project Planner

## Overview

The Team Project Planner is a tool designed to manage users, teams, and project boards with tasks. It provides a set of APIs to handle the creation, updating, and management of these entities, and it uses local file storage for persistence.

## Features

- **User Management**
  - Create, update, and list users
  - Describe a user
  - Get a user's teams

- **Team Management**
  - Create, update, and list teams
  - Describe a team
  - Add and remove users from a team
  - List users of a team

- **Project Board Management**
  - Create and close project boards
  - Add tasks to boards
  - Update the status of tasks
  - List open boards for a team
  - Export board data to a text file

## Directory Structure

team_project_planner/
├── base_classes/
│ ├── project_board_base.py
│ ├── team_base.py
│ └── user_base.py
├── concrete_implementation/
│ ├── project_board_manager.py
│ ├── team_manager.py
│ └── user_manager.py
├── db/
│ ├── boards.json
│ ├── teams.json
│ └── users.json
├── out/
├── requirements.txt
└── README.md

bash
Copy code

## Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/team_project_planner.git
   cd team_project_planner
Install dependencies

Make sure you have pip installed and run:

bash
Copy code
pip install -r requirements.txt
Run the application

You can use the provided classes to create and manage users, teams, and project boards. Here is an example script to test the ProjectBoardManager:

python
Copy code
from concrete_implementation.project_board_manager import ProjectBoardManager
import json
import datetime

pbm = ProjectBoardManager()

# Create a board
create_board_request = json.dumps({
    "name": "Sprint 1",
    "description": "First sprint board",
    "team_id": 1,
    "creation_time": datetime.datetime.now().isoformat()
})
print(pbm.create_board(create_board_request))

# Add a task to the board
add_task_request = json.dumps({
    "title": "Design database schema",
    "description": "Design the initial database schema for the project",
    "user_id": 1,
    "board_id": 1,
    "creation_time": datetime.datetime.now().isoformat()
})
print(pbm.add_task(add_task_request))

# Export the board to a text file
export_board_request = json.dumps({
    "id": 1
})
print(pbm.export_board(export_board_request))
Persisting Data

The application uses JSON files for persistence. The db folder contains these files:

users.json: Stores user data
teams.json: Stores team data
boards.json: Stores project board and task data
Ensure that these files are present in the db directory. If not, you can create them with an empty JSON array ([]) as the content.

