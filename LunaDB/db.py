import os
from .table import Table

class LunaDB():
    def __init__(self, name):
        self.name = name
        self.path = name + "/"
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.root_table = self.table("#")
        
    def table(self, name, id_field = None):
        return Table(self.path, name, id_field = id_field)

    def drop_table(self, name):
        del_path = self.path + name
        os.remove(del_path)

    ###### Root table link methods
    
    def insert(self, row, strict = True):
        self.root_table.insert(row, strict)

    def insert_multiple(self, rows, strict = True):
        self.root_table.insert_multiple(rows, strict)
    
    def delete(self, filter_function, auto_clean = True):
        self.root_table.delete(filter_function, auto_clean)
    
    def search(self, filter_function):
        return self.root_table.search(filter_function)

    

    
