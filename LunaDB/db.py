import os
from .table import Table

class LunaDB():
    def __init__(self, name, auto_clean_buffer = 5000000):
        self.name = name
        self.path = name + "/"
        self.id_path = self.path + "ids/"
        self.auto_clean_buffer = auto_clean_buffer
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        if not os.path.isdir(self.id_path):
            os.mkdir(self.id_path)
        self.root_table = self.table("#")
        
    def table(self, name, id_field = None):
        return Table(self.path, name, id_field = id_field, auto_clean_buffer = self.auto_clean_buffer)

    def drop_table(self, name):
        del_path = self.path + name
        os.remove(del_path)

    ###### Root table link methods
    
    def insert(self, row, strict = True):
        '''
        Inserts a new document to table
        If you use strict = False you can use it as insert_or_skip
        '''
        self.root_table.insert(row, strict)

    def insert_multiple(self, rows, strict = True):
        '''
        Insert multiple documents to table
        '''
        self.root_table.insert_multiple(rows, strict)

    def update(self, row, auto_clean = True, strict = True):
        self.root_table.update(row, auto_clean=auto_clean, strict = strict)

    def upsert(self, row, auto_clean = True):
        self.root_table.upsert(row, auto_clean=auto_clean)
    
    def delete(self, filter_function, auto_clean = True):
        self.root_table.delete(filter_function, auto_clean)
    
    def search(self, filter_function):
        return self.root_table.search(filter_function)

    

    
