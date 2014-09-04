#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Sample Flask application."""


from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/traditional/')
def traditional():
    contador = request.values.get('contador', 0)
    contador = int(contador) + 1
    return render_template('traditional.html',
                           contador=contador)

@app.route('/spa/')
def spa():
    return render_template('spa.html', contador=1)

@app.route('/spa/counter/')
def spa_counter():
    contador = request.values.get('contador', 1)
    contador = int(contador) + 1
    return render_template('spa-counter.html', contador=contador)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
