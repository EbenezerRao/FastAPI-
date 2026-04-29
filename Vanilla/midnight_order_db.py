import json
import os

class MidnightOrderDB:
    def __init__(self, filename : str = 'midnight_order.json'):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write("[]")

    def get_all(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data
        
    # def insert_data(self, filename : str, data : dict) -> dict:
    #     current_data = self.get_all()
    #     new_id = len(current_data) + 1
    #     data['id'] = new_id
    #     current_data.append(new_id)
    #     with open(self.filename, 'w') as file:
    #         data = json.load(current_data, file, indent = 4)
    #         return data

    # 🔥 CHALLENGE 1: THE BOUNCER
    def safe_insert(self, data: dict) -> bool:
        # 1. Check if "restaurant" AND "item" are keys inside the 'data' dictionary.
        # (Hint: use `if "restaurant" not in data or "item" not in data:`)
        # 2. If they are missing, return False immediately.
        # 3. If they exist, do the normal insert logic (assign ID, append, dump) and return True.
        if 'restaurant' not in data or 'item' not in data:
            return False
        else:
            current_data = self.get_all()
            new_id = len(current_data) + 1
            data['id'] = new_id
            current_data.append(data)
            with open(self.filename, 'w') as file:
                json.dump(current_data, file, indent=4)
            return True

    # 🔥 CHALLENGE 2: THE MULTI-FILTER
    def get_pending_from(self, restaurant_name: str) -> list:
        # 1. Load data
        # 2. Create an empty list for matches
        # 3. Loop through data. If the order's restaurant == restaurant_name AND delivered == False:
        # 4. Append to matches
        # 5. Return matches
        current_data = self.get_all()
        matches = []
        for item in current_data:
            if restaurant_name == item['restaurant'] and item['delivered'] == False:
                matches.append(item)
        return matches
        pass
# --- TEST SCRIPT ---
db = MidnightOrderDB()

print("1. Testing Bouncer (Safe Insert)...")
# Should return False and NOT save to disk!
print("Bad Data Insert:", db.safe_insert({"restaurant": "Burger Singh"})) 
# Should return True and save!
print("Good Data Insert:", db.safe_insert({"restaurant": "Biryani Bees", "item": "Chicken Biryani", "delivered": False}))
db.safe_insert({"restaurant": "Biryani Bees", "item": "Mutton Masala", "delivered": True})

print("\n2. Finding pending orders from Biryani Bees...")
# Should ONLY print the Chicken Biryani, because the Mutton Masala is delivered=True!
print(db.get_pending_from("Biryani Bees"))