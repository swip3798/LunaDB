import json
import os
from .exceptions import DuplicateEntries, DocumentNotFound

class Table():
    '''
    Represents a table holding documents in LunaDB
    '''

    def __init__(self, path, name, auto_clean_buffer, id_field = None):
        '''
        Parameters:
        path : String => The path were the table should be saved
        name : String => Name of the table, also name of the file in the database dir
        auto_clean_buffer : boolean => How many space can be used by disabled entries
        id_field : String => If there is a manual unique id field, it can be named here, otherwise an autoincremented _id field will be used
        '''
        self.name = name
        self.id_field = id_field
        self.auto_clean_buffer = auto_clean_buffer
        self.buffer = 0
        if self.id_field == None:
            self.auto_id = True
            self.id_field = "_id"
        else:
            self.auto_id = False
        self.path = path + name
        self.id_path = path + "ids/" + name 
        if not os.path.isfile(self.path):
            open(self.path, "w").close()
        if not os.path.isfile(self.id_path) and self.auto_id:
            f = open(self.id_path, "w")
            f.write("0")
            f.close()

    def insert(self, row, strict = True):
        '''
        Inserts a new document to table
        If you use strict = False you can use it as an insert or skip

        If you use auto_id, do not use the field "_id", it will be overwritten with the autoincrement id
        '''
        res = self.search(lambda x: x[self.id_field] == row[self.id_field])
        if len(res) == 0:
            if self.auto_id:
                row["_id"] = self._get_new_id()
            entry = json.dumps(row, separators=(',',':'))
            self._write_string(entry)
        elif strict:
            raise DuplicateEntries


    def insert_multiple(self, rows, strict = True):
        '''
        Insert multiple documents to table
        '''
        for idx, i in enumerate(rows):
            res = self.search(lambda x: x[self.id_field] == i[self.id_field])
            if len(res) == 0:
                if self.auto_id:
                    i["_id"] = self._get_new_id()
                rows[idx] = json.dumps(i, separators=(',',':'))
            elif strict:
                raise DuplicateEntries
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
                        self.buffer += len(line)
                except:
                    pass
        if auto_clean and self.buffer > self.auto_clean_buffer:
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
        # os.rename(self.path, tmp)
        new_db = ""
        f = open(self.path, "r")
        while True:
            line = f.readline()
            typ = self._check_entry(line)
            if typ == 1:
                continue
            if typ == 2:
                with open(tmp, "w") as f:
                    f.write(new_db)
                    break
            new_db += line
        os.replace(tmp, self.path)
        self.buffer = 0
    
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
    
    def _get_new_id(self):
        next_id = int(open(self.id_path, "r").read())
        with open(self.id_path, "w") as f:
            f.write(str(next_id + 1))
        return next_id