import subprocess
import requests
import time

from pr_bench.git import check_repo
from pr_bench.helper import load_config, wait_for_server


def run_single_benchmark(config, tests):
    server = subprocess.Popen(config["start"].split(), stdout=subprocess.PIPE)
    base_url = f"http://localhost:{config['port']}"
    wait_for_server(base_url + config["wait_url"])

    result = {}

    try:
        for test in tests:
            response_times = []
            for _ in range(10):
                response = requests.get(base_url + config["tests"][test]["url"])
                response_times.append(response.elapsed.total_seconds())
            result[test] = {"response_times": response_times}
    finally:
        server.kill()

    return result


def run_benchmark(base_commit, compare_commit):
    if not check_repo():
        raise RuntimeError(f"Not a git repo")

    config_base = load_config(base_commit)
    config_comp = load_config(compare_commit)

    common_tests = [
        x for x in config_base["tests"].keys() if x in config_comp["tests"].keys()
    ]
    results = {}

    base_result = run_single_benchmark(config_base, common_tests)
    compare_result = run_single_benchmark(config_comp, common_tests)

    for test in common_tests:
        print(
            "Base: {} s".format(
                sum(base_result[test]["response_times"])
                / len(base_result[test]["response_times"])
            )
        )
        print(
            "Comp: {} s".format(
                sum(compare_result[test]["response_times"])
                / len(compare_result[test]["response_times"])
            )
        )
