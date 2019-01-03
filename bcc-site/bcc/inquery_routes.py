from flask import request, render_template, Blueprint
from dataaccess import inquiry_repository
from flask_login import login_required
inquery_blueprint = Blueprint('inquiry', __name__)
inquiry_repo = inquiry_repository.InquiryRepository()

@inquery_blueprint.route('/inquiry', methods=['GET', 'POST'])
@login_required
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

@inquery_blueprint.route('/inquiry/<int:inquiry_id>')
@login_required
def website_inquiry_detail(inquiry_id):
    inquiry=inquiry_repo.get_inquiry_detail(inquiry_id)
    return render_template('inquiry_detail.html', inquiry=inquiry)