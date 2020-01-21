#!/bin/bash
sqlcmd -S $(scripts/get_docker_ip),1433 -U SA -P "yourStrong(!)Password"
