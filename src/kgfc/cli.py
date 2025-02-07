import argparse
# from kgfc import *


def main():
    parser = argparse.ArgumentParser(description='Generate a knowledge graph directly from Github repository')
    parser.add_argument('repo_url', type=str, help='URL of the github repository')
    parser.add_argument('-o', '--output', type=str, help='Output directory for the local knowledge graph')

    args = parser.parse_args()

    
if __name__ == "__main__":
    main()