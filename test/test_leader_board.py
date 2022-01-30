import pathlib
import unittest

from src.leader_board import extract_results_from_source_table, get_ranking_table_str, TeamResult


class TestLeaderBoard(unittest.TestCase):
    current_path = pathlib.Path(__file__).parent.resolve()

    def _get_source_table(self, file_path):
        with open(self.current_path / file_path, mode='r') as f:
            source_table = f.readlines()
        self.assertIsNotNone(source_table)

        return source_table

    def _get_assertion_text(self, file_path):
        with open(self.current_path / file_path, mode='r') as f:
            solution_text = f.read()
        self.assertIsNotNone(solution_text)

        return solution_text

    def test_example_case(self):
        """
        Test the example test game provided by problem statement.
        """
        source_table = self._get_source_table('data/example_problem.txt')
        solution_text = self._get_assertion_text('data/example_solution.txt')

        tbl = extract_results_from_source_table(source_table)
        tbl_str = get_ranking_table_str(tbl)

        self.assertEqual(tbl_str, solution_text)

    def test_edge_case_winning_t2(self):
        """
        Test edge case where winning team in match is team 2 (example problem only had winning team 1).
        """
        source_table = self._get_source_table('data/winning_t2_problem.txt')
        solution_text = self._get_assertion_text('data/winning_t2_solution.txt')

        tbl = extract_results_from_source_table(source_table)
        tbl_str = get_ranking_table_str(tbl)

        self.assertEqual(tbl_str, solution_text)

    def test_sort_edge_case(self):
        tr = TeamResult('Team1', 1)
        with self.assertRaises(TypeError):
            results = ['some_string', tr]
            results.sort()
        with self.assertRaises(TypeError):
            results = [tr, 'some_string']
            results.sort()
