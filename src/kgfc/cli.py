import argparse
from .core import read_file_content, parse_code_content


def main():
    parser = argparse.ArgumentParser(description='Generate a knowledge graph directly from Github repository')
    parser.add_argument('--repo_url', type=str, help='URL of the github repository')
    parser.add_argument('--file', type=str, help="Path of file to parse")
    parser.add_argument('-o', '--output', type=str, help='Output directory for the local knowledge graph')

    args = parser.parse_args()

    if (args.file and args.repo_url):
        parser.error("Only one of --file or --url must be provided.")

    file_content = read_file_content(args.file)
    class_nodes, method_nodes = parse_code_content(file_content)

    print(method_nodes)


if __name__ == "__main__":
    main()
