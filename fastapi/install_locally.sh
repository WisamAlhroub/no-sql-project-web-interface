#!/usr/bin/env bash
# this is a script file to install a python virtual environment on your local device

# using bulit-in python venv
python -m venv nosqlproject

# or using conda:
# conda create --name nosqlproject python=3.9

# for linux devices, this script to activate the environment
source env/bin/activate

pip install -r ./requirements.txt