#!/bin/bash

CRUMB=$(curl -s 'http://admin:admin@localhost:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)')
curl -H "$CRUMB" --data-urlencode "script=$(cat /home/jenkins/jenkins/jenkins.groovy)" http://admin:admin@localhost:8080/scriptText
