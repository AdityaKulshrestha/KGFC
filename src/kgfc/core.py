import os 
import tempfile
from git import Repo
from .utils import get_repo_name

def generate_codebase_tree(repo_url: str):
    """Generates a directory tree for a Github Repository"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_name = get_repo_name(repo_url)
        repo_path = os.path.join(temp_dir, repo_name)
        try:
            Repo.clone_from(repo_url, repo_path)
        except Exception as e:
            raise Exception(f"Failed to clone repository: {e}")
