import pandas as pd
from flask import Flask, request, Blueprint, render_template

insurance_page = Blueprint('insurance_page', __name__, template_folder='templates')


@insurance_page.route('/calculatePremium')
def insurance_premium_cal():
    return render_template("premium_calculator.html")

@insurance_page.route('/')
def insurance_landing_page():
    return render_template("insurance_home.html")

