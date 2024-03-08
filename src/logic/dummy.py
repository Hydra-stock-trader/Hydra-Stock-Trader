from src.models.models import  Item


def get_item(item_id: int):
    item = Item(id=item_id, name="Sample Item", description="This is a sample item", price=9.99)
    return item