import unittest
import shutil

dir_path = "test_db"

class UpdateTests(unittest.TestCase):
    
    
    def tearDown(self):
        try:
            shutil.rmtree(dir_path)
        except:
            pass