"""Recharge model."""
from model.tools import Tools
from bson import ObjectId


class Recharge(object):
    """docstring for recharge."""

    def __init__(self, recharge_id=None, created_at=None, company_id=None,
                 product_id=None, phone_number=None, value=None):
        """Constructor."""
        self._id = recharge_id
        self._created_at = created_at
        self._company_id = company_id
        self._product_id = product_id
        self._phone_number = phone_number
        self._value = value

    def get_recharge_id(self):
        """get."""
        return self._id

    def get_created_at(self):
        """get."""
        return self._created_at

    def get_company_id(self):
        """get."""
        return self._company_id

    def get_product_id(self):
        """get."""
        return self._product_id

    def get_phone_number(self):
        """get."""
        return self._phone_number

    def get_value(self):
        """get."""
        return self._value


class FactoryRecharge():
    """Racharge factory."""

    tools = Tools()

    def loadrecharge(self, db, recharge_id=None, phone_number=None):
        """Load object from database."""
        # Search data from data
        if recharge_id:
            recharges = db['recharges'].find(
                {"_id": ObjectId("%s" % recharge_id.strip())})
        else:
            recharges = db['recharges'].find(
                {"phone_number": phone_number.strip()})
        return_temp = []
        for i in recharges:
            # Create list of objectes from database
            return_temp.append(Recharge(
                recharge_id=str(i['_id']).
                replace("ObjectId('", '').replace("'", ''),
                created_at=i['created_at'].strftime("%d/%m/%Y, %H:%M:%S"),
                company_id=i['company_id'],
                product_id=i['product_id'],
                phone_number=i['phone_number'],
                value=i['value']))
        return return_temp

    def recharge_to_json(self, recharges=[]):
        """Convert to json."""
        return_list = []
        # build dict from object
        for c in recharges:
            dic = {
                "id": c.get_recharge_id(),
                "created_at": c.get_created_at(),
                "company_id": c.get_company_id(),
                "product_id": c.get_product_id(),
                "phone_number": c.get_phone_number(),
                "value": c.get_value()
            }
            return_list.append(dic)
        # convert dict to json
        return self.tools.convert_data(return_list)

    def new_recharge(
            self, created_at=None, company_id=None,
            product_id=None, phone_number=None, value=None):
        """Build object."""
        return Recharge(
            created_at=created_at,
            company_id=company_id,
            product_id=product_id,
            phone_number=phone_number,
            value=value)

    def insert(self, db, recharge):
        """Insert object in database."""
        recharge_insert = {
            "created_at": recharge.get_created_at(),
            "company_id": recharge.get_company_id(),
            "product_id": recharge.get_product_id(),
            "phone_number": recharge.get_phone_number(),
            "value": recharge.get_value(),
        }

        result = db['recharges'].insert_one(recharge_insert).inserted_id
        return self.loadrecharge(db, recharge_id=str(result))
        # return json.dumps({"id": str(result)})
