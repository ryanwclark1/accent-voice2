import argparse
import os

from repo_check.check_local_accent_repositories import assert_no_missing_repos
from repo_check.git import display_branches, fetch_all_repositories, find_repo_unmerged_branches
from repo_check.repositories import accent_repositories


def main():
    parsed_args = _parse_args()
    directory = parsed_args.directory

    assert_no_missing_repos(directory)
    fetch_all_repositories(os.path.join(directory, accent_rep) for accent_rep in accent_repositories)
    leftover = _find_prefixed_unmerged_branches(directory, parsed_args.prefix)
    display_branches(leftover)


def _find_prefixed_unmerged_branches(directory, prefix):
    leftover = []
    for repository in accent_repositories:
        repository_path = os.path.join(directory, repository)
        current_leftover = [
            (repository, branch)
            for branch in find_repo_unmerged_branches(repository_path)
            if _is_prefixed(branch, prefix)
        ]
        leftover.extend(current_leftover)

    return leftover


def _is_prefixed(branch, prefix):
    return branch.startswith(prefix) or branch.startswith('remotes/origin/' + prefix)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix", help='prefix used to name all branches related to ticket')
    parser.add_argument(
        "-d",
        "--directory",
        help='directory containing all accent repositories (default : $HOME/accent_src)',
        default=os.environ['HOME'] + '/accent_src',
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
