# main.py
from fastapi import FastAPI

# 1. Create a FastAPI instance
app = FastAPI()

# 2. Define a path operation (a route)
@app.get("/")
async def read_root():
    """
    This is the root endpoint.
    It returns a simple greeting.
    """
    return {"message": "Hello, FastAPI!"}

# 3. Define another path operation with a path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """
    This endpoint takes an item_id as a path parameter
    and an optional query parameter 'q'.
    """
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# 4. Define a POST request with a Pydantic model for request body
import json
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    """
    This endpoint accepts an Item object in the request body.
    """
    return {"message": "Item created successfully", "item": item}

@app.post("/commands/")
async def create_command(color_code: str):
    data = {
        "command": "change",
        "color": color_code
    }
    with open("command.json", "w") as f:
        json.dump(data, f, indent=4)
    return {"message": "Command file created successfully", "data": data}
