#!/bin/bash
sudo docker run --rm -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=yourStrong_Password' \
   -p 4433:1433 --name mssql1 \
   -d mcr.microsoft.com/mssql/server:2019-GA-ubuntu-16.04


sudo docker run --rm -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=yourStrong_Password' \
   -p 4434:1433 --name mssql2 \
   -d mcr.microsoft.com/mssql/server:2019-GA-ubuntu-16.04

sudo docker ps
