import json
import os

class KraftEventDB:
    def __init__(self, filename : str = 'kraft_teams.json'):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write('[]')
    
    def get_all(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data
        
    def insert_team(self, data: dict) -> dict:
        current_data = self.get_all()
        data['id'] = len(current_data) + 1
        current_data.append(data)
        with open(self.filename, 'w') as file:
            json.dump(current_data, file, indent=4)
        return data
    
    def add_bonus_points(self, team_id : int, points : int) -> dict:
        current_data = self.get_all()
        for item in current_data:
            if item['id'] == team_id:
                item['score'] += points
                with open(self.filename, 'w') as file:
                    json.dump(current_data, file, indent=4)
                return item
            
    def get_top_team(self) -> dict:
        current_data = self.get_all()
        highest_score = 0
        top_team = None
        for item in current_data:
            if item['score'] > highest_score:
                highest_score = item['score']
                top_team = item
        return top_team
    pass

# --- TEST SCRIPT ---
db = KraftEventDB()
print("1. Registering Teams...")
db.insert_team({"team_name": "AppBuilders", "tech_stack": "React Native", "score": 70})
db.insert_team({"team_name": "FastCoders", "tech_stack": "FastAPI", "score": 85})

print("\n2. Adding 20 bonus points to Team 1...")
db.add_bonus_points(1, 20)

print("\n3. Finding the winner:")
print(db.get_top_team()) # Should now be Team 1 (Score 90)!