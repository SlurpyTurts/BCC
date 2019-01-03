from flask import request, render_template, Blueprint, redirect, url_for
from dataaccess import inventory_repository
from flask_login import login_required
inventory_blueprint = Blueprint('inventory', __name__)
inv_repo = inventory_repository.InventoryRepository()

@inventory_blueprint.route('/inventory')
@login_required
def inventory_page():
    inventory = inv_repo.get_inventory_list()
    inv_locations=inv_repo.get_inventory_location_list()
    return render_template('inventory.html', inventory=inventory, inv_locations=inv_locations)

@inventory_blueprint.route('/inventory/transaction', methods=['GET','POST'])
@login_required
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
        return redirect(url_for('inventory.inventory_page'))
    part_number=request.args.get('partNumber')
    return render_template('inventory_transaction.html', error=error, locations=inventory_locations)

@inventory_blueprint.route('/inventory/<int:part_number>')
@login_required
def transation_history_by_part(part_number):
    transactions = inv_repo.get_part_transactions(part_number)
    return render_template('inventory_part_transactions.html', transactions=transactions)

@inventory_blueprint.route('/inventory/loc/<string:inv_loc>')
@login_required
def inv_by_loc(inv_loc):
    transactions = inv_repo.get_inventory_list_by_loc()
    inv_locations = inv_repo.get_inventory_location_list()
    return render_template('inventory_loc.html', transactions=transactions, inv_locations=inv_locations)