from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class Message(BaseModel):
    message: str


ITEMS: dict[int, Item] = {
    1: Item(id=1, name="Item 1", description="First item"),
    2: Item(id=2, name="Item 2", description="Second item"),
    3: Item(id=3, name="Item 3", description=None),
}

_next_id = 4


@app.get("/items")
def list_items() -> list[Item]:
    return list(ITEMS.values())


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    return ITEMS[item_id]


@app.post("/items", status_code=201)
def create_item(body: ItemCreate) -> Item:
    global _next_id
    item = Item(id=_next_id, name=body.name, description=body.description)
    ITEMS[_next_id] = item
    _next_id += 1
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, body: ItemUpdate) -> Item:
    item = ITEMS[item_id]
    if body.name is not None:
        item = item.model_copy(update={"name": body.name})
    if body.description is not None:
        item = item.model_copy(update={"description": body.description})
    ITEMS[item_id] = item
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> Message:
    del ITEMS[item_id]
    return Message(message="Deleted")
