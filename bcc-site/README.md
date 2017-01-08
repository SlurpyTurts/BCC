# bcc-site

This is a node express based site for BCC. Node express was chosen because it provided one solution for UI and backend, offers many online tutorials and help, and has a small learning curve.

# Project structure

##routes
  Handles collecting data, DB queries, stuff like that. Once the appropriate data is gathered, a view is picked to render the data.

##views
  Handles display of the data

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
