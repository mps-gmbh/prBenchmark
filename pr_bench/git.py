import subprocess


def check_repo():
    cp = subprocess.run(
        ["git", "status"], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    return cp.returncode == 0


def git_checkout(commit):
    from pr_bench import PrBenchmarkError

    # check if modified files are present
    output = subprocess.check_output(["git", "status", "--porcelain"]).decode()
    if any(x.strip().startswith("M") for x in output.split("\n")):
        raise PrBenchmarkError("working directory not clean")

    cp = subprocess.run(
        ["git", "checkout", commit], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
