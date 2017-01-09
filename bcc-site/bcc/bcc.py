# -*- coding: utf-8 -*-
"""
    BCC
    ~~~~~~

    A site designed to manage parts, orders, and inventry.

"""

import os
#TODO hook in a mysql client
#from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/bom')
def bom_builder_page():
    return render_template('bom.html')

@app.route('/inventory')
def inventory_page():
    return render_template('inventory.html')

@app.route('/orders')
def orders_page():
    return render_template('orders.html')

@app.route('/dealers')
def dealers_page():
    return render_template('dealers.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('home_page'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home_page'))
