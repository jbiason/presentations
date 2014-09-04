#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Sample Flask application."""


from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/traditional')
def traditional():
    return render_template('traditional.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
