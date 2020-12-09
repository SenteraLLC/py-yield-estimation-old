# py-yield-estimation

``src``: Yield estimation model in bushels/acre based on NDVI

## Installation 

### Windows 

1) [Set up SSH](https://github.com/SenteraLLC/install-instructions/blob/master/ssh_setup.md)
2) Install [conda](https://github.com/SenteraLLC/install-instructions/blob/master/conda.md)
3) Install package

        git clone git@github.com:SenteraLLC/py-yield-estimation.git
        cd py-yield-estimation
        conda env create -f environment.yml
        conda activate yield-venv
        pip install .
   
4) Set up ``pre-commit`` to ensure all commits to adhere to **black** and **PEP8** style conventions.

        pre-commit install
   
#### Linux

1) [Set up SSH](https://github.com/SenteraLLC/install-instructions/blob/master/ssh_setup.md)
2) Install [pyenv](https://github.com/SenteraLLC/install-instructions/blob/master/pyenv.md) and [poetry](https://python-poetry.org/docs/#installation)
3) Install package

        git clone git@github.com:SenteraLLC/py-yield-estimation.git
        cd py-yield-estimation
        pyenv install $(cat .python-version)
        poetry install
        
4) Set up ``pre-commit`` to ensure all commits to adhere to **black** and **PEP8** style conventions.

        poetry run pre-commit install

## Usage

This service takes GeoJSON as input, finds the date with the least cloud coverage from a given date range and outputs a yield estimation in bushels per acre based on NDVI. 

Within the correct poetry/conda shell, run ``src --help`` to view available CLI commands.

## Serverless local usage

Check out the docs [here](https://www.serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/)

        >> serverless invoke local --function yield_estimation --data '{ "geoJSON": ...}'

## Local usage (without serverless)

        >> poetry run python scripts/run_yield_estimation.py

## Documentation

This library is documented using Sphinx. To generate documentation, navigate to the *docs/* subfolder,
and run ``make html``.  Make sure you are in the correct conda environment/poetry shell.  Open 
*docs/\_build/html/index.html* with a browser to get more in depth information on the various modules 
and functions within the library.
