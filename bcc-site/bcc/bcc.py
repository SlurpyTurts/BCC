# -*- coding: utf-8 -*-
"""
    BCC
    ~~~~~~

    A site designed to manage parts, orders, and inventory.

"""

import os, math, locale

locale.setlocale(locale.LC_ALL, 'en_US')

from dataaccess import inventory_repository, part_repository, bom_repository, dealer_repository, order_repository, supplier_repository, todo_repository, contact_repository, terms_repository, freight_repository, testing_repository, inquiry_repository
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json, jsonify


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
contact_repo = contact_repository.ContactRepository()
terms_repo = terms_repository.TermsRepository()
freight_repo = freight_repository.FreightRepository()
test_repo = testing_repository.TestingRepository()
inquiry_repo = inquiry_repository.InquiryRepository()



@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/delete_bom_relationship/<int:parent>/<int:child>')
def delete_bom_relationship(parent, child):
    bom_repo.remove_bom_relationship(parent, child)
    return redirect(url_for('bom_tree', part_number=parent))

@app.route('/delete_order_line/<int:order_number>/<int:line_item>')
def delete_order_line(order_number, line_item):
    order_repo.remove_order_line(order_number, line_item)
    return redirect(url_for('order_detail_page', order_number=order_number))









@app.route('/update_standard_purchase_price/<int:part>/<int:moq>/<string:supplierPartNumber>')
def update_standard_purchase_price(part, moq, supplierPartNumber):
    supplierPartNumber.replace("%20", " ")
    supplier_repo.remove_standard_purchase_price(part)
    supplier_repo.set_standard_purchase_price(part, moq, supplierPartNumber)
    part_price = supplier_repo.get_part_price(part, moq, supplierPartNumber)
    part_repo.update_standard_purchase_price(part, part_price)
    return redirect(url_for('part_detail', part_number=part))

@app.route('/update_order_status/<int:order_number>/string:new_status')
def update_order_status(order_number, new_status):
    order_repo.update_order_status(order_number, new_status)
    return redirect(url_for('order_detail_page', order_number=order_number))










@app.route('/bom')
def bom_builder_page():
    part_number = request.args.get('part_number')
    levels = request.args.get('levels')
    if part_number and levels:
        bom_items=bom_repo.get_bom_of_parent(part_number, int(levels))
        print('number of bom items ' + str(len(bom_items)))
        return render_template('bom_search.html', bom_items=bom_items, part_number=part_number, levels=levels)
    return render_template('bom_search.html')

@app.route('/bom/<int:part_number>', methods=['GET','POST'])
def bom_tree(part_number):
    if request.method == 'POST':
        child_part_number=request.form['partNumber']
        part_qty=request.form['qty']
        part_ref_des=request.form['refDes']
        if part_ref_des == '' or part_ref_des == 'None':
            part_ref_des = None
        bom_repo.set_new_bom_child(part_number, child_part_number, part_qty, part_ref_des)
        return redirect(url_for('bom_tree', part_number=part_number))
    else:
        if request.args.get('level'):
            levels = request.args.get('level')
        else:
            levels = 1
        parts=bom_repo.get_bom_of_parent(part_number, int(levels))
        part_description=part_repo.get_part_description(part_number)
        return render_template('bom_detail.html', parts=parts, part_number=part_number, part_description=part_description, bom_cost=bom_repo.get_bom_cost(part_number), levels=levels)

@app.route('/bom/<int:parent_part>/<int:child_part>', methods=['GET','POST'])
def bom_update(parent_part, child_part):
    if request.method == 'POST':
        quantity=request.form['quantity']
        ref_des=request.form['refDes']
        if ref_des == '' or ref_des == 'None':
            ref_des = None
        bom_repo.update_bom_relationship(parent_part, child_part, quantity, ref_des)
        return redirect(url_for('bom_tree', part_number=parent_part))
    else:
        bom_relationship=bom_repo.get_bom_relationship(parent_part, child_part)
        return render_template('bom_edit.html', bom_relationship=bom_relationship)










