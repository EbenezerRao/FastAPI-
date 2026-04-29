import os
import json

class JSONDatabase:
    def __init__(self, filename: str):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                file.write("[]")

    def get_all(self) -> list:
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data
        
    def insert(self, data: dict) -> dict:
        current_data = self.get_all()
        new_id = len(current_data) + 1  
        data['id'] = new_id
        current_data.append(data)
        with open(self.filename, 'w') as file:
            json.dump(current_data, file, indent=4)

        return data

db = JSONDatabase("hackers.json")

print("Adding hackers to the hard drive...")
db.insert({"name": "Neo", "skill": "Python"})
db.insert({"name": "Trinity", "skill": "FastAPI"})

print("\nReading from the hard drive:")
print(db.get_all())