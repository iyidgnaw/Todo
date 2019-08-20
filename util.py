import os

CACHE = os.getcwd() + '/appCache'
HELP_MSG = 'User Commands:\n\
        ls: list all lists or list all items.\n\
        new : create a new list or a new item.\n\
        rm : delete a item or delete a list.\n\
        mv : update the list name or move an item to another list.\n\
        main : go back to main menu\n\
        exit: save the exit the app.'

HELP_USAGE = {
        'ls': 'Usage:\n  ls',
        'new': 'Usage:\n new [listName/content]',
        'rm': 'Usage:\n rm [task_id/listName]',
        'use': 'Usage:\n use [listName]',
        'mv': 'Usage:\n mv listName listName / mv itemId listName',
        'main': 'Usage:\n main',
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
