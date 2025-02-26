import os
import tempfile
import glob
from git import Repo
from .utils import get_repo_name
from .models import FileClass
from kgfc import Treesitter
import argparse


def generate_codebase_tree(repo_url: str):
    """Generates a directory tree for a Github Repository"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_name = get_repo_name(repo_url)
        repo_path = os.path.join(temp_dir, repo_name)
        try:
            Repo.clone_from(repo_url, repo_path)

            # Iterate over the files
            python_files_nodes = []
            python_files = glob.glob(os.path.join(repo_path, "**", "*.py"), recursive=True)
            for file_path in python_files:
                file_path = os.path.abspath(file_path)

                try:
                    file_content = read_file_content(file_path)  # Read file content

                    class_nodes, method_nodes = parse_code_content(file_content)  # Parse content
                    subdirs_list = file_path.replace(f'{repo_path}{os.sep}', "").split(os.sep)
                    file_class = FileClass(name=os.path.basename(file_path),
                                           path=subdirs_list,
                                           classes=class_nodes,
                                           methods=method_nodes
                                           )

                    python_files_nodes.append(file_class)

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

            return python_files_nodes

        except Exception as e:
            raise Exception(f"Failed to clone repository: {e}")


def parse_code(args: argparse.Namespace):
    if args.file:
        file_content = read_file_content(args.file)
        class_nodes, method_nodes = parse_code_content(file_content)
        file_nodes = FileClass(
            name=args.file.split(os.sep)[-1],
            path=args.file,
            classes=class_nodes,
            methods=method_nodes
            )
    else:
        file_nodes = generate_codebase_tree(args.repo_url)

    return file_nodes


def read_file_content(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
        file_bytes = code.encode()
        return file_bytes


def parse_code_content(file_bytes: bytes):
    treesitter_parser = Treesitter().create_treesitter()    
    class_nodes, method_nodes = treesitter_parser.parse(file_bytes)
    return class_nodes, method_nodes
