# bcc-site

This is a Flask based site for BCC

# Project structure

All backend logic is currently performed in bcc.py. As the project grows it can split into multiple files. The templates directory contains html templates which are rendered with logic found in bcc.py.

# Local setup

This project requires python and pip to be installed. Most likely you already have python and pip installed. If not, head on over to the python web site to download it. This project uses python 2.

## One time setup

These commands are only needed the first time you setup the project. After this, don't worry about it.

    pip install flask
    pip install --editable .

## Development

If you have a new terminal open you have to run

  export FLASK_APP=bcc && flask run

The site should now be running on port 5000


## Testing

Run `python setup.py test` to see the tests pass.

## Database connectivity

For database connectivity we use PyMySQL. Check out the docs here.

https://github.com/PyMySQL/PyMySQL

## A note about third party libaries

If you are need another library in the future, make sure to add it to the `setup.py` and then simply run `pip install --editable .`. This command
reads dependencies declared in the setup file and automatically installs them.