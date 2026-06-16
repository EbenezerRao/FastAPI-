# from passlib.context import CryptContext

# pswd = CryptContext(schemes=['bcrypt'], deprecated='auto')

# def verify_password_strength(password : str):
#     if len(password) < 8:
#         raise ValueError("Password must be at least 8 characters long")
#     elif not any (char.isdigit() for char in password):
#         raise ValueError("Password must contain at least one number")
#     else:
#         return True

# # --- TEST IT ---
# # verify_password_strength("weak")       # Should crash with ValueError
# # verify_password_strength("NoNumbersHere") # Should crash with ValueError
# verify_password_strength("AsherAdmin2026") # Should return True

def verify_username(username: str):
    banned_words = ["admin", "root", "system", "staff"]
    if any (banned_word in username.lower() for banned_word in banned_words):
        raise ValueError("Username cannot contain banned words")
    pass

# --- TEST IT ---
# verify_username("ebenezer_dev")      # Should return True
# verify_username("AsherAdMiN2026")    # Should crash with ValueError
# verify_username("system_manager")    # Should crash with ValueError