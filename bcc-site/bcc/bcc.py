# -*- coding: utf-8 -*-
"""
    BCC
    ~~~~~~

    A site designed to manage parts, orders, and inventory.

"""

import os

from dataaccess import inventory_repository, part_repository, bom_repository, dealer_repository, order_repository, supplier_repository, todo_repository
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))

inv_repo = inventory_repository.InventoryRepository()
part_repo = part_repository.PartRepository()
bom_repo = bom_repository.BomRepository()
dealer_repo = dealer_repository.DealerRepository()
order_repo = order_repository.OrderRepository()
supplier_repo = supplier_repository.SupplierRepository()
todo_repo = todo_repository.TodoRepository()

@app.route('/')
def home_page():
    return render_template('index.html')



@app.route('/bom')
def bom_builder_page():
    part_number = request.args.get('part_number')
    levels = request.args.get('levels')
    if part_number and levels:
        bom_items=bom_repo.get_bom_of_parent(part_number, int(levels))
        print('number of bom items ' + str(len(bom_items)))
        return render_template('bom.html', bom_items=bom_items, part_number=part_number, levels=levels)
    return render_template('bom.html')



@app.route('/inventory')
def inventory_page():

    return render_template('inventory.html', inventory_items=inv_repo.get_inventory_list())



@app.route('/parts/<int:part_number>')
def part_detail(part_number):
    return render_template('part_detail.html', part=part_repo.get_part_by_part_number(part_number), supplier_parts=supplier_repo.get_supplier_parts_by_part(part_number))

@app.route('/parts')
def part_search():
    part_prefix=request.args.get('part_prefix')
    if part_prefix:
        return render_template('part_search.html', searchresults=part_repo.get_parts_by_part_number_prefix(part_prefix))

    part_description=request.args.get('description')
    if part_description:
        return render_template('part_search.html', searchresults=part_repo.get_parts_by_description(part_description))

    return render_template('part_search.html')





@app.route('/orders')
def orders_page():
    return render_template('order_overview.html', orders=order_repo.get_order_overview())

@app.route('/orders/<int:order_number>')
def order_detail_page(order_number):
    return render_template('order_detail.html', order=order_repo.get_order_lines(order_number), payments=order_repo.get_order_payments(order_number))





@app.route('/suppliers')
def suppliers_page():
    return render_template('supplier_overview.html')




@app.route('/dealers')
def dealers_page():
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
       page = 1
    number_of_dealers = 5
    dealer_start = (page - 1) * number_of_dealers
    return render_template('dealers.html', dealers = dealer_repo.get_dealer_list(dealer_start, number_of_dealers), page = page, max_page = 5)

@app.route('/dealers/<int:dealer_id>')
def dealer_detail_page(dealer_id):
    return render_template('dealer_detail.html', dealers = dealer_repo.get_dealer_detail(dealer_id), dealerOrders = dealer_repo.get_order_list(dealer_id))



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
    return render_template('todo.html', todos = todo_repo.get_todo_list())