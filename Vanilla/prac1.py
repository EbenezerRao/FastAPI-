import os
import json

class UsherDB:
    def __init__(self,  filename : str = 'usher_clients.json'):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write("[]")

    def get_all(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data
        
    def insert_client(self, data : dict) -> dict:
        current_data = self.get_all()
        new_id = len(current_data) + 1
        data['id'] = new_id
        current_data.append(data)
        with open(self.filename, 'w') as file:
            json.dump(current_data, file, indent=4)
        return data
    
    def get_by_status(self, status : str) -> list:
        data = self.get_all()
        filterd_data = []
        for item in data:
            if item['status'] == status:
                filterd_data.append(item)
        return filterd_data
    
    def delete_client(self, client_id : int) -> bool:
        current_data = self.get_all()
        for item in current_data:
            if item['id'] == client_id:
                current_data.remove(item)
                with open(self.filename, 'w') as file:
                    json.dump(current_data, file, indent=4)
                return True
            
db = UsherDB()

print("1. Adding USHER clients...")
db.insert_client({"client": "Local Cafe", "deliverable": "Logo Rebrand", "status": "Pending"})
db.insert_client({"client": "Startup X", "deliverable": "Figma Mockup", "status": "In Progress"})
db.insert_client({"client": "DevFest", "deliverable": "T-shirt Design", "status": "Pending"})

print("\n2. Finding all 'Pending' projects:")
# Should print Local Cafe and DevFest!
print(db.get_by_status("Pending"))

print("\n3. Deleting Client #1 (Local Cafe)...")
db.delete_client(1)

print("\n4. Final Hard Drive State:")
print(db.get_all())