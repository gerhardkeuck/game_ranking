import pathlib
import unittest

from src.leader_board import extract_results_from_source_table, get_ranking_table_str, TeamResult, parse_match, Match, \
    apply_match_points, apply_ranks


class TestLeaderBoard(unittest.TestCase):
    current_path = pathlib.Path(__file__).parent.resolve()

    def test_team_result_sort(self):
        t1 = TeamResult('TeamA', 2)
        t2 = TeamResult('TeamB', 2)
        t3 = TeamResult('TeamC', 1)

        teams = [t3, t2, t1]
        teams.sort()
        self.assertEqual(teams, [t1, t2, t3])

    def test_team_result_sort_invalid(self):
        tr = TeamResult('Team1', 1)
        with self.assertRaises(TypeError):
            results = ['some_string', tr]
            results.sort()
        with self.assertRaises(TypeError):
            results = [tr, 'some_string']
            results.sort()

    def test_team_result_string(self):
        t1 = TeamResult('Team1', 1)
        self.assertEqual(f'{t1}', '0. Team1, 1 pt')

        t2 = TeamResult('Team2', 2)
        self.assertEqual(f'{t2}', '0. Team2, 2 pts')

        t3 = TeamResult('Team3', 0)
        self.assertEqual(f'{t3}', '0. Team3, 0 pts')

    def test_parse_match(self):
        match_str = '   a b c    5   ,  d e f   7 '
        match = parse_match(match_str)
        self.assertEqual(match.t1_name, 'a b c')
        self.assertEqual(match.t1_score, 5)
        self.assertEqual(match.t2_name, 'd e f')
        self.assertEqual(match.t2_score, 7)

    def test_apply_match_points_t2_win(self):
        m1 = Match('t1', 0, 't2', 1)
        points = dict()
        apply_match_points(m1, points)
        self.assertIn('t1', points)
        self.assertIn('t2', points)
        self.assertEqual(points['t1'], 0)
        self.assertEqual(points['t2'], 3)

        apply_match_points(m1, points)
        self.assertIn('t1', points)
        self.assertIn('t2', points)
        self.assertEqual(points['t1'], 0)
        self.assertEqual(points['t2'], 6)

    def test_apply_match_points_t1_win(self):
        m1 = Match('t1', 1, 't2', 0)
        points = dict()
        apply_match_points(m1, points)
        self.assertIn('t1', points)
        self.assertIn('t2', points)
        self.assertEqual(points['t1'], 3)
        self.assertEqual(points['t2'], 0)

    def test_apply_match_points_draw(self):
        m1 = Match('t1', 1, 't2', 1)
        points = dict()
        apply_match_points(m1, points)
        self.assertIn('t1', points)
        self.assertIn('t2', points)
        self.assertEqual(points['t1'], 1)
        self.assertEqual(points['t2'], 1)

    def test_apply_ranks(self):
        results = [
            TeamResult('t1', 5),
            TeamResult('t2', 5),
            TeamResult('t3', 3),
            TeamResult('t4', 1),
            TeamResult('t5', 1),
        ]
        apply_ranks(results)
        self.assertEqual(results[0].rank, 1)
        self.assertEqual(results[1].rank, 1)
        self.assertEqual(results[2].rank, 3)
        self.assertEqual(results[3].rank, 4)
        self.assertEqual(results[4].rank, 4)

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
