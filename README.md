
Trello Reporter
===============

This is a simple python + mustache script that allows you to generate
email update reports about your trello boards.

Setup
-----

1. clone this git repo
1. If you wish to use a virtualenv create one and activate it
1. pip install -r requirements.txt, then install my fork of trollop from https://bitbucket.org/richardwarburton/trollop
1. cp trello\_reports/settings-default.py trello\_reports/settings.py and customise
1. run python trello\_reporter/lib.py or put it in a cron job
