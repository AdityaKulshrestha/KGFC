from setuptools import setup, find_packages

with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

setup(
    name='kgfc',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'kgfc=kgfc.cli:main',  # This creates the CLI command
        ],
    },
    include_package_data=True,
    author="Aditya Kulshrestha",
    description="A simple command-line tool to generate a knowledge graph based on your GitHub repo",
)
