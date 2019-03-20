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
    
    def use(self, itemEntity, **kwargs):
        results = []

        itemComponent = itemEntity.item

        if itemComponent.useFunction is None:
            results.append({
                            'message': Message('The {} cannot be used'.format(itemEntity.name), tcod.yellow)
                           })
        else:
            kwargs = {**itemComponent.functionKwargs, **kwargs}
            itemUseResults = itemComponent.useFunction(self.owner, **kwargs)

            for itemUseResult in itemUseResults:
                if itemUseResult.get('consumed'):
                    self.removeItem(itemEntity)
            
            results.extend(itemUseResults)

        return results
    
    def removeItem(self, item):
        self.items.remove(item)