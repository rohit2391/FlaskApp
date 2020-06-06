from flask import Flask, render_template, request,jsonify
import pandas as pd
import numpy as np
import statsmodels
import pickle

from deploymodel import simple_page
from insurance import insurance_page
app = Flask(__name__)
app.register_blueprint(simple_page)
app.register_blueprint(insurance_page)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'

premium = 1000
premium_val = premium-(0.1*premium)

# @app.route('/', methods=['GET'])
# def getPremiumResult():
#     return render_template('insurance_home.html')



# @app.route('/news', methods=['GET'])
# def news_page_landing():
#     return render_template('index2.html')

@app.route("/getPremium")
def ReturnPremium():
    premium = request.args.get('premium',type=int)
    revised_premium = premium-(0.1*premium)
    return "New Premium is: "+ str(revised_premium)

@app.route("/getPremium1")
def ReturnPremium1():
    premium = request.args.get('premium_val', type=int)
    premium_val = str(premium)
    return render_template('premium_details.html', premium_val=premium_val)

###### Logic for Calculate Premium   ########


@app.route('/calculatePremium1')
def insurance_premium_cal():
    return render_template("premium_calculator.html")


@app.route("/getPremiumResult")
def PremiumResult():
    const = request.args.get('const', type=int)
    # const = str(const)

    age = request.args.get('age', type=int)
    # age = str(age)

    sex = request.args.get('sex', type=int)
    # sex = str(sex)

    bmi = request.args.get('bmi', type=int)
    # bmi = str(bmi)

    children = request.args.get('children', type=int)
    # children = str(children)

    smoker = request.args.get('smoker', type=int)
    # smoker = str(smoker)

    region = request.args.get('region', type=int)
    # region = str(region)

    insuranceclaim = request.args.get('insuranceclaim', type=int)
    # insuranceclaim = str(insuranceclaim)

    insurance = pd.DataFrame([[const, age, sex, bmi, children, smoker, region, insuranceclaim]],
                             columns=['const', 'age', 'sex', 'bmi', 'children', 'smoker', 'region', 'insuranceclaim'])
    print(insurance)
    predicted_premium = linear_regression.predict(insurance)
    print(predicted_premium)
    predicted_premium = str(predicted_premium[0])
    # return render_template('premium_details.html', const=const, age=age, sex=sex, bmi=bmi, children=children, smoker=smoker, region=region)
    return render_template('premium_details.html',predicted_premium=predicted_premium)

##############################################

regression_model = pickle.load(open('./RegressionModel.pkl', 'rb'))


@app.route("/getTestPremium")
def testPremium():
    age = request.args.get('age', type=int)
    bmi = request.args.get('bmi', type=int)
    children = request.args.get('children', type=int)
    gender = request.args.get('gender')
    smoker = request.args.get('smoker')
    region = request.args.get('region')
    insurance = pd.DataFrame([[age, bmi, children, gender, smoker, region]],
                             columns=['age', 'bmi', 'children', 'gender', 'smoker', 'region'])
    insurance = pd.get_dummies(insurance)
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


@app.route("/getTestLinear")
def testLinear():
    const =1
    age=10
    sex=0
    bmi=27
    children = 2
    smoker =1
    region =3
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


if __name__ == '__main__':
    app.run()
