from flask import render_template, Blueprint, redirect, url_for, request
from dataaccess import supplier_repository, part_repository, contact_repository
supplier_blueprint = Blueprint('supplier', __name__)
supplier_repo = supplier_repository.SupplierRepository()

# TODO what does supplier management have to do with parts?
part_repo = part_repository.PartRepository()

# TODO what does supplier management have to do with contacts?
contact_repo = contact_repository.ContactRepository()

@supplier_blueprint.route('/update_standard_purchase_price/<int:part>/<int:moq>/<string:supplierPartNumber>')
def update_standard_purchase_price(part, moq, supplierPartNumber):
    supplierPartNumber.replace("%20", " ")
    supplier_repo.remove_standard_purchase_price(part)
    supplier_repo.set_standard_purchase_price(part, moq, supplierPartNumber)
    part_price = supplier_repo.get_part_price(part, moq, supplierPartNumber)
    part_repo.update_standard_purchase_price(part, part_price)
    return redirect(url_for('part_detail', part_number=part))

@supplier_blueprint.route('/parts/<int:part_number>')
def part_detail(part_number):
    parents = part_repo.get_parents(part_number)
    part = part_repo.get_part_by_part_number(part_number)
    supplier_parts = supplier_repo.get_supplier_parts_by_part(part_number)
    return render_template('part_detail.html', parents=parents, part=part, supplier_parts=supplier_parts)

@supplier_blueprint.route('/parts/<int:part_number>/addsource', methods=['GET','POST'])
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

@supplier_blueprint.route('/suppliers')
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

@supplier_blueprint.route('/suppliers/new', methods=['GET','POST'])
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
            supplier_repo.set_new_supplier(supplier, website, status, shipping_address_line_1, shipping_address_line_2,
                                           shipping_city, shipping_state, shipping_zip, shipping_country,billing_address_line_1,
                                           billing_address_line_2, billing_city, billing_state, billing_zip, billing_country)
            return redirect(url_for('suppliers_page'))
    return render_template('supplier_new.html')

@supplier_blueprint.route('/suppliers/<int:supplier_id>')
def get_supplier_detail(supplier_id):
    return render_template('supplier_detail.html', suppliers=supplier_repo.get_supplier_detail(supplier_id),
                           contacts=contact_repo.get_contact_by_supplier(supplier_id),
                           supplier_parts=supplier_repo.get_supplier_part_by_supplier(supplier_id))


