from itertools import imap
from sh import git
from concurrent.futures import ThreadPoolExecutor, wait


def find_repo_unmerged_branches(repository_path):
    git_branches = git.bake('branch', '-a', '--no-color', '--no-merged', 'origin/master')
    branches = imap(_clean_branch_name, git_branches(_cwd=repository_path, _iter=True))
    for branch in branches:
        yield branch


def find_repo_merged_branches(repository_path):
    git_branches = git.bake('branch', '-a', '--no-color', '--merged', 'origin/master')
    for raw_branch in git_branches(_cwd=repository_path, _iter=True):
        if 'master' in raw_branch:
            continue
        yield _clean_branch_name(raw_branch)


def _clean_branch_name(raw_line):
    return raw_line[2:-1]


def _fetch_repo(repository_path):
    git_fetch = git.bake('fetch', '-p')
    git_fetch(_cwd=repository_path)


def display_branches(leftover):
    for repo, branch in leftover:
        print("{} : {}".format(repo, branch))


def fetch_all_repositories(repository_paths):
    with ThreadPoolExecutor(max_workers=010) as executor:
        futures = [executor.submit(_fetch_repo, repo) for repo in repository_paths]
        wait(futures)
