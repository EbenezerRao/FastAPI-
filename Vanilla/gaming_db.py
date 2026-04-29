import os
import json

class GamingLeaderboardDB:
    def __init__(self, filename : str = 'leaderboard.json'):
        self.filename = filename
        if os.path.exists(filename) == False:
            with open(filename, 'w') as file:
                file.write('[]')
    
    def get_all(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data
        
    def insert_player(self, data: dict) -> dict:
        current_data = self.get_all()
        new_id = len(current_data) + 1
        data['id'] = new_id
        current_data.append(data)
        with open(self.filename, 'w') as file:
            json.dump(current_data, file, indent=4)
        return data

# 🔥 CHALLENGE 1: THE SORTER
    def get_top_players(self, limit: int) -> list:
        current_data = self.get_all()
        
        # We sort the list of dictionaries DIRECTLY. 
        # lambda x: x['score'] tells Python "Look inside the dictionary to find the number to sort by"
        current_data.sort(key=lambda x: x['score'], reverse=True)
        
        # Return the sliced list
        return current_data[:limit]
    
    # 🔥 CHALLENGE 2: THE SEASON RESET
    def reset_season(self) -> int:
        current_data = self.get_all()
        
        # 1. Create a safe new list to hold the players we are keeping
        survivors = []
        
        # 2. Loop through the old data
        for player in current_data:
            if player['active'] == True:
                player['score'] = 0         # Reset their score
                survivors.append(player)    # Save them to the new list
            # Notice we do nothing if they are False. They just get left behind!

        # 3. SAVE OUTSIDE THE LOOP! Overwrite the hard drive with the survivors list.
        with open(self.filename, 'w') as file:
            json.dump(survivors, file, indent=4)
            
        # 4. Return the total count of survivors
        return len(survivors)

# --- TEST SCRIPT ---
db = GamingLeaderboardDB()

print("1. Registering Players...")
db.insert_player({"player_alias": "NoobMaster69", "score": 1200, "active": False})
db.insert_player({"player_alias": "GamerDudeEBBY", "score": 8500, "active": True})
db.insert_player({"player_alias": "Steve", "score": 3400, "active": True})
db.insert_player({"player_alias": "Alex", "score": 9999, "active": True})

print("\n2. Getting Top 2 Players:")
# Should print Alex (9999) and GamerDudeEBBY (8500)
top_2 = db.get_top_players(2)
for p in top_2:
    print(f"{p['player_alias']}: {p['score']}")

print("\n3. Triggering Season Reset...")
# Should delete NoobMaster69 and set everyone else to 0!
survivors_count = db.reset_season()
print(f"Season reset! {survivors_count} players remain active.")

print("\n4. Final Hard Drive State:")
print(db.get_all())