from flask import render_template, Blueprint, redirect, url_for, request
from dataaccess import dealer_repository
from flask_login import login_required
dealer_blueprint = Blueprint('dealer', __name__)
dealer_repo = dealer_repository.DealerRepository()

@dealer_blueprint.route('/dealers')
@login_required
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

@dealer_blueprint.route('/dealers/<int:dealer_id>')
@login_required
def dealer_detail_page(dealer_id):
    return render_template('dealer_detail.html', dealers = dealer_repo.get_dealer_detail(dealer_id), dealerOrders = dealer_repo.get_order_list(dealer_id))

@dealer_blueprint.route('/dealers/new', methods=['GET','POST'])
@login_required
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
            return redirect(url_for('dealer.dealers_page'))
        else:
            error='invalid input. Check your input fields.'
    return render_template('dealer_new.html', error=error)

@dealer_blueprint.route('/dealers/<int:dealer_id>/update', methods=['GET', 'POST'])
@login_required
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



