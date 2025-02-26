import os
import tempfile
import glob
from git import Repo
from loguru import logger
from typing import List
from .utils import get_repo_name
from .models import FileClass
from kgfc import Treesitter
from kgfc.database.client import Neo4jManager
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


def insert_to_kg(repo_url: str, parsed_code: List[FileClass]):
    client = Neo4jManager()
    repo_name = get_repo_name(repo_url)
    # Create the repo node
    try:
        _ = client.create_node("Repository", {'repo_name': repo_name, 'repo_url': repo_url})
        logger.info("Created repo node successfully")
    except Exception as e:
        logger.error(f"Failed to create a node: {e}")

    for _, code in enumerate(parsed_code):
        for idx, sub_dir in enumerate(code.path):
            if idx == 0:
                query = """
                    MATCH (repo: Repository {repo_name: $repo_name})  // Find the existing parent node
                    MERGE (subdir:SUBDIR {name: $sub_dir})  // Create the child node if it doesn't exist
                    MERGE (repo)-[:CONTAINS]->(subdir)  // Create the relationship if it doesn't exist
                    RETURN subdir
                """
                parameters = {'repo_name': repo_name, 'sub_dir': sub_dir}
                _ = client.execute_query(query, parameters)

            elif idx == (len(code.path) - 1):
                query = """
                    MATCH (subdir: SUBDIR {name: $sub_dir})
                    CREATE (file:FILE {filename: $filename})
                    MERGE (subdir)-[:CONTAINS]->(file)
                    RETURN file
                """
                parameters = {'sub_dir': code.path[idx-1], 'filename': sub_dir}
                _ = client.execute_query(query, parameters)
                logger.info(f"Successfully added file: {sub_dir}")
            else:
                query = """
                    MATCH (parentdir: SUBDIR {name: $parent_subdir})  // Find the existing parent node
                    MERGE (subdir:SUBDIR {name: $sub_dir})  // Create the child node if it doesn't exist
                    MERGE (parentdir)-[:CONTAINS]->(subdir)  // Create the relationship if it doesn't exist
                    RETURN subdir
                """
                parameters = {'parent_subdir': code.path[idx-1], 'sub_dir': sub_dir}
                _ = client.execute_query(query, parameters)


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
