import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

market_db = {}

class MarketItem(BaseModel):
    item_name : str
    price_ruppess : int
    is_sold : bool

@app.post('/api/v1/items')
def post_items(item: MarketItem):
    item_id = str(uuid.uuid4())[:6]
    market_db[item_id] = {
        "name of the item" : item.item_name,
        'price (in ruppess)' : item.price_ruppess,
        'is the item sold' : item.is_sold
    }
    return {
        'message' : 'Item successfully added to the market!',
        'item_id' : item_id
    }

@app.get('/api/v1/items/{item_id}')
def get_item(item_id : str):
    if item_id not in market_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return market_db[item_id]

@app.put('/api/v1/items/{item_id}/buy')
def buy_item(item_id : str):
    if item_id not in market_db:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        market_db[item_id]['is the item sold'] = True
        return {
            "message" : f"{market_db[item_id]['name of the item']} has been sold!"
        }

@app.delete('/api/v1/items/{item_id}')
def delete_item(item_id : str):
    if item_id not in market_db:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        del market_db[item_id]
        return {
            'message' : 'Item successfully deleted from the market!'
        }
