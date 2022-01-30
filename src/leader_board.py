from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Match:
    t1_name: str
    t1_score: int
    t2_name: str
    t2_score: int


class TeamResult:
    def __init__(self, name: str, points: int):
        self.name: str = name
        self.points: int = points
        # This step is calculated after all teams are sorted.
        self.rank = None

    def __lt__(self, other):
        """
        Teams should first be sorted in descending order by score
        and secondly in ascending alphabetical order by team name.
        """
        if not isinstance(other, TeamResult):
            raise TypeError(f"'<' not supported between instances of '{type(other)}' and '{type(self)}'")
        if self.points == other.points:
            return self.name < other.name
        else:
            return self.points > other.points

    def __str__(self):
        return f'{self.rank}. {self.name}, {self.points} {("pt" if self.points == 1 else "pts")}'


def parse_match(match: str) -> Match:
    """
    Parses a match string into its relevant parts for team one and two.

    Example:
    Given the following match:
        Tarantulas 1, FC Awesome 0
    The expected output is:
        Team 1 name: Tarantulas
        Team 1 score: 1
        Team 2 name: FC Awesome
        Team 2 score: 0

    :param match: Since match outcome string.
    :return: Tuple representing first team name and score and second team name and score.
    """

    t1, t2 = match.strip().split(',')

    def get_team_output(team_str: str):
        name, _, score = team_str.rpartition(' ')
        return name.strip(), int(score)

    t1_name, t1_score = get_team_output(t1)
    t2_name, t2_score = get_team_output(t2)

    return Match(t1_name, t1_score, t2_name, t2_score)


def apply_match_points(match: Match, points: Dict[str, int]) -> None:
    """
    Calculate the points awarded to team one and two for the given match.

    Scoring rules:
    - Tie is worth 1 point
    - Win is worth 3 points
    - Loss is worth 0 points
    """
    if match.t1_score > match.t2_score:
        t1_points = 3
        t2_points = 0
    elif match.t1_score < match.t2_score:
        t1_points = 0
        t2_points = 3
    else:
        t1_points = 1
        t2_points = 1
    points[match.t1_name] = points.get(match.t1_name, 0) + t1_points
    points[match.t2_name] = points.get(match.t2_name, 0) + t2_points


def apply_ranks(results: List[TeamResult]) -> None:
    """
    Calculates the ranking for each team.
    Ranking starts at 1 for the team with the most points.
    Teams with the same points, get the same score.
    If a team has fewer points than the previous team, their rank is the total number of previous teams + 1.
    """
    prev_points = None
    point_group_rank = 0
    for i in range(0, len(results)):
        r = results[i]
        if prev_points is None:
            prev_points = r.points
            point_group_rank = 1
        elif r.points < prev_points:
            prev_points = r.points
            point_group_rank = i + 1
        r.rank = point_group_rank


def extract_results_from_source_table(src_tbl: List[str]) -> List[TeamResult]:
    """
    Orchestration function for the game ranking problem.

    Does the following:
    1. Parses each match.
    2. Award points for each team.
    3. Sorts the teams according the points and name.
    4. Assigns appropriate rank for each team.

    :param src_tbl: List of strings, each representing a match.
    :return: Sorted and ranked list of teams.
    """

    # key is team name, value is int with score
    scores: Dict[str, int] = dict()

    for match_str in src_tbl:
        match = parse_match(match_str)
        apply_match_points(match, scores)

    results = [TeamResult(name, points) for name, points in scores.items()]
    results.sort()

    apply_ranks(results)

    return results


def get_ranking_table_str(results: List[TeamResult]):
    """
    Generates a ranking table string for the given sorted results list.

    :return: String representing the ranking table.
    """

    s = ""
    for i in range(0, len(results)):
        s += f'{results[i]}\n'
    return s
