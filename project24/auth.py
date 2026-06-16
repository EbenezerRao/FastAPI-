from passlib.context import CryptContext

pswd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password : str):
    return pswd.hash(password)

# ... (keep your get_password_hash and update_password functions at the top)

if __name__ == "__main__":
    print("--- ASHER PORTAL SECURE LOGIN ---")
    fake_db = {}

    # 1. Registration Phase
    print("\n[Register]")
    new_user = input("Choose a username: ")
    new_pass = input("Choose a password: ")

    # Hash it and save to our fake database dictionary
    fake_db[new_user] = get_password_hash(new_pass)
    print("Registration Successful! Hash saved to DB.")

    # 2. Login Phase
    print("\n[Login]")
    login_user = input("Enter username: ")
    login_pass = input("Enter password: ")

    # 3. The Auth Logic
    if login_user not in fake_db:
        print("Access Denied: User not found.")
    else:
        # Grab the hash from the database
        stored_hash = fake_db[login_user]
        
        # Verify the typed password against the stored hash
        # (Using the 'pswd' CryptContext you defined earlier)
        if pswd.verify(login_pass, stored_hash):
            print("Access Granted: Welcome to the Asher Portal!")
        else:
            print("Access Denied: Incorrect Password.")