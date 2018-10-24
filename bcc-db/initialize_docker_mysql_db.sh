#!/bin/bash
# Sets up the initial database schema assuming you have a fresh docker image

mysql -u root --password="my-secret-pw" -e "CREATE USER 'bccuser'@'%' IDENTIFIED BY 'password';"
mysql -u root --password="my-secret-pw" < /etc/bcc/BCC_STRUCTURE_LATEST.sql 
mysql -u root --password="my-secret-pw" -e "GRANT ALL PRIVILEGES ON *.* TO 'bccuser'@'%' WITH GRANT OPTION;"
mysql -u root --password="my-secret-pw" -e "UPDATE mysql.user SET Host='%' WHERE Host='localhost';"
mysql -u root --password="my-secret-pw" -e "FLUSH PRIVILEGES;"
