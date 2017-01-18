#!/bin/bash

sudo pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install flask
pip install --editable .
