import argparse
import sys

from pr_bench.benchmark import run_benchmark
from pr_bench.helper import cd
from pr_bench.exc import PrBenchmarkError


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("base_commit")
    parser.add_argument("compare_commit")
    parser.add_argument("dir")

    args = parser.parse_args()

    with cd(args.dir):
        try:
            run_benchmark(args.base_commit, args.compare_commit)
        except PrBenchmarkError as e:
            print(e)
            sys.exit(1)
