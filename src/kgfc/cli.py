import argparse
from .core import read_file_content, parse_code_content, parse_code


def main():
    parser = argparse.ArgumentParser(description='Generate a knowledge graph directly from Github repository')
    parser.add_argument('--repo-url', type=str, help='URL of the github repository')
    parser.add_argument('--file', type=str, help="Path of file to parse")
    parser.add_argument('-o', '--output', type=str, help='Output directory for the local knowledge graph')

    args = parser.parse_args()

    if (args.file and args.repo_url):
        parser.error("Only one of --file or --url must be provided.")

    nodes = parse_code(args)
    print([nodes[i].classes for i in range(len(nodes))])


if __name__ == "__main__":
    main()
