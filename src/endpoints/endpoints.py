from fastapi import APIRouter
from models.models import  Item
from logic.dummy import get_item

router = APIRouter()

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = get_item(item_id)
    return item