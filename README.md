# flasktask

A task/issue management website that behaves similarly to other issue manager websites such as Jira or Trello. Written in Python Flask framework.

## Requirements
Python 3.4+ with pip 19.04 or lower. Transition to Python 3.6 will be done soon.

### Start DB
Run the `./reset_db.sh` script. It will create an empty sqlite database in `flasktask/site.db`. You may start the app anytime after that without issue.

The database will eventually be migrated to something stronger like PostgreSQL

### Start Website
To start this on localhost:5000, just run `python run.py`. Ensure a database is started.


