import math
from flask import render_template, Blueprint, redirect, url_for, request
from dataaccess import part_repository
parts_blueprint = Blueprint('parts', __name__)
part_repo = part_repository.PartRepository()

@parts_blueprint.route('/parts')
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

@parts_blueprint.route('/parts/new', methods=['GET','POST'])
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
        return redirect(url_for('parts.part_detail', part_number=part_type+part_number))
    else:
        return render_template('part_new.html', part_status_list=part_repo.get_part_status_list(), part_unit_list=part_repo.get_part_unit_list(), part_type_list=part_repo.get_part_type_list(), part_family_list=part_repo.get_part_family_list())

@parts_blueprint.route('/parts/<int:part_number>/update', methods=['GET','POST'])
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
        return redirect(url_for('parts.part_detail', part_number=part_number))
    else:
        part_unit = part_repo.get_part_unit_list()
        part_status = part_repo.get_part_status_list()
        part = part_repo.get_part_by_part_number(part_number)
        return render_template('part_update.html', part_unit=part_unit, part=part, part_status=part_status)






