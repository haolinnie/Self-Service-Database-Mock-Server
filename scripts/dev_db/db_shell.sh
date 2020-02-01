#!/bin/bash
sqlcmd -S $(scripts/get_docker_ip mssql2),4434 -U SA -P "yourStrong_Password"
