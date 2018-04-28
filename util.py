import os

CACHE = os.getcwd() + '/appCache'
HELP_MSG = 'User Commands:\n\
        show: show the things in current list.\n\
        listall: show available lists in app.\n\
        add : add a new task to current list.\n\
        delete : delete a task from current list with an id.\n\
        abort : abort the current list.\n\
        new : create a new list with given name.\n\
        use : switch to specific list with given name.\n\
        exit: save the exit the app.'

HELP_USAGE = {
        'show': 'Usage:\n  show',
        'listall': 'Usage:\n  listall',
        'add': 'Usage:\n add [content]',
        'delete': 'Usage:\n delete [task_id]',
        'abort': 'Usage:\n abort [list_name]',
        'new': 'Usage:\n new [list_name]',
        'use': 'Usage:\n use [list_name]',
        'exit': 'Usage:\n exit'
        }

MSG = {
        'Invalid id': 'Given id is out of range',
        'Unsupport Name': 'Given name is not support',
        'Name Not Found': 'Given name not found',
        'Delete Default': 'Cannot delete default list',
        'Not a String': 'Given value is not a string',
        'Empty Field': 'Empty field is not allowed',
        'Item Exists': 'Item already exists'
        }
