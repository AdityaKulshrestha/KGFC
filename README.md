# KGFC

A simple toolkit to allow QA on your codebase

## Installation
1. pip install uv
2. uv venv
3. Activate the environment
    ```
    # Linux 
    .venv/bin/activate

    # Windows
    .venv\Scripts\activate
    ```
4. uv pip install -r requirements.txt
5. create a .env file
    ```
    NEO4J_URI=Neo4j url
    NEO4J_USER=Your username
    NEO4J_PASSWORD=Your password
    ```
6. Run the Neo4j docker container
    `docker run --name neo4j-container -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=USERNAME/PASSWORD -v /path/to/your/data:/data neo4j`


## How to run
`python -m kgfc.cli --help`


## Running a simple file
python -m kgfc.cli --file sample_code/main.py