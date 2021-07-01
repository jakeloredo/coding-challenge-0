from io import StringIO
import unittest
from unittest.mock import patch

from solution import build_hierarchy


class TestSolution(unittest.TestCase):
    def test_hierarchy(self):
        test_data = [
            {'first_name': 'Jeff', 'id': 1, 'manager': None, 'salary': 110000},
            {'first_name': 'Andy', 'id': 2, 'manager': 1, 'salary': 90000}
        ]

        h = build_hierarchy(test_data)
        self.assertEqual(200000, h.total_salary)
        self.assertIsNotNone(h.get_employee(1))
        self.assertIsNotNone(h.get_employee(1).get('direct_reports'))
        self.assertListEqual(h.get_employee(1).get('direct_reports'), [2])

    def test_print_output(self):
        test_data = [
            {'first_name': 'Dave', 'id': 1, 'manager': 2, 'salary': 100000},
            {'first_name': 'Jeff', 'id': 2, 'manager': None, 'salary': 110000},
            {'first_name': 'Andy', 'id': 3, 'manager': 1, 'salary': 90000},
            {'first_name': 'Jason', 'id': 4, 'manager': 1, 'salary': 80000},
            {'first_name': 'Dan', 'id': 5, 'manager': 1, 'salary': 70000},
            {'first_name': 'Rick', 'id': 6, 'manager': 1, 'salary': 60000},
            {'first_name': 'Suzanne', 'id': 9, 'manager': 1, 'salary': 80000}
        ]
        expected_output = "Jeff\n\tDave\n\t\tAndy\n\t\tDan\n\t\tJason\n\t\tRick\n\t\tSuzanne\n"

        h = build_hierarchy(test_data)
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            h.pretty_print()
            self.assertEqual(mock_stdout.getvalue(), expected_output)
