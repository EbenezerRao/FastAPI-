from passlib.context import CryptContext

psd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password : str):
    return psd_context.hash(password)

def verify_pswd(plain_pswd : str, hashed_pswd : str):
    return psd_context.verify(plain_pswd, hashed_pswd)

# --- THE TEST ZONE ---
if __name__ == "__main__":
    test_password = "AsherAdmin2026!"
    scrambled_hash = get_password_hash(test_password)
    
    print(f"Original Password: {test_password}")
    print(f"Scrambled Hash: {scrambled_hash}")
    
    # Let's test if our verifier works
    is_correct = verify_pswd("AsherAdmin2026!", scrambled_hash)
    print(f"Does the password match the hash? {is_correct}")