@app.route('/inventory')
def inventory_page():
    inventory = inv_repo.get_inventory_list()
    inv_locations=inv_repo.get_inventory_location_list()
    return render_template('inventory.html', inventory=inventory, inv_locations=inv_locations)

@app.route('/inventory/transaction', methods=['GET','POST'])
def set_inventory_transaction():
    error = None
    inventory_locations=inv_repo.get_inventory_location_list()
    if request.method == 'POST':
        part_number=request.form['partNumber']
        quantity=request.form['quantity']
        inventory_from=request.form['inventoryFrom']
        if inventory_from=='6':
            inventory_from=None
        inventory_to=request.form['inventoryTo']
        note=request.form['note']
        transaction_date=request.form['transactionDate']
        inv_repo.set_inv_transaction(part_number, quantity, inventory_from, inventory_to, note, transaction_date)
        return redirect(url_for('inventory_page'))
    part_number=request.args.get('partNumber')
    return render_template('inventory_transaction.html', error=error, locations=inventory_locations)

@app.route('/inventory/<int:part_number>')
def transation_history_by_part(part_number):
    transactions = inv_repo.get_part_transactions(part_number)
    return render_template('inventory_part_transactions.html', transactions=transactions)

@app.route('/inventory/loc/<string:inv_loc>')
def inv_by_loc(inv_loc):
    transactions = inv_repo.get_inventory_list_by_loc()
    inv_locations = inv_repo.get_inventory_location_list()
    return render_template('inventory_loc.html', transactions=transactions, inv_locations=inv_locations)










@app.route('/parts/<int:part_number>')
def part_detail(part_number):
    parents = part_repo.get_parents(part_number)
    part = part_repo.get_part_by_part_number(part_number)
    supplier_parts = supplier_repo.get_supplier_parts_by_part(part_number)
    return render_template('part_detail.html', parents=parents, part=part, supplier_parts=supplier_parts)

@app.route('/parts')
def part_search():

    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
        page = 1
    number_of_parts = 40
    part_start = (page - 1) * number_of_parts
    part_prefix=request.args.get('part_prefix')
    max_page=int(math.ceil(part_repo.get_parts_count()/number_of_parts) + 1)

    if part_prefix:
        return render_template('part_search.html', searchresults=part_repo.get_parts_by_part_number_prefix(part_prefix))

    part_description=request.args.get('description')
    if part_description:
        return render_template('part_search.html', searchresults=part_repo.get_parts_by_description(part_description))

    if not part_prefix and not part_description:
        return render_template('part_search.html', parts=part_repo.get_parts(part_start, number_of_parts), page=page, max_page=max_page)

    return render_template('part_search.html')

@app.route('/parts/new', methods=['GET','POST'])
def create_new_part():
    if request.method == 'POST':
        part_type = request.form['partType']
        part_number = request.form['partNumber']
        part_description = request.form['partDescription']
        PTSC1 = request.form['partTypeSubClass1']
        PTSC2 = request.form['partTypeSubClass2']
        PTSC3 = request.form['partTypeSubClass3']
        part_status = request.form['partStatus']
        part_unit = request.form['partUnit']
        part_repo.set_new_part(part_type+part_number, part_description, PTSC1, PTSC2, PTSC3, part_unit, part_status)
        return redirect(url_for('part_detail', part_number=part_type+part_number))
    else:
        return render_template('part_new.html', part_status_list=part_repo.get_part_status_list(), part_unit_list=part_repo.get_part_unit_list(), part_type_list=part_repo.get_part_type_list(), part_family_list=part_repo.get_part_family_list())

