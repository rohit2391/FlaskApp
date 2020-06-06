import pandas as pd
from flask import Flask, request, Blueprint, render_template

banking_page = Blueprint('banking_page', __name__, template_folder='templates')

@insurance_page.route('/bank')
def bank_landing_page():
    return render_template("bank_home.html")