#! /usr/local/bin/python3
'''Main module of my Todo app'''

import os
import pickle
import signal
import sys

CACHE = os.getcwd() + '/appCache'
HELP_MSG = 'User Commands:\n\
        show: show the things in current list.\n\
        listall: show available lists in app.\n\
        add [content]: add a new task to current list.\n\
        delete [task_id]: delete a task from current list with an id.\n\
        abort [list_name]: abort the current list.\n\
        new [list_name]: create a new list with given name.\n\
        use [list_name]: switch to specific list with given name.\n\
        exit: save the exit the app.'


class TodoApp(object):
    '''todo application main class'''
    def __init__(self):
        self._registered = {'Default': toDoList()}
        self._using = 'Default'
        print('This is the init')
        self.showAllThing()

    def addThing(self, content):
        if not type(content) is str: 
            raise ValueError('Check your content please')
        if not content:
            raise ValueError('Empty content is not allowed')
        currentList = self._getCurrentList()
        currentList.addThing(content)

    def _getCurrentList(self):
        return self._registered[self._using]

    def createList(self, nameOfList):
        if not type(nameOfList) is str: 
            raise ValueError('Given name is not support')
        if not nameOfList:
            raise ValueError('List name is required')
        if nameOfList in self._registered:
            raise ValueError('List exist')
        self._registered[nameOfList] = toDoList()
        self.useList(nameOfList)

    def showAllThing(self):
        print('Current List: {}'.format(self._using))
        currentList = self._registered[self._using]
        currentList.printList()

    def showAllList(self):
        for name in self._registered:
            print(name)

    def deleteThing(self, t_id):
        currentList = self._getCurrentList()
        currentList.deleteThing(t_id)

    def deleteList(self, nameOfList):
        if not type(nameOfList) is str: 
            raise ValueError('Given name is not support')
        if nameOfList not in self._registered:
            raise ValueError('Given list name not found')
        if nameOfList == 'Default':
            raise ValueError('Cannot delete default list')
        if nameOfList == self._using:
            self.useList('Default')
        self._registered.pop(nameOfList, None)

    def useList(self, nameOfList):
        if not type(nameOfList) is str: 
            raise ValueError('Given name is not support')
        if nameOfList not in self._registered:
            raise ValueError('Given list name not found')
        self._using = nameOfList
        print('Using {}'.format(nameOfList))

    # TODO: Edit Thing
    def editThing(self):
        pass

    # TODO: Rename List
    def renameList(self):
        pass

    def main(self, todo_args):
        supportCmd = {
                'show': lambda args: self.showAllThing(),
                'listall': lambda args: self.showAllList(),
                'add': self.addThing,
                'delete': self.deleteThing,
                'abort': self.deleteList,
                'new': self.createList,
                'use': self.useList,
                'exit': lambda args: self.exit()
                }
        if not todo_args:
            self.showAllThing()

        elif todo_args[0] in ('-i', '--interactive'):
            while 1:
                args = input('\n>').strip().split(' ')
                if not args or not args[0]:
                    print(HELP_MSG)
                    continue
                cmd = args.pop(0)
                if cmd not in supportCmd:
                    print('Unknown commands!')
                    print(HELP_MSG)
                    continue
                try:
                    supportCmd.get(cmd, lambda x: print(HELP_MSG))\
                    (' '.join(args))
                except ValueError as err:
                    print(err.args[0])

        else:
            print('Use -i or --interactive to enter interactive mode')

    def exit(self, sig, frame):
        with open(CACHE, 'wb') as backup:
            pickle.dump(self, backup)
        print('\nCurrent tasks saved. Keep Moving!')
        print('{}\nGoodbye\n{}'.format('*'*50, '*'*50))
        sys.exit(0)

class toDoThing(object):
    '''todo thing'''
    def __init__(self, content):
        self._content = content

    def getContent(self):
        return self._content

class toDoList(object):
    '''todo list: the container for several things'''
    def __init__(self):
        self._listOfThings = []

    def addThing(self, content):
        newThing = toDoThing(content)
        self._listOfThings.append(newThing)

    def deleteThing(self, t_id):
        self._listOfThings.pop(int(t_id)-1)

    def printList(self):
        for t_id, thing in enumerate(self._listOfThings):
            print('{}. {}'.format(str(t_id+1), thing.getContent()))


if __name__ == '__main__':
    print ('{}\nTODO is Todo!\n{}'.format('*'*50, '*'*50))
    if not os.path.isfile(CACHE):
        todo = TodoApp()
    else:
        with open(CACHE, 'rb') as f:
            todo = pickle.load(f)
    signal.signal(signal.SIGINT, todo.exit)
    todo.main(sys.argv[1:])
