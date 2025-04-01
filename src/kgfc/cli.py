import argparse
from .core import parse_code, insert_to_kg, fetch_answer


def main():
    parser = argparse.ArgumentParser(description='Generate a knowledge graph directly from Github repository')
    parser.add_argument('--repo-url', type=str, help='URL of the github repository')
    parser.add_argument('--file', type=str, help="Path of file to parse")
    parser.add_argument('-o', '--output', type=str, help='Output directory for the local knowledge graph')
    parser.add_argument('-q', '--query', type=str, help='Query to be asked to the codebase')
    parser.add_argument('--repo-name', type=str, help="Repository name for the QA")


    args = parser.parse_args()

    if (args.file or args.repo_url):
        nodes = parse_code(args)
        insert_to_kg(args.repo_url, nodes)
        print([nodes[i].name for i in range(len(nodes))])
    else:
        parser.error("Only one of --file or --url must be provided.")

    if args.q and args.repo_name:
        answer = fetch_answer(args.q, args.repo_name)

    else:
        parser.error("Please provide the repository name for the query!")



if __name__ == "__main__":
    main()
