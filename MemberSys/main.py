from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()


class Item(BaseModel):
    '''
    Item Model
    
    Attributes:
        name (str): Item name
        price (float): Item price
        is_offer (Union[bool, None]): Item offer    

    '''

    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id} 

@app.get("/items/{item_id}/time")
def get_time():
    return {"time": datetime.now()}