from passlib.context import CryptContext

pswd = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str):
    return pswd.hash(password)

def update_password(old_password_attempt: str, new_password: str, current_db_hash: str):
    if not pswd.verify(old_password_attempt, current_db_hash):
        raise ValueError("Old password does not match")
    else:
        new_pswd = pswd.hash(new_password)
        return new_pswd
    pass 
if __name__ == "__main__":
    print("--- ASHER PORTAL SECURE LOGIN ---")
    fake_db = {}

    # 1. Registration Phase
    print("\n[Register]")
    new_user = input("Choose a username: ")
    new_pass = input("Choose a password: ")

    fake_db[new_user] = pswd.hash(new_pass)
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
        if pswd.verify(login_pass, stored_hash):
            print("Access Granted: Welcome to the Asher Portal!")
        else:
            print("Access Denied: Incorrect Password.")