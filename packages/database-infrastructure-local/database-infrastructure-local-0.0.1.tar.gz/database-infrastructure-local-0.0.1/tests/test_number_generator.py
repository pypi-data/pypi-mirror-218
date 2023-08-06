import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
load_dotenv()
from NumberGenerator import number_generator

class TestNumberGenerator(unittest.TestCase):
    
    def setUp(self):
        cursor = number_generator.db_connection().cursor()
        cursor.execute("SELECT `number` FROM profile_table")
        
        self.existing_numbers = cursor.fetchall()

    def test_number_generator(self):
        for i in range(100):
            num = self.num_gen.get_random_number()
            assert num not in self.existing_numbers

if __name__ == '__main__':
    unittest.main()