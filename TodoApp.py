#! /usr/local/bin/python3
'''Main module of my Todo app'''

import os
import pickle
import signal
import sys
from util import MSG, HELP_MSG, CACHE, HELP_USAGE

from TodoList import TodoList
from TodoExceptions import ListNameConflictError, ListNameNotFoundError


class TodoApp(object):
    '''todo application main class'''
    def __init__(self):
        self._registered = {'Default': TodoList('Default')}
        self._cur = None
        print('Initiation completed')

    def _create(self, content):
        if not self._cur:
            # Create a list
            if content in self._registered:
                raise ListNameConflictError
            self._registered[content] = TodoList(content)
            self._cur = self._registered[content]
        else:
            # Create a new item
            self._cur.create(content)


    def _get(self):
        if self._cur:
            print('Current List: {}'.format(self._cur.getName()))
            self._cur.get()
        else:
            for listName in self._registered:
                print(listName)


    def _delete(self, content):
        if self._cur:
            # Delete an item
            self._cur.delete(content)
        else:
            # Delete a list
            self._registered.pop(content, None)


    def _useList(self, listName):
        if listName not in self._registered:
            raise ListNameNotFoundError
        self._cur = self._registered[listName]
        print('Using {}'.format(self._cur.getName()))


    def _update(self, names):
        old_name, new_name = names.split(' ')
        if old_name not in self._registered:
            raise ListNameNotFoundError
        self._registered[new_name] = self._registered.pop(old_name)
        self._registered.update(new_name)

    def _backToMain(self):
        self._cur = None

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
        print('{}\nGoodbye\n{}'.format('*'*50, '*'*50))
        sys.exit(0)

    def main(self, todo_args):
        supportCmd = {
                'ls': lambda args: self._get(),
                'new': self._create,
                'rm': self._delete,
                'mv': self._update,
                'use': self._useList,
                'main': lambda args: self._backToMain(),
                'exit': lambda args: self.exit(signal.SIGINT, None),
                'help': self._help
                }
        if not todo_args:
            self._get()

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


if __name__ == '__main__':
    print('{}\nTODO is Todo!\n{}'.format('*'*50, '*'*50))
    if not os.path.isfile(CACHE):
        todo = TodoApp()
    else:
        with open(CACHE, 'rb') as f:
            todo = pickle.load(f)
    signal.signal(signal.SIGINT, todo.exit)
    todo.main(sys.argv[1:])
