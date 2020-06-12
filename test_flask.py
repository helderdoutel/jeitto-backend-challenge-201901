from unittest.mock import Mock
import unittest
import main
from model import company, recharges
import json
import datetime

main.request = Mock()
main.db = {}
main.db['companys'] = Mock()
main.db['recharges'] = Mock()
main.db['recharges'].find.return_value = [{
    "_id": "ObjectId('5ee17afd7ba2c152b796d37c')", 
    "created_at": datetime.datetime.utcnow(), 
    "company_id": "claro_11", 
    "product_id": "claro_20", 
    "phone_number": "5511999999999", 
    "value": 20.00}]
main.db['companys'].find.return_value = [
    {
        "company_id": "claro_11",
        "products":[
            {"id": "claro_10", "value": 10.0},
            {"id": "claro_20", "value": 20.0}
        ]
    }
]
# main.faccomp = Mock()
# main.facrec = Mock()

def test_company_products():
    main.request.arg.return_value = {'company_id': 'tim_11'}
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
    assert isinstance(main.company_products(), str)

def phone_recharge_post(product_id, phone_number, value):
    main.request.json = {
        "company_id": "claro_11",
        "product_id": product_id,
        "phone_number": phone_number,
        "value": value
    }
    
    temp = Mock()
    temp.inserted_id = "5ee17afd7ba2c152b796d37c"
    main.db['recharges'].insert_one.return_value = temp
    print(main.phone_recharge_post())
    try:
        return json.loads(main.phone_recharge_post())
    except:
        return {}

def test_phone_recharge_post():
    assert 'id' in phone_recharge_post(
        product_id="claro_20", phone_number="5511999999999", value=20.00).keys()
    assert not 'id' in phone_recharge_post(
        product_id="claro_21", phone_number="5511999999999", value=20.0).keys()
    assert not 'id' in phone_recharge_post(
        product_id="claro_20", phone_number="5511999999999", value=21.0).keys()
    assert not 'id' in phone_recharge_post(
        product_id="claro_20", phone_number="55119999999", value=20.0).keys()

def test_phone_recharge_get():

    
    main.request.args = {'id': '5ee17afd7ba2c152b796d37c', 'phone_number': '5511999999999'}
    main.facrec = recharges.FactoryRecharge()
    print(main.phone_recharge_get())

