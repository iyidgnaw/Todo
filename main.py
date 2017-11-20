#! /usr/bin/env python
__author__ = 'Diyi Wang'
'''Main module of my Todo app'''

import argparse
import os
import pickle
import shlex
CACHE = '/Users/diyi.wang/Github/Python/Todo/appCache'

class toDoApp(object):
    '''todo application main class'''
    def __init__(self):
        self._registered = {'Default': toDoList()}
        self._using = 'Default'
        print('This is the init')
        self.showAllThing()

    def addThing(self, content):
        currentList = self._getCurrentList()
        currentList.addThing(content)

    def _getCurrentList(self):
        return self._registered[self._using]

    def createList(self, nameOfList):
        self._registered[nameOfList] = toDoList()
        self.useList(nameOfList)

    def showAllThing(self):
        print('Current List: {}'.format(self._using))
        currentList = self._registered[self._using]
        currentList.showAll()

    def showAllList(self):
        for name in self._registered:
            print(name)

    def deleteThing(self, id):
        currentList = self._getCurrentList()
        currentList.deleteThing(id)

    def deleteList(self, nameOfList):
        self._registered.pop(nameOfList, None)

    def useList(self, nameOfList):
        self._using = nameOfList
        print('Using {}'.format(nameOfList))

    # TODO: Edit Thing
    def editThing(self):
        pass

    # TODO: Rename List
    def renameList(self):
        pass

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

    def deleteThing(self, id):
        self._listOfThings.pop(int(id)-1)

    def showAll(self):
        for id, thing in enumerate(self._listOfThings):
            print("{}. {}".format(str(id+1), thing.getContent()))


if __name__ == '__main__':
    print ("TODO is Todo!")
    supportCmd = {'show': 'showAllThing' , # show things in current list
                  'listall': 'showAllList', # list all lists
                  'add': 'addThing', # Add thing
                  'delete': 'deleteThing', # Delete thing
                  'abort': 'deleteList', # Delete list
                  'new': 'createList', # Create new list
                  'use': 'useList' # Switch to list
                  }
    if not os.path.isfile(CACHE):
        # Init the app
        todo = toDoApp()
        print "Init process done!"
    else:
        with open(CACHE, 'rb') as f:
            todo = pickle.load(f)

    
    parser = argparse.ArgumentParser(description='Todo List App in terminal')
    parser.add_argument('command', choices=supportCmd.keys())
    parser.add_argument('-n', '--name', type=str, 
        help='The given list name', default=None)
    parser.add_argument('-c', '--content', type=str,
        help='The content you want in the Thing', default=None)
    parser.add_argument('--id', type=int,
        help='The id you want to delete', default=None)
    args = parser.parse_args()
    
    func = getattr(todo, supportCmd[args.command])
    # if args.command == 'add':
    #     func(args.content)
    # elif args.command in ['use', 'abort', 'new']:
    #     func(args.name)
    # elif args.command == 'delete':
    #     func(args.id)
    # else:
    #     func()
    func(args)
    todo.showAllThing()

    with open(CACHE, 'wb') as f:
        pickle.dump(todo, f)
























    
