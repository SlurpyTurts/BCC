#!/bin/bash
docker run -dit \
-p 80:80 \
--name bcc-web-server \
-v "$PWD":/app \
--link bcc-db:mysql \
tutum/apache-php

open http://localhost
