#!/bin/bash
docker run -d --rm -p 5100:5100 -p 3306:3306 --name ssd_container ssd_server 
