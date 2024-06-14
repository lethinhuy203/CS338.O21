#!/bin/bash

# Create virtual environment and activate it
python -m venv venv
source venv/Scripts/activate

# install required packages
pip install -r requirements.txt
# run code
flask --app src run --debug