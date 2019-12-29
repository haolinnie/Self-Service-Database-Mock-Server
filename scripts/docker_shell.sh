#!/bin/bash
docker exec -it $( docker ps | grep ssd_server | awk '{print $1}') /bin/bash
