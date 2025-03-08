import requests


def _accent_repositories():
    response = requests.get("http://mirror.accentservices.com/repos/all")
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        raise RuntimeError("Unable to fetch repositories list. Reponse code: %s." % response.status_code)


accent_repositories = _accent_repositories()
