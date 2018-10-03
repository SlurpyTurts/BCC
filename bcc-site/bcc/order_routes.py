from flask import render_template, Blueprint, redirect, url_for, request
from dataaccess import order_repository, freight_repository, contact_repository, dealer_repository, terms_repository
import math
order_blueprint = Blueprint('order', __name__)
order_repo = order_repository.OrderRepository()
freight_repo = freight_repository.FreightRepository()
contact_repo = contact_repository.ContactRepository()
dealer_repo = dealer_repository.DealerRepository()
terms_repo = terms_repository.TermsRepository()

@order_blueprint.route('/delete_order_line/<int:order_number>/<int:line_item>')
def delete_order_line(order_number, line_item):
    order_repo.remove_order_line(order_number, line_item)
    return redirect(url_for('order_detail_page', order_number=order_number))

@order_blueprint.route('/update_order_status/<int:order_number>/string:new_status')
def update_order_status(order_number, new_status):
    order_repo.update_order_status(order_number, new_status)
    return redirect(url_for('order_detail_page', order_number=order_number))

@order_blueprint.route('/orders')
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

@order_blueprint.route('/orders/<int:order_number>')
def order_detail_page(order_number):
    order_info=order_repo.get_order_info(order_number)
    order_lines=order_repo.get_order_lines(order_number)
    order_total=order_repo.get_order_total(order_number)
    customer_info=contact_repo.get_contact_by_order(order_number)
    payments=order_repo.get_order_payments(order_number)
    payments_total=order_repo.get_order_payments_total(order_number)
    shipments=order_repo.get_order_shipments(order_number)
    return render_template('order_detail.html', order_info=order_info, order_lines=order_lines, payments=payments, order_total=order_total, payments_total=payments_total, shipments=shipments, customer_info=customer_info)

@order_blueprint.route('/orders/<int:order_number>/addLine', methods=['GET','POST'])
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

@order_blueprint.route('/orders/<int:order_number>/<int:line_item>/lineEdit', methods=['GET','POST'])
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

@order_blueprint.route('/orders/<int:order_number>/addPayment', methods=['GET','POST'])
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

@order_blueprint.route('/orders/<int:order_number>/addShipment', methods=['GET','POST'])
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

@order_blueprint.route('/orders/new', methods=['GET','POST'])
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



