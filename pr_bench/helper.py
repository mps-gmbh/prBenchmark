import contextlib
import os
import requests
import subprocess
import time
import yaml

from pr_bench.git import git_checkout
from pr_bench.exc import PrBenchmarkError


@contextlib.contextmanager
def cd(path):
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


def load_config(commit):
    git_checkout(commit)
    with open("benchmark.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


def wait_for_server(url):
    server_ready = False
    for _ in range(10):
        try:
            requests.get(url)
        except requests.exceptions.RequestException:
            time.sleep(0.5)
        else:
            server_ready = True
            break

    if not server_ready:
        raise PrBenchmarkError("Could not reach test server")