@app.route('/parts/<int:part_number>/update', methods=['GET','POST'])
def update_part(part_number):
    error = None
    if request.method == 'POST':
        part_description = request.form['partDescription']
        PTSC1 = request.form['PTSC1']
        PTSC2 = request.form['PTSC2']
        PTSC3 = request.form['PTSC3']
        part_unit = int(request.form['partUnit'])
        part_status = int(request.form['partStatus'])
        part_purchase_price = request.form['standardPurchasePrice']
        part_sell_price = request.form['standardSellPrice']
        part_repo.update_part(part_description, PTSC1, PTSC2, PTSC3, part_status, part_unit, part_purchase_price, part_sell_price, part_number)
        return redirect(url_for('part_detail', part_number=part_number))
    else:
        part_unit = part_repo.get_part_unit_list()
        part_status = part_repo.get_part_status_list()
        part = part_repo.get_part_by_part_number(part_number)
        return render_template('part_update.html', part_unit=part_unit, part=part, part_status=part_status)

@app.route('/parts/<int:part_number>/addsource', methods=['GET','POST'])
def set_part_source(part_number):
    if request.method == 'POST':
        part_supplier=request.form['supplierName']
        supplier_part_number=request.form['supplierPartNumber']
        supplier_link=request.form['supplierPartLink']
        part_MOQ=request.form['partMOQ']
        part_unit_price=request.form['partUnitPrice']
        part_repo.set_part_supplier_update(part_supplier, part_number, supplier_part_number, supplier_link, part_unit_price, part_MOQ)
        return redirect(url_for('part_detail', part_number=part_number))
    else:
        suppliers=supplier_repo.get_supplier_list(0, supplier_repo.get_max_supplier_id())
        return render_template('part_add_source.html', part_number=part_number, suppliers=suppliers)










@app.route('/orders')
def orders_page():
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
        page = 1
    number_of_orders = 5
    max_page = int(math.ceil(order_repo.get_orders_count() / number_of_orders) + 1)
    order_start = (page - 1) * number_of_orders
    orders = order_repo.get_order_overview(order_start, number_of_orders)
    return render_template('order_overview.html', orders=orders, page=page, max_page=max_page)

@app.route('/orders/<int:order_number>')
def order_detail_page(order_number):
    order_info=order_repo.get_order_info(order_number)
    order_lines=order_repo.get_order_lines(order_number)
    order_total=order_repo.get_order_total(order_number)
    customer_info=contact_repo.get_contact_by_order(order_number)
    payments=order_repo.get_order_payments(order_number)
    payments_total=order_repo.get_order_payments_total(order_number)
    shipments=order_repo.get_order_shipments(order_number)
    return render_template('order_detail.html', order_info=order_info, order_lines=order_lines, payments=payments, order_total=order_total, payments_total=payments_total, shipments=shipments, customer_info=customer_info)

@app.route('/orders/<int:order_number>/addLine', methods=['GET','POST'])
def order_add_line(order_number):
    error = None
    if request.method == 'POST':
        part_number=request.form['partNumber']
        quantity=request.form['quantity']
        unit_discount=request.form['unitDiscount']
        if order_number and part_number and quantity:
            if unit_discount is None:
                unit_discount = 0
            order_repo.set_new_order_line(order_number, part_number, quantity, unit_discount)
            return redirect(url_for('order_detail_page', order_number=order_number))
    return render_template('order_line_add.html', order_number=order_number)

@app.route('/orders/<int:order_number>/<int:line_item>/lineEdit', methods=['GET','POST'])
def edit_order_line(order_number, line_item):
    error = None
    if request.method == 'POST':
        quantity=request.form['quantity']
        unit_discount=request.form['lineDiscount']
        if quantity:
            if unit_discount is None:
                unit_discount = 0
            order_repo.update_order_line(order_number, line_item, quantity, unit_discount)
            return redirect(url_for('order_detail_page', order_number=order_number))
    return render_template('order_line_edit.html', line_detail=order_repo.get_order_line_detail(order_number, line_item))

@app.route('/orders/<int:order_number>/addPayment', methods=['GET','POST'])
def order_add_payment(order_number):
    error = None
    if request.method == 'POST':
        payment_amount = request.form['paymentAmount']
        payment_method = request.form['paymentMethod']
        payment_reference = request.form['paymentReference']
        if order_number and payment_amount and payment_method:
            order_repo.set_new_order_payment(order_number, payment_amount, payment_method, payment_reference)
            return redirect(url_for('order_detail_page', order_number=order_number))
    return render_template('order_payment_add.html', order_number=order_number)

