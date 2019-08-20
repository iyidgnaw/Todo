from TodoItem import TodoItem
from TodoExceptions import ItemIdNotFoundError

class TodoList(object):
    '''todo list: the container for several items'''
    def __init__(self, name):
        self._listOfThings = []
        self.name = name

    def getName(self):
        return self.name

    def create(self, content):
        newItem = TodoItem(content)
        self._listOfThings.append(newItem)

    def delete(self, itemId):
        if int(itemId) > self.getListLen():
            raise ItemIdNotFoundError
        self._listOfThings.pop(int(itemId)-1)

    def get(self):
        for itemId, item in enumerate(self._listOfThings):
            print('{}. {}'.format(str(itemId+1), item.getContent()))

    def getListLen(self):
        return len(self._listOfThings)

    def update(self, name):
        self.name = name