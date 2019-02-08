import json
import os
from .exceptions import DuplicateEntries, DocumentNotFound

class Table():

    def __init__(self, path, name, id_field = None):
        self.name = name
        self.id_field = id_field
        self.path = path + name
        if not os.path.isfile(self.path):
            open(self.path, "w").close()

    def insert(self, row, strict = True):
        '''
        Inserts a new document to table
        If you use strict = False you can use it as insert_or_skip
        '''
        res = self.search(lambda x: x[self.id_field] == row[self.id_field])
        if len(res) == 0:
            entry = json.dumps(row, separators=(',',':'))
            self._write_string(entry)
        elif strict:
            raise DuplicateEntries


    def insert_multiple(self, rows, strict = True):
        '''
        Insert multiple documents to table
        '''
        for idx, i in enumerate(rows):
            if strict:
                res = self.search(lambda x: x[self.id_field] == i[self.id_field])
            else:
                res = []
            if len(res) == 0:
                rows[idx] = json.dumps(i, separators=(',',':'))
        self._write_strings(rows)

    def update(self, row, auto_clean = True, strict = True):
        '''
        Updates a document matching with the id_field
        '''
        if self.delete(lambda x: x[self.id_field] == row[self.id_field], auto_clean=auto_clean):
            self.insert(row)
        elif strict:
            raise DocumentNotFound
    
    def delete(self, filter_function, auto_clean = True):
        '''
        Deletes all documents matching to the filter function
        '''
        res = False
        with open(self.path, "rb+") as f:
            while True:
                line = f.readline().decode("utf-8")
                typ = self._check_entry(line)
                if typ == 1:
                    continue
                elif typ == 2:
                    break
                else:
                    entry = json.loads(line)
                try:
                    if filter_function(entry):
                        f.seek(-len(line), 1)
                        f.write("::".encode("utf-8"))
                        f.seek(len(line) - 2, 1)
                        res = True
                except:
                    pass
        if auto_clean:
            self.clean()
        return res
    
    def search(self, filter_function):
        '''
        Searches in the documents of a table
        '''
        response = []
        with open(self.path, "r") as f:
            while True:
                # Load next line
                entry = f.readline()
                # Check line
                typ = self._check_entry(entry)
                if typ == 1:
                    continue
                elif typ == 2:
                    break
                else:
                    entry = json.loads(entry)
                try:
                    if filter_function(entry):
                        response.append(entry)
                except:
                    pass
        return response
            
    
    def upsert(self, row, auto_clean = True):
        '''
        Inserts or updates a new document, update works only with id_field
        '''
        self.delete(lambda x: x[self.id_field] == row[self.id_field], auto_clean=auto_clean)
        self.insert(row)

    def clean(self):
        '''
        Cleans the whole database
        '''
        tmp = self.path + "tmp"
        os.rename(self.path, tmp)
        new_db = ""
        f = open(tmp, "r")
        while True:
            line = f.readline()
            typ = self._check_entry(line)
            if typ == 1:
                continue
            if typ == 2:
                with open(self.path, "w") as f:
                    f.write(new_db)
                    break
            new_db += line
        os.remove(tmp)
    
    def all(self):
        return self.search(lambda x: True)
    
    ###### Internal abstraction methods ########

    def _write_string(self, string):
        with open(self.path, "a") as f:
            f.write(string + "\n")
    
    def _write_strings(self, string_list):
        string = ""
        for i in string_list:
            string += i + "\n"
        with open(self.path, "a") as f:
            f.write(string)
    
    def _check_entry(self, entry):
        '''
        0 = Can be read
        1 = Is deleted
        2 = End of table
        '''
        if entry == "":
            return 2
        if entry[:2] == "::":
            return 1
        return 0