@app.route('/orders/<int:order_number>/addShipment', methods=['GET','POST'])
def order_add_shipment(order_number):
    error = None
    carrier_list=freight_repo.get_freight_carrier_list()
    if request.method == 'POST':
        shipment_item = request.form['shipmentItem']
        shipment_serial = request.form['shipmentSerial']
        shipment_date = request.form['shipmentDate']
        shipment_carrier = request.form['shipmentCarrier']
        shipping_method = request.form['shippingMethod']
        tracking_number = request.form['shipmentTrackingNumber']
        shipment_cost = request.form['shipmentCost']
        if order_number and shipment_date and shipment_carrier:
            order_repo.set_new_order_shipment(order_number, shipment_item, shipment_serial, shipment_date, shipment_carrier, shipping_method, tracking_number, shipment_cost)
            return redirect(url_for('order_detail_page', order_number=order_number))
    return render_template('order_shipment_add.html', order_number=order_number, carrier_list=carrier_list)

@app.route('/orders/new', methods=['GET','POST'])
def create_new_order():
    error = None
    if request.method == 'POST':
        dealer=request.form['dealerName']
        terms=request.form['orderTerms']
        cust_first_name=request.form['customerFirstName']
        cust_last_name=request.form['customerLastName']
        cust_phone=request.form['customerPhone']
        cust_email=request.form['customerEmail']
        cust_shipping_address_line_1=request.form['shippingAddressLine1']
        cust_shipping_address_line_2=request.form['shippingAddressLine2']
        cust_city=request.form['shippingCity']
        cust_state=request.form['shippingState']
        cust_zip=request.form['shippingZip']
        cust_country=request.form['shippingCountry']
        if dealer and terms and cust_shipping_address_line_1:
            contact_repo.set_new_cust_contact(cust_first_name, cust_last_name, cust_shipping_address_line_1, cust_shipping_address_line_2, cust_city, cust_state, cust_zip, cust_country, cust_phone, cust_email)
            cust_number = contact_repo.get_max_cust_id()
            order_repo.set_new_order(dealer, terms, cust_number)
            order_number = order_repo.get_max_order_number()
            return redirect(url_for('order_detail_page',order_number=order_number))
    return render_template('order_new.html',dealers=dealer_repo.get_full_dealer_list(), terms=terms_repo.get_terms_list())










@app.route('/suppliers')
def suppliers_page():
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
        page = 1
    number_of_suppliers = 10
    supplier_start = (page - 1) * number_of_suppliers
    return render_template('supplier_overview.html', suppliers=supplier_repo.get_supplier_list(supplier_start, number_of_suppliers), page=page, max_page=5)

@app.route('/suppliers/new', methods=['GET','POST'])
def add_new_supplier():
    if request.method == 'POST':
        supplier=request.form['supplierName']
        website=request.form['supplierWebsite']
        status=request.form['status']
        shipping_address_line_1=request.form['shippingAddressLine1']
        shipping_address_line_2=request.form['shippingAddressLine2']
        shipping_city=request.form['shippingCity']
        shipping_state=request.form['shippingState']
        shipping_zip=request.form['shippingZip']
        shipping_country=request.form['shippingCountry']
        billing_address_line_1 = request.form['billingAddressLine1']
        billing_address_line_2 = request.form['billingAddressLine2']
        billing_city = request.form['billingCity']
        billing_state = request.form['billingState']
        billing_zip = request.form['billingZip']
        billing_country = request.form['billingCountry']
        if supplier and status:
            supplier_repo.set_new_supplier(supplier, website, status, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country,billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country)
            return redirect(url_for('suppliers_page'))
    return render_template('supplier_new.html')

@app.route('/suppliers/<int:supplier_id>')
def get_supplier_detail(supplier_id):
    return render_template('supplier_detail.html', suppliers=supplier_repo.get_supplier_detail(supplier_id), contacts=contact_repo.get_contact_by_supplier(supplier_id), supplier_parts=supplier_repo.get_supplier_part_by_supplier(supplier_id))











