# main.py
import argparse
from rich.console import Console
from utils.aoc_client import AocClient

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Advent of Code Toolkit")
    subparsers = parser.add_subparsers(dest="command")

    # ---- collect ----
    p_collect = subparsers.add_parser("collect")
    p_collect.add_argument("--day", "-d", type=int, required=True)
    p_collect.add_argument("--year", "-y", type=int, required=True)

    # ---- submit ----
    p_run = subparsers.add_parser("run")
    p_run.add_argument("--day", "-d", type=int, required=True)
    p_run.add_argument("--year", "-y", type=int, required=True)
    p_run.add_argument("--part", "-p", type=int, required=True, choices=[1,2])
    p_run.add_argument("--test", "-t", type=str, required=True,
                       help="Test mode: True/False")

    args = parser.parse_args()

    client = AocClient.load()

    console.rule("[bold blue]Advent of Code (AOC) Toolkit")
    if args.command == "collect":
        client.collect_day(args.year, args.day)

    elif args.command == "run":
        test_bool = args.test.lower() == "true"
        client.run_solution(args.year, args.day, args.part, test_bool)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
