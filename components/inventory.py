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
                            'message': Message('Inventory is Full', tcod.yellow)
                           })
        else:
            results.append({
                            'itemAdded': item,
                            'message': Message('You picked up {}'.format(item.name), tcod.blue)
                           })    
            self.items.append(item)
        return results