"""Jeito teste pratico."""
from pymongo import MongoClient
import os
from flask import Flask, request, session, jsonify
import re
import json
from bson import ObjectId
import datetime
from model.company import FactoryCompany
from model.recharges import FactoryRecharge

# creating app
app = Flask(__name__)

# start connection to database
client = MongoClient('localhost', 27017)
db = None
faccomp = FactoryCompany()
facrec = FactoryRecharge()

def reset_database():
    """Reset database on startup."""
    client.drop_database('jeitto_db')

    db = client['jeitto_db']

    companys_collection = db['companys']

    companys = [
        {
            "company_id": "claro_11",
            "products":[
                {"id": "claro_10", "value": 10.0},
                {"id": "claro_20", "value": 20.0}
            ]
        },
        {
            "company_id": "tim_11",
            "products":[
                {"id": "tim_10", "value": 10.0},
                {"id": "tim_20", "value": 20.0}
            ]
        }
    ]

    result = companys_collection.insert_many(companys).inserted_ids
    if not result:
        return 'Failed'
    return db

@app.route("/", methods=['GET'])
def home():
    """Home page."""
    return "Hello World"


@app.route("/CompanyProducts", methods=['GET'])
def company_products():
    company = request.args.get('company_id', None)
    # load object from database
    companys = faccomp.loadCompany(db, company_id=company)
    # convert object to json
    companys = faccomp.company_to_json(companys)
    return companys

@app.route("/PhoneRecharges", methods=['POST'])
def phone_recharge_post():
    form = request.json
    company = []
    product = []
    # check for company_id in the form
    if "company_id" in form.keys():
        company = faccomp.loadCompany(db, company_id=form["company_id"])
    else:
        return 'Invalid company'
    if company and "product_id" in form.keys():
        # list the product ids
        products_id = [x["id"] for x in company[0].get_products()]
        # check if the product id is on form
        if form["product_id"] in products_id:
            for x in company[0].get_products():
                # save product if it exist in the companny
                if form["product_id"] in x["id"]:
                    product = x
        else:
            return 'Invalid product'
    else:
        return 'Invalid company'
    if product and "value" in form.keys():
        # check if value is the same as the product
        if not (float(product['value']) == float(form['value'])):
            return "Wrong value"

    # check phone number
    if not form.get('phone_number', None):
        return "Invalid phone"

    # take only from the phone number
    phone = ''.join([x for x in form["phone_number"] if x.isdigit()])
    # check if it has the right length 
    if not (phone and len(phone) == 13):
        return "Invalid phone"

    # create new object with form data
    recharge = facrec.new_recharge(
        company_id=form["company_id"],
        product_id=form["product_id"],
        phone_number=phone,
        value=float(form["value"]),
        created_at=datetime.datetime.utcnow()
    )
    # persist in database
    result = facrec.insert(db, recharge)
    # return json to user
    return json.dumps({"id": result[0].get_recharge_id()})

@app.route("/PhoneRecharges", methods=['GET'])
def phone_recharge_get():
    phone_number = request.args.get('phone_number', None)
    recharge_id = request.args.get('id', None)

    # check if some of parameters were passed in request
    if not(phone_number or recharge_id):
        return "Error"

    # recreate object from data
    rec = facrec.loadrecharge(db, recharge_id=recharge_id, phone_number=phone_number)

    # convert to json
    rec = facrec.recharge_to_json(recharges=rec)
    return rec


if __name__ == "__main__":
    db = reset_database()
    app.run(debug=True)