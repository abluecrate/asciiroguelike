import tcod
from gameMessages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def addItem(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'itemAdded': None,
                'message': Message('You cannot carry any more. Your inventory is full', tcod.yellow)
            })
        else:
            results.append({
                'itemAdded': item,
                'message': Message('You pick up the {}'.format(item.name), tcod.light_blue)
            })
        
            self.items.append(item)
        
        return results