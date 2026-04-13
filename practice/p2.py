from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import uuid

app = FastAPI()

gigs_db = {}

class GigCreate(BaseModel):
    title : str
    campus_location : str
    payout_ruppees : int

@app.post('/api/v1/gigs')
def gig_create(gig_data : GigCreate): # <--- Named the incoming data 'gig_data'
    
    generated_id = str(uuid.uuid4())[:6] # <--- Named the UUID 'generated_id'
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    gigs_db[generated_id] = {
        'title' : gig_data.title,
        'campus_location' : gig_data.campus_location,
        'payout_ruppees' : gig_data.payout_ruppees,
        'created_at' : time_stamp  # <--- Don't forget to save the timestamp!
    }
    
    return {"message" : "Gig created!", "gig_id" : generated_id}

@app.get('/api/v1/gigs/{gig_id}')
def get_gig(gig_id : str):
    if gig_id in gigs_db:
        return gigs_db[gig_id]
    else:
        raise HTTPException(status_code=404, detail= "Gig not found")
    
@app.delete('/api/v1/gigs/{gig_id}')
def delete_gig(gig_id : str):
    if gig_id in gigs_db:
        del gigs_db[gig_id]
        return {"message" : "Gig deleted!"}
    else:
        raise HTTPException(status_code=404, detail= "Gig not found")