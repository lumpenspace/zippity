import unittest
from packgpt import cli

class TestCLI(unittest.TestCase):
    def test_cli_function(self):
        # Here you can call your cli function and assert the expected result
        result = cli.your_cli_function('arg1', 'arg2')
        self.assertEqual(result, 'expected result')

if __name__ == '__main__':
    unittest.main()