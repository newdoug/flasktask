#!/usr/bin/env python

from flasktask import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

