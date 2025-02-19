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


## How to run
`python -m kgfc.cli --help`


## Running a simple file
python -m kgfc.cli --file sample_code/main.py