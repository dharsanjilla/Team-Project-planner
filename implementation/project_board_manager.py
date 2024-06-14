import json
import os
import datetime
from base_classes.project_board_base import ProjectBoardBase
from base_classes.team_base import TeamBase
from base_classes.user_base import UserBase

class ProjectBoardManager(ProjectBoardBase):
    def __init__(self, db_path='db/boards.json'):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as file:
                json.dump([], file)
    
    def create_board(self, request: str):
        boards = self._load_boards()
        board = json.loads(request)
        
        # Validate constraints
        if any(b['name'] == board['name'] and b['team_id'] == board['team_id'] for b in boards):
            raise ValueError("Board name must be unique for a team.")
        if len(board['name']) > 64:
            raise ValueError("Board name can be max 64 characters.")
        if len(board['description']) > 128:
            raise ValueError("Description can be max 128 characters.")
        
        # Assign an ID and creation time
        board_id = len(boards) + 1
        board['id'] = board_id
        board['status'] = "OPEN"
        board['tasks'] = []
        
        boards.append(board)
        self._save_boards(boards)
        return json.dumps({"id": board_id})
    
    def close_board(self, request: str) -> str:
        boards = self._load_boards()
        board_id = json.loads(request)['id']
        
        for board in boards:
            if board['id'] == board_id:
                if all(task['status'] == 'COMPLETE' for task in board['tasks']):
                    board['status'] = "CLOSED"
                    board['end_time'] = datetime.datetime.now().isoformat()
                    self._save_boards(boards)
                    return json.dumps({"status": "Board closed"})
                else:
                    raise ValueError("Cannot close board with incomplete tasks.")
        raise ValueError("Board not found.")
    
    def add_task(self, request: str) -> str:
        boards = self._load_boards()
        task = json.loads(request)
        board_id = task.pop('board_id')
        
        # Validate constraints
        for board in boards:
            if board['id'] == board_id:
                if board['status'] != 'OPEN':
                    raise ValueError("Can only add tasks to an open board.")
                if any(t['title'] == task['title'] for t in board['tasks']):
                    raise ValueError("Task title must be unique for a board.")
                if len(task['title']) > 64:
                    raise ValueError("Title name can be max 64 characters.")
                if len(task['description']) > 128:
                    raise ValueError("Description can be max 128 characters.")
                
                # Assign an ID and creation time
                task_id = len(board['tasks']) + 1
                task['id'] = task_id
                task['status'] = "OPEN"
                task['creation_time'] = datetime.datetime.now().isoformat()
                
                board['tasks'].append(task)
                self._save_boards(boards)
                return json.dumps({"id": task_id})
        
        raise ValueError("Board not found.")
    
    def update_task_status(self, request: str):
        boards = self._load_boards()
        task_update = json.loads(request)
        task_id = task_update['id']
        new_status = task_update['status']
        
        for board in boards:
            for task in board['tasks']:
                if task['id'] == task_id:
                    task['status'] = new_status
                    self._save_boards(boards)
                    return json.dumps({"status": "Task updated"})
        
        raise ValueError("Task not found.")
    
    def list_boards(self, request: str) -> str:
        boards = self._load_boards()
        team_id = json.loads(request)['id']
        
        open_boards = [board for board in boards if board['team_id'] == team_id and board['status'] == 'OPEN']
        return json.dumps(open_boards)
    
    def export_board(self, request: str) -> str:
        boards = self._load_boards()
        board_id = json.loads(request)['id']
        
        for board in boards:
            if board['id'] == board_id:
                out_file = f'out/board_{board_id}.txt'
                with open(out_file, 'w') as file:
                    file.write(f"Board Name: {board['name']}\n")
                    file.write(f"Description: {board['description']}\n")
                    file.write(f"Team ID: {board['team_id']}\n")
                    file.write(f"Creation Time: {board['creation_time']}\n")
                    file.write(f"Status: {board['status']}\n")
                    if board['status'] == 'CLOSED':
                        file.write(f"End Time: {board['end_time']}\n")
                    file.write("Tasks:\n")
                    for task in board['tasks']:
                        file.write(f"  Task ID: {task['id']}\n")
                        file.write(f"  Title: {task['title']}\n")
                        file.write(f"  Description: {task['description']}\n")
                        file.write(f"  Assigned User ID: {task['user_id']}\n")
                        file.write(f"  Creation Time: {task['creation_time']}\n")
                        file.write(f"  Status: {task['status']}\n")
                        file.write("\n")
                return json.dumps({"out_file": out_file})
        
        raise ValueError("Board not found.")
    
    def _load_boards(self):
        with open(self.db_path, 'r') as file:
            return json.load(file)
    
    def _save_boards(self, boards):
        with open(self.db_path, 'w') as file:
            json.dump(boards, file, indent=4)

if not os.path.exists('out'):
    os.makedirs('out')

if __name__ == '__main__':
    project_board_manager = ProjectBoardManager()
    print(project_board_manager.create_board('{"name": "Board 1", "description": "First board", "team_id": 1}'))
    print(project_board_manager.create_board('{"name": "Board 2", "description": "Second board", "team_id": 1}'))
    print(project_board_manager.create_board('{"name": "Board 3", "description": "Third board", "team_id": 2}'))
    print(project_board_manager.list_boards('{"id": 1}'))
    print(project_board_manager.add_task('{"title": "Task 1", "description": "First task", "board_id": 1, "user_id": 1}'))
    print(project_board_manager.add_task('{"title": "Task 2", "description": "Second task", "board_id": 1, "user_id": 2}'))
    print(project_board_manager.add_task('{"title": "Task 3", "description": "Third task", "board_id": 2, "user_id": 1}'))
    print(project_board_manager.update_task_status('{"id": 1, "status": "COMPLETE"}'))
    print(project_board_manager.list_boards('{"id": 1}'))
    print(project_board_manager.export_board('{"id": 1}'))
    print(project_board_manager.close_board('{"id": 1}'))
    print(project_board_manager.list_boards('{"id": 1}'))
    print(project_board_manager.list_boards('{"id": 2}'))
    print(project_board_manager.list_boards('{"id": 3}'))
