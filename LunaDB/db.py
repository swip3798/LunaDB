import os
from .table import Table

class LunaDB():
    def __init__(self, name):
        self.name = name
        self.path = name + "/"
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
            open(self.path + "#", "w").close()
        
    def table(self, name, id_field = None):
        return Table(self.path, name, id_field = id_field)

    def drop_table(self, name):
        del_path = self.path + name
        os.remove(del_path)
    
