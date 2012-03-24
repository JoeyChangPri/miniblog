#!/bin/sh
command="cd /home/cj/miniblog &&\
git pull origin master &&\
cp _settings.py settings.py &&\
sudo /home/cj/miniblog/runctl restart
"
ssh your@server  "${command}"
