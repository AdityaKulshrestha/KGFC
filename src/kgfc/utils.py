import os 


def get_repo_name(repo_url: str):
    """Extracts the repository name from the URL"""
    repo_url = repo_url.strip()
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    repo_name = repo_url.split('/')[-1]
    return repo_name 




