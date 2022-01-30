import sys
import argparse

from src.leader_board import extract_results_from_source_table, get_ranking_table_str

parser = argparse.ArgumentParser(description='Parse a game table and outputs the ranking.')
parser.add_argument('file', type=str,
                    help='text file representing a valid game match table')

if __name__ == '__main__':
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        source_tbl = f.readlines()

    ranking = extract_results_from_source_table(source_tbl)

    ranking_str = get_ranking_table_str(ranking)

    sys.stdout.write(ranking_str)
