import pytest
from unittest import mock
from pr_bench.git import check_repo, git_checkout
from pr_bench.exc import PrBenchmarkError


@pytest.mark.parametrize("return_code", [0, 128])
def test_check_repo(return_code):
    cp = mock.Mock(returncode=return_code)
    with mock.patch("pr_bench.git.subprocess.run", return_value=cp):
        result = check_repo()

    if return_code == 0:
        assert result
    else:
        assert not result


def test_git_checkout_not_clean():
    output = " M some_file".encode("utf-8")

    with mock.patch("pr_bench.git.subprocess.check_output", return_value=output):
        with pytest.raises(PrBenchmarkError):
            git_checkout("asd")


def test_git_checkout():
    output = "?? some_file".encode("utf-8")

    with mock.patch("pr_bench.git.subprocess.check_output", return_value=output):
        with mock.patch("pr_bench.git.subprocess.run") as run:
            git_checkout("asd")

    assert run.called
