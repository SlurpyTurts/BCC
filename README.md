# BCC web site

## Running locally

The most simple way to get started on development is to run apache http with php installed in a docker container.
Install docker from [here](https://www.docker.com/products/overview). After docker is installed and
running, just run the following command

    ./start_local_web_server.sh

The command will launch a web server pointing to the root directory as its base and open the
browser to the launched web site.

To stop the web site, run

    ./stop_local_web_server.sh

This command will shutdown the apache-php container and remove it.
