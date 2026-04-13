# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import uuid

# app = FastAPI()

# lib_db = {}

# class BookCreate(BaseModel):
#     title : str
#     author : str
#     is_available : bool

# @app.post('/api/v1/books')
# def book_create(book_data : BookCreate):
#     book_id = str(uuid.uuid4())[:6]
#     lib_db[book_id] = {
#         'title' : book_data.title,
#         'author' : book_data.author,
#         'is_available' : book_data.is_available
#     }
#     return {'message' : "Book added to library!", "book_id" : book_id}

# @app.get('/api/v1/books/{book_id}')
# def get_book(book_id : str):
#     if book_id in lib_db:
#         return lib_db[book_id]
#     else:
#         raise HTTPException(status_code=404, detail= "Book not found")

# @app.put('/api/v1/books/{book_id}/checkout')
# def checkout_book(book_id : str):
#     if book_id in lib_db:
#         lib_db[book_id]['is_available'] = False
#         return {"message" : "Book checked out!"}
#     else:
#         raise HTTPException(status_code=404, detail= "Book not found")




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import uuid

# app = FastAPI()

# order_queue = {}

# class Order(BaseModel):
#     customer_name : str
#     drink_type : str
#     size : str

# @app.post('/api/v1/orders')
# def create_order(order_data : Order):
#     order_id = str(uuid.uuid4())[:6]
#     order_queue[order_id] = {
#         'customer_name' : order_data.customer_name,
#         'drink-type' : order_data.drink_type,
#         'size' : order_data.size
#     }
#     return {'message' : 'Order Created for ' + order_data.customer_name, 'order_id' : order_id  }

# @app.get('/api/v1/orders')
# def get_orders():
#     if len(order_queue) == 0:
#         raise HTTPException(status_code=404, detail= "No orders found")
#     else:
#         return {'total_orders' : len(order_queue), 'orders' : order_queue}


# @app.delete('/api/v1/orders/{order_id}')
# def delete_order(order_id : str):
#     if order_id in order_queue:
#         del order_queue[order_id]
#         return {'message' : 'Order ' + order_id + ' deleted'}
#     else:
#         raise HTTPException(status_code=404, detail= "Order not found")


