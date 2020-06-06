import pandas as pd
import numpy as np
import statsmodels

from flask import Flask, request, Blueprint, render_template
import pickle

simple_page = Blueprint('simple_page', __name__, template_folder='templates')
# @simple_page.route('/<page>')

regression_model = pickle.load(open('./RegressionModel.pkl', 'rb'))

app = Flask(__name__)


@app.route("/getPremium1")
def predictPremium():
    age = request.args.get('age', type=int)
    bmi = request.args.get('bmi', type=int)
    children = request.args.get('children', type=int)
    gender = request.args.get('gender')
    smoker = request.args.get('smoker')
    region = request.args.get('region')

    insurance = pd.DataFrame([[age, bmi, children, gender, smoker, region]],
                             columns=['age', 'bmi', 'children', 'gender', 'smoker', 'region'])
    insurance = pd.get_dummies()

    missing_col = set(
        ['const', 'age', 'bmi', 'children', 'gender_female', 'gender_male', 'smoker_no', 'smoker_occasionally',
         'smoker_yes', 'region_northeast', 'region_northwest', 'region_southeast', 'region_southwest']) - set(
        insurance.columns)
    for col_name in missing_col:
        insurance[col_name] = 0
    print(insurance)
    predicted_premium = regression_model.predict(insurance)
    return str(predicted_premium[0])


linear_regression = pickle.load(open('./linear_regression.pkl', 'rb'))


@simple_page.route('/getTestLinear1')
# @app.route("/getTestLinear1")
def testLinear1():
    const =1
    age=80
    sex=0
    bmi=27
    children = 5
    smoker =1
    region =2
    insuranceclaim=1

    # age = request.args.get('age', type=int)
    # bmi = request.args.get('bmi', type=int)
    # children = request.args.get('children', type=int)
    # gender = request.args.get('gender')
    # smoker = request.args.get('smoker')
    # region = request.args.get('region')
    insurance = pd.DataFrame([[const, age, sex, bmi, children, smoker, region, insuranceclaim]],
                             columns=['const', 'age', 'sex', 'bmi', 'children', 'smoker', 'region', 'insuranceclaim'])
    print(insurance)
    predicted_premium = linear_regression.predict(insurance)
    return str(predicted_premium[0])

# @simple_page.route("/getPremium1")
# def ReturnPremium1():
#     #return  render_template('premium_details.html')
#     # premium = request.args.get('premium',type=int)
#     # revised_premium = premium-(0.1*premium)
#     #
#     #premium = request.form['premium_val']
#     #return "New Premium is: "+ str(premium)
#     return render_template('premium_details.html')



if __name__ == "__main__":
    app.run(debug=True)
