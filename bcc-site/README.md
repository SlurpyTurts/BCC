# bcc-site

This is a Flask based site for BCC

# Project structure

All backend logic is currently performed in bcc.py. As the project grows it can split into multiple files. The templates directory contains html templates which are rendered with logic found in bcc.py.

# Local setup

This project requires python and pip to be installed. Most likely you already have python and pip installed. If not, head on over to the python web site to download it. This project uses python 2.

## One time setup

You will need to make sure you have the following installed

- python
- pip

Next, you need to get the application registered for single sign on with google. To do this:

    1. Go to https://console.developers.google.com/apis/credentials
    2. Register a new application
    3. Set `Authorized JavaScript origins`
        a. 	`https://127.0.0.1:5000`
        b.  `https://localhost:5000`
    4. Set Authorized redirect URIs
        a. 	`https://127.0.0.1:5000/oauth2callback`
        b.  `https://localhost:5000/oauth2callback`
    5. On your app details page in the google console, click `download json`
    6. put the `client_secret.json` file in this directory, don't check it in to source control

## Development

Install dependencies by running

    pip install -r requirements.txt

If you have a new terminal open you have to run

    ./run.sh

The site should now be running on port 5000


## Testing

Run `pytest` to see the tests pass.

## Database connectivity

For database connectivity we use PyMySQL. Check out the docs here.

https://github.com/PyMySQL/PyMySQL

## A note about third party libraries

If you are need another library in the future, make sure to add it to the `requirements.txt` and then simply run `pip install -r requirements.txt`. This command
reads dependencies declared in the dependency file and automatically installs them.
