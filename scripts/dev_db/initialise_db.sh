#!/bin/bash
sudo docker cp data/sample_db_mssql1.sql mssql1:/tmp
sudo docker exec -it mssql1 /opt/mssql-tools/bin/sqlcmd \
   -S 0.0.0.0 -U SA -P "yourStrong_Password" \
   -i '/tmp/sample_db_mssql1.sql'

sudo docker cp data/sample_db_mssql2.sql mssql2:/tmp
sudo docker exec -it mssql2 /opt/mssql-tools/bin/sqlcmd \
   -S 0.0.0.0 -U SA -P "yourStrong_Password" \
   -i '/tmp/sample_db_mssql2.sql'
