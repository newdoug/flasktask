#!/usr/bin/env bash

rm -f flasktask/site.db
python -c '''
from flasktask import *
app = create_app(Config)
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()
'''
exit $?
