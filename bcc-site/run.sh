#!/bin/bash


rm -rf $(find bcc | grep \\.pyc )
. venv/bin/activate
export FLASK_APP=bcc && flask run
