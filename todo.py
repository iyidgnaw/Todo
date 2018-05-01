#! /usr/local/bin/python3
'''Main module of my Todo app'''

import os
import pickle
import signal
import sys
from util import MSG, HELP_MSG, CACHE, HELP_USAGE


class TodoApp(object):
    '''todo application main class'''
    def __init__(self):
        self._registered = {'Default': toDoList()}
        self._using = 'Default'
        print('This is the init')
        self._showAllThing()

    def _addThing(self, content):
        if not isinstance(content, str):
            raise ValueError(MSG['Not a String'])
        if not content:
            raise ValueError(MSG['Empty Field'])
        currentList = self._getCurrentList()
        currentList.addThing(content)

    def _getCurrentList(self):
        return self._registered[self._using]

    def _createList(self, nameOfList):
        if not isinstance(nameOfList, str):
            raise ValueError(MSG['Not a String'])
        if not nameOfList:
            raise ValueError(MSG['Empty Field'])
        if nameOfList in self._registered:
            raise ValueError(MSG['Item Exists'])
        self._registered[nameOfList] = toDoList()
        self._useList(nameOfList)

    def _showAllThing(self):
        print('Current List: {}'.format(self._using))
        currentList = self._registered[self._using]
        currentList.printList()

    def _showAllList(self):
        for name in self._registered:
            print(name)

    def _deleteThing(self, t_id):
        currentList = self._getCurrentList()
        if int(t_id) > currentList.getListLen():
            raise ValueError(MSG['Invalid id'])
        currentList.deleteThing(t_id)

    def _deleteList(self, nameOfList):
        if not isinstance(nameOfList, str):
            raise ValueError(MSG['Not a String'])
        if nameOfList not in self._registered:
            raise ValueError(MSG['Name Not Found'])
        if nameOfList == 'Default':
            raise ValueError(MSG['Delete Default'])
        if nameOfList == self._using:
            self._useList('Default')
        self._registered.pop(nameOfList, None)

    def _useList(self, nameOfList):
        if not isinstance(nameOfList, str):
            raise ValueError(MSG['Not a String'])
        if nameOfList not in self._registered:
            raise ValueError(MSG['Name Not Found'])
        self._using = nameOfList
        print('Using {}'.format(nameOfList))

    def _editThing(self, args):
        t_id, *new_content = args.split(' ')
        new_content = " ".join(new_content)
        currentList = self._getCurrentList()
        if int(t_id) > currentList.getListLen():
            raise ValueError(MSG['Invalid id'])
        currentList.editThing(t_id, new_content)


    def _renameList(self, names):
        old_name, new_name = names.split(' ')
        if not old_name or not new_name:
            raise ValueError(MSG['Empty Field'])
        if old_name not in self._registered:
            raise ValueError(MSG['Item Exists'])
        self._registered[new_name] = self._registered.pop(old_name)

    def _help(self, command=None):
        if not command:
            print(HELP_MSG)
            print('Type >help COMMAND to see detail usage of specific command')
            return
        elif command not in HELP_USAGE:
            raise ValueError(MSG['Unsupport Name'])
        print(HELP_USAGE[command])
        return
###############################################################################
# Public Funtions
###############################################################################

    def exit(self, sig, frame):
        with open(CACHE, 'wb') as backup:
            pickle.dump(self, backup)
        print('\nCurrent tasks saved. Keep Moving!')
        print('{}\nGoodbye\n{}'.format('*'*50, '*'*50))
        sys.exit(0)

    def main(self, todo_args):
        supportCmd = {
                'show': lambda args: self._showAllThing(),
                'listall': lambda args: self._showAllList(),
                'add': self._addThing,
                'delete': self._deleteThing,
                'edit': self._editThing,
                'abort': self._deleteList,
                'new': self._createList,
                'rename': self._renameList,
                'use': self._useList,
                'exit': lambda args: self.exit(signal.SIGINT, None),
                'help': self._help
                }
        if not todo_args:
            self._showAllThing()

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
                except (ValueError, TypeError) as err:
                    print(err.args[0])

        else:
            print('Use -i or --interactive to enter interactive mode')

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

    def editThing(self, t_id, content):
        newThing = toDoThing(content)
        self._listOfThings[int(t_id)-1] = newThing

    def deleteThing(self, t_id):
        self._listOfThings.pop(int(t_id)-1)

    def printList(self):
        for t_id, thing in enumerate(self._listOfThings):
            print('{}. {}'.format(str(t_id+1), thing.getContent()))

    def getListLen(self):
        return len(self._listOfThings)


if __name__ == '__main__':
    print('{}\nTODO is Todo!\n{}'.format('*'*50, '*'*50))
    if not os.path.isfile(CACHE):
        todo = TodoApp()
    else:
        with open(CACHE, 'rb') as f:
            todo = pickle.load(f)
    signal.signal(signal.SIGINT, todo.exit)
    todo.main(sys.argv[1:])
