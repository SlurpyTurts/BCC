from flask import request, render_template, Blueprint, redirect, url_for
from dataaccess import bom_repository, part_repository
from flask_login import login_required
bom_blueprint = Blueprint('bom', __name__)
bom_repo = bom_repository.BomRepository()
part_repo = part_repository.PartRepository()

@bom_blueprint.route('/bom')
@login_required
def bom_builder_page():
    part_number = request.args.get('part_number')
    levels = request.args.get('levels')
    if part_number and levels:
        bom_items=bom_repo.get_bom_of_parent(part_number, int(levels))
        print('number of bom items ' + str(len(bom_items)))
        return render_template('bom_search.html', bom_items=bom_items, part_number=part_number, levels=levels)
    return render_template('bom_search.html')

@bom_blueprint.route('/bom/<int:part_number>', methods=['GET','POST'])
@login_required
def bom_tree(part_number):
    if request.method == 'POST':
        child_part_number=request.form['partNumber']
        part_qty=request.form['qty']
        part_ref_des=request.form['refDes']
        if part_ref_des == '' or part_ref_des == 'None':
            part_ref_des = None
        bom_repo.set_new_bom_child(part_number, child_part_number, part_qty, part_ref_des)
        return redirect(url_for('bom.bom_tree', part_number=part_number))
    else:
        if request.args.get('level'):
            levels = request.args.get('level')
        else:
            levels = 1
        parts=bom_repo.get_bom_of_parent(part_number, int(levels))
        part_description=part_repo.get_part_description(part_number)
        return render_template('bom_detail.html', parts=parts, part_number=part_number, part_description=part_description, bom_cost=bom_repo.get_bom_cost(part_number), levels=levels)

@bom_blueprint.route('/bom/<int:parent_part>/<int:child_part>', methods=['GET','POST'])
@login_required
def bom_update(parent_part, child_part):
    if request.method == 'POST':
        quantity=request.form['quantity']
        ref_des=request.form['refDes']
        if ref_des == '' or ref_des == 'None':
            ref_des = None
        bom_repo.update_bom_relationship(parent_part, child_part, quantity, ref_des)
        return redirect(url_for('bom.bom_tree', part_number=parent_part))
    else:
        bom_relationship=bom_repo.get_bom_relationship(parent_part, child_part)
        return render_template('bom_edit.html', bom_relationship=bom_relationship)

@bom_blueprint.route('/delete_bom_relationship/<int:parent>/<int:child>')
@login_required
def delete_bom_relationship(parent, child):
    bom_repo.remove_bom_relationship(parent, child)
    return redirect(url_for('bom.bom_tree', part_number=parent))
