"""Jeito teste pratico."""
from pymongo import MongoClient
import os
from flask import Flask, request, session, jsonify
import re
import json
from bson import ObjectId
import datetime

# creating app
app = Flask(__name__)

# start connection to database
client = MongoClient('localhost', 27017)
db = None

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
        raise Exception('Failed')
    return db

def convert_data(input_query, return_id=False, json_render=True):
    """Returns json."""
    if isinstance(input_query, dict):
        input_query = [input_query]
    temp_data = []
    for data in input_query:
        if not return_id:
            del data['_id']
        else:
            data["id"] = str(data['_id']).replace("ObjectId('", '').replace("'", '')
            del data['_id']
        for k in data.keys():
            if isinstance(data[k], datetime.datetime):
                data[k] = data[k].strftime("%d/%m/%Y, %H:%M:%S")
        temp_data.append(data)
    if json_render:
        print("Aqui2", temp_data)
        return json.dumps(temp_data)
    return temp_data

def find_company(company_id=None, json_render=True):
    """."""
    if company_id:
        companys = db['companys'].find({"company_id": company_id})
    else:
        companys = db['companys'].find({})
    return_temp = []
    for i in companys:
        return_temp.append(i)
    return convert_data(return_temp, json_render=json_render)


@app.route("/", methods=['GET'])
def home():
    """Home page."""
    return "Hello World"


@app.route("/CompanyProducts", methods=['GET'])
def company_products():
    company = request.args.get('company_id', None)
    return find_company(company)

@app.route("/PhoneRecharges", methods=['POST'])
def phone_recharge_post():
    form = request.json
    print(form)
    recharges_collection = db['recharges']

    company = []
    product = []
    if "company_id" in form.keys():
        company = find_company(form["company_id"], json_render=False)
        print(company)
    else:
        raise Exception('Invalid company')
    if company and "product_id" in form.keys():
        products_id = [x["id"] for x in company[0]["products"]]
        if form["product_id"] in products_id:
            for x in company[0]["products"]:
                if form["product_id"] in x["id"]:
                    product = x
        else:
            raise Exception('Invalid product')
    else:
        raise Exception('Invalid company')
    if product and "value" in form.keys():
        if not (float(product['value']) == float(form['value'])):
            raise Exception("Wrong value")

    if not form.get('phone_number', None):
        raise Exception("Invalid phone")

    phone = ''.join([x for x in form["phone_number"] if x.isdigit()])
    if not (phone and len(phone) == 13):
        raise Exception("Invalid phone")
    recharge = {
        "company_id": form["company_id"],
        "product_id": form["product_id"],
        "phone_number": phone,
        "value": float(form["value"]),
        "created_at": datetime.datetime.utcnow()
    }

    result = recharges_collection.insert_one(recharge).inserted_id
    return json.dumps({"id": str(result)})

@app.route("/PhoneRecharges", methods=['GET'])
def phone_recharge_get():
    phone_number = request.args.get('phone_number', None)
    recharge_id = request.args.get('id', None)

    if not(phone_number or recharge_id):
        raise Exception("Error")

    if recharge_id:
        recharges = db['recharges'].find({"_id": ObjectId("%s" % recharge_id.strip())})
    else:
        recharges = db['recharges'].find({"phone_number": phone_number.strip()})
    return_temp = []
    for i in recharges:
        print(i)
        return_temp.append(i)
    print("aqui", return_temp)
    return convert_data(return_temp, return_id=True)


if __name__ == "__main__":
    db = reset_database()
    app.run()