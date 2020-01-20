#!/bin/bash
sudo docker run --rm -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=yourStrong(!)Password' \
   -p 1433:1433 --name sql1 \
   -d mcr.microsoft.com/mssql/server:2019-GA-ubuntu-16.04
