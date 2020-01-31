#!/bin/bash
sqlcmd -S $(scripts/get_docker_ip),1434 -U SA -P "yourStrong_Password"
