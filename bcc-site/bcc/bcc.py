# -*- coding: utf-8 -*-
"""
    BCC
    ~~~~~~

    A site designed to manage parts, orders, and inventory.

"""

import locale

locale.setlocale(locale.LC_ALL, 'en_US')

from dataaccess import dealer_repository, todo_repository, contact_repository, terms_repository, freight_repository, testing_repository
from flask import Flask, request, session, redirect, url_for, render_template, flash
import inquery_routes
import supplier_routes
import bom_routes
import inventory_routes
import order_routes, dealer_routes, parts_routes

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))

app.register_blueprint(inquery_routes.inquery_blueprint)
app.register_blueprint(supplier_routes.supplier_blueprint)
app.register_blueprint(bom_routes.bom_blueprint)
app.register_blueprint(inventory_routes.inventory_blueprint)
app.register_blueprint(order_routes.order_blueprint)
app.register_blueprint(dealer_routes.dealer_blueprint)
app.register_blueprint(parts_routes.parts_blueprint)

todo_repo = todo_repository.TodoRepository()
test_repo = testing_repository.TestingRepository()

@app.route('/')
def home_page():
    return render_template('index.html')

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

@app.route('/todo')
def todo_overview_page():
    return render_template('todo.html', todos = todo_repo.get_todo_list(), todo_categories=todo_repo.get_todo_categories())

@app.route('/todo/<string:todo_cat>')
def todo_category_page(todo_cat):
    return render_template('todo.html', todos = todo_repo.get_todo_category_list(todo_cat), todo_categories=todo_repo.get_todo_categories())

@app.route('/todo/incomplete')
def todo_incomplete_page():
    return render_template('todo.html', todos = todo_repo.get_todo_unfinished_list(), todo_categories=todo_repo.get_todo_categories())

@app.route('/todo/new', methods=['GET','POST'])
def todo_new_page():
    error=None
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        date_added = request.form['dateAdded']
        if id and category and description and date_added:
            todo_repo.set_todo_item(category, description, date_added)
            return redirect(url_for('todo_overview_page'))
        else:
            error="invalid derp"
    return render_template('todo_new.html', error=error)

@app.route('/test')
def test_overview_page():
    return render_template('test_home.html')

@app.route('/test/speaker/new')
def test_speaker_new():
    return render_template('test_speaker_new.html')

@app.route('/test/amp/new', methods=['GET', 'POST'])
def test_amp_new():
    if request.method == 'POST':
        model=request.form['model']
        serial_number=request.form['serialNumber']
        notes=request.form['notes']
        test_repo.set_amp_test_info(model,serial_number,notes)
        return redirect(url_for('test_amp_new_cosmetic', serial_number=serial_number))
    return render_template('test_amp_new.html')

@app.route('/test/amp/new/<string:serial_number>/cosmetic_check', methods=['GET', 'POST'])
def test_amp_new_cosmetic(serial_number):
    if request.method == 'POST':
        return redirect(url_for('test_amp_new_electric_preliminary', serial_number=serial_number))
    return render_template('test_amp_new_cosmetic_check.html')

@app.route('/test/amp/new/<string:serial_number>/electrical_check_preliminary', methods=['GET', 'POST'])
def test_amp_new_electric_preliminary(serial_number):
    if request.method == 'POST':
        return redirect(url_for('test_amp_new_electric_10percent', serial_number=serial_number))
    return render_template('test_amp_new_electrical_check_preliminary.html')

@app.route('/test/amp/new/<string:serial_number>/electrical_check_10percent', methods=['GET', 'POST'])
def test_amp_new_electric_10percent(serial_number):
    if request.method == 'POST':
        ac_voltage = request.form['acVoltage']
        bias = request.form['bias']
        screen = request.form['screen']
        plate = request.form['plate']
        filament =request.form['filament']
        test_repo.set_amp_voltage_measurement_10_percent(ac_voltage, bias, screen, plate, filament, serial_number)
        return redirect(url_for('test_amp_new_electric_30percent', serial_number=serial_number))
    return render_template('test_amp_new_electrical_check_10percent.html')

@app.route('/test/amp/new/<string:serial_number>/electrical_check_30percent', methods=['GET', 'POST'])
def test_amp_new_electric_30percent(serial_number):
    if request.method == 'POST':
        ac_voltage = request.form['acVoltage']
        bias = request.form['bias']
        screen = request.form['screen']
        plate = request.form['plate']
        filament = request.form['filament']
        test_repo.set_amp_voltage_measurement_30_percent(ac_voltage, bias, screen, plate, filament, serial_number)
        return redirect(url_for('test_amp_new_electric_87percent', serial_number=serial_number))
    return render_template('test_amp_new_electrical_check_30percent.html')

@app.route('/test/amp/new/<string:serial_number>/electrical_check_87percent', methods=['GET', 'POST'])
def test_amp_new_electric_87percent(serial_number):
    if request.method == 'POST':
        ac_voltage = request.form['acVoltage']
        bias = request.form['bias']
        screen = request.form['screen']
        plate = request.form['plate']
        filament = request.form['filament']
        test_repo.set_amp_voltage_measurement_87_percent(ac_voltage, bias, screen, plate, filament, serial_number)
        return redirect(url_for('test_amp_new_electric_100percent', serial_number=serial_number))
    return render_template('test_amp_new_electrical_check_87percent.html')

@app.route('/test/amp/new/<string:serial_number>/electrical_check_100percent', methods=['GET', 'POST'])
def test_amp_new_electric_100percent(serial_number):
    if request.method == 'POST':
        ac_voltage = request.form['acVoltage']
        bias = request.form['bias']
        screen = request.form['screen']
        plate = request.form['plate']
        filament = request.form['filament']
        test_repo.set_amp_voltage_measurement_87_percent(ac_voltage, bias, screen, plate, filament, serial_number)
        power30 = request.form['30Max']
        power1k = request.form['1kMax']
        power30k = request.form['30kMax']
        test_repo.set_amp_power_handling(power30,power1k,power30k,serial_number)
    return render_template('test_amp_new_electrical_check_100percent.html')

