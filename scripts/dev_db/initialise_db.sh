#!/bin/bash
sudo docker cp data/create_sample_database_mssql.sql sql1:/tmp
sudo docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd \
   -S localhost -U SA -P "yourStrong(!)Password" \
   -i '/tmp/create_sample_database_mssql.sql'
