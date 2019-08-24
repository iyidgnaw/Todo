### Todo app in terminal.

#### Usage

`./todo.py` will show you the current task you have in default list or the list you have selected.

`./todo.py -i` will start the interactive mode and waiting for your command.

You can then type `help` or `ANYTHING YOU WANT` to get the supported commands list.

Enjoy. 

### TODO:
- [x] ls in top menu will present all lists  
- [x] ls in list menu will list all items  
- [x] new in top menu will create a list (name cannot be duplicate or None)  
- [x] new in list menu will create an item (content cannot be None)  
- [x] rm in top menu will delete a list  
- [x] rm in list menu will delete an item  
- [x] mv in top menu will change the list name (mv oldName newName)  
- [ ] mv in list menu will move item to another list (mv itemId listName)  
- [x] main will go back to main menu  
- [ ] in-app auto-completion  
- [ ] reset whole app  
- [ ] Persist into database


Exceptions:
    ItemIdNotFound, ListNameNotFound, ListNameConflict