@app.route('/dealers')
def dealers_page():
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
       page = 1
    number_of_dealers = 10
    dealer_start = (page - 1) * number_of_dealers
    return render_template('dealers.html', dealer_status=dealer_repo.get_dealer_status_list(), dealers=dealer_repo.get_dealer_list(dealer_start, number_of_dealers), page=page, max_page=5)

@app.route('/dealers/<int:dealer_id>')
def dealer_detail_page(dealer_id):
    return render_template('dealer_detail.html', dealers = dealer_repo.get_dealer_detail(dealer_id), dealerOrders = dealer_repo.get_order_list(dealer_id))

@app.route('/dealers/new', methods=['GET','POST'])
def create_new_dealer():
    error = None
    if request.method == 'POST':
        dealer_name = request.form['dealerName']
        dealer_website = request.form['dealerWebsite']
        dealer_status = request.form['dealerStatus']
        billing_address_line_1 = request.form['billingAddressLine1']
        billing_address_line_2 = request.form['billingAddressLine2']
        billing_city = request.form['billingCity']
        billing_state = request.form['billingState']
        billing_zip = request.form['billingZip']
        billing_country = request.form['billingCountry']
        shipping_address_line_1 = request.form['shippingAddressLine1']
        shipping_address_line_2 = request.form['shippingAddressLine2']
        shipping_city = request.form['shippingCity']
        shipping_state = request.form['shippingState']
        shipping_zip = request.form['shippingZip']
        shipping_country = request.form['shippingCountry']
        if dealer_name and dealer_status and billing_address_line_1 and billing_city and billing_state and billing_zip and billing_country:
            dealer_repo.set_new_dealer(dealer_name, dealer_website, dealer_status, billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country)
            return redirect(url_for('dealers_page'))
        else:
            error='invalid input. Check your input fields.'
    return render_template('dealer_new.html', error=error)

@app.route('/dealers/<int:dealer_id>/update', methods=['GET', 'POST'])
def set_dealer_update(dealer_id):
    if request.method == 'POST':
        dealer_name = request.form['dealerName']
        dealer_website = request.form['dealerWebsite']
        dealer_status = request.form['dealerStatus']
        billing_address_line_1 = request.form['billingAddressLine1']
        billing_address_line_2 = request.form['billingAddressLine2']
        billing_city = request.form['billingCity']
        billing_state = request.form['billingState']
        billing_zip = request.form['billingZip']
        billing_country = request.form['billingCountry']
        shipping_address_line_1 = request.form['shippingAddressLine1']
        shipping_address_line_2 = request.form['shippingAddressLine2']
        shipping_city = request.form['shippingCity']
        shipping_state = request.form['shippingState']
        shipping_zip = request.form['shippingZip']
        shipping_country = request.form['shippingCountry']
        if dealer_name and dealer_status and billing_address_line_1 and billing_city and billing_state and billing_zip and billing_country:
            dealer_repo.set_update_dealer(dealer_name, dealer_website, dealer_status, billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country, dealer_id)
            return redirect(url_for('dealer_detail_page',dealer_id=dealer_id))
    return render_template('dealer_update.html', dealer_info=dealer_repo.get_dealer_detail(dealer_id))










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






@app.route('/inquiry', methods=['GET', 'POST'])
def website_inquiry_overview():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        subject = request.form['subject']
        message = request.form['message']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        date = request.form['date']
        inquiry_repo.set_new_inquiry(first_name, last_name, subject, message, email, city, state, country, date)
        inquiries = inquiry_repo.get_inquiry_list()
        return render_template('inquiry_overview.html', inquiries=inquiries)
    else:
        inquiries = inquiry_repo.get_inquiry_list()
        return render_template('inquiry_overview.html', inquiries=inquiries)

@app.route('/inquiry/<int:inquiry_id>')
def website_inquiry_detail(inquiry_id):
    inquiry=inquiry_repo.get_inquiry_detail(inquiry_id)
    return render_template('inquiry_detail.html', inquiry=inquiry)