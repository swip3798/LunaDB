import json

class Table():

    def __init__(self, path, name, id_field):
        self.name = name
        self.id_field = id_field
        self.path = path + name

    def insert(self, row):
        '''
        Inserts a new document to table
        '''
        entry = json.dumps(row, separators=(',',':'))
        self._write_string(entry)

    def update(self, row):
        '''
        Updates a document matching with the id_field
        '''
        pass
    
    def delete(self, filter_function):
        '''
        Deletes all documents matching to the filter function
        '''
        pass
    
    def search(self, filter_function):
        '''
        Searches in the documents of a table
        '''
        with open(self.path, "r") as f:
            while True:
                entry = f.readline()
                typ = self._check_entry(entry)
                if typ == 1:
                    continue
                elif typ == 2:
                    break
                else:
                    entry = json.loads(entry)
            
    
    def upsert(self, row):
        '''
        Inserts or updates a new document, update works only with id_field
        '''
        pass
    
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