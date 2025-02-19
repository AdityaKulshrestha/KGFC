import os 
import tempfile
from git import Repo
from .utils import get_repo_name
from kgfc import Treesitter


def generate_codebase_tree(repo_url: str):
    """Generates a directory tree for a Github Repository"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_name = get_repo_name(repo_url)
        repo_path = os.path.join(temp_dir, repo_name)
        try:
            Repo.clone_from(repo_url, repo_path)
        except Exception as e:
            raise Exception(f"Failed to clone repository: {e}")


def read_file_content(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
        file_bytes = code.encode()
        return file_bytes


def parse_code_content(file_bytes: bytes):
    treesitter_parser = Treesitter().create_treesitter()    
    class_nodes, method_nodes = treesitter_parser.parse(file_bytes)
    return class_nodes, method_nodes
