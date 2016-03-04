#!/bin/bash
deactivate 2> /dev/null   # in case we are in an env
virtualenv -p python3 .ve && source .ve/bin/activate
pip install -r requirements.txt
./manage.py migrate
