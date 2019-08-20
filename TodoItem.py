
class TodoItem(object):
    '''todo thing'''
    def __init__(self, content):
        self._content = content

    def getContent(self):
        return self._content


