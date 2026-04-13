# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app = FastAPI()

# users_db = {}

# @app.get("/api/v1/users/{user_id}")
# def get_user(user_id: str):
#     if user_id in users_db:
#         return users_db[user_id]
#     else:
#         raise HTTPException(status_code=404, detail = "User not found")

from fastapi import FastAPI, HTTPException

app = FastAPI()

users_db = {}

@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id : str):
    if user_id in users_db:
        del users_db[user_id]
        return {"message" : "User deleted!"}
    else:
        raise HTTPException(status_code=404, detail = "User not found")