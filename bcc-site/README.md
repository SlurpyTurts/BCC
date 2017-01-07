# bcc-api

This API is the data tier for the BCC project. It proves a REST API for all interactions
and data interaction.


# Get up and running

Make sure you have node.js installed.

First, you need to install the dependencies. This will download any required libaries
and such.

    npm install

Start the application with this command

    DEBUG=bcc-api:* npm start

This will start the application on port 3000


# Project Structure

  This app uses node Express. It is able to host the front end and provide an extensible backend as well.

## Database calls

  Database connectivity is managed with mysqljs. Check out their guide to write queries.

  https://github.com/mysqljs/mysql
