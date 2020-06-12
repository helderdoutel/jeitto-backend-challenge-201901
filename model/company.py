"""Company model."""
from model.tools import Tools


class Company(object):
    """docstring for Company."""

    def __init__(self, company_id=None, products=[]):
        """Class constructor."""
        self.company_id = company_id
        self.products = products

    def get_company_id(self):
        """get."""
        return self.company_id

    def get_products(self):
        """get."""
        return self.products


class FactoryCompany():
    """Campany factory."""

    tools = Tools()

    def load_company(self, db, company_id=None):
        """Load company object."""
        if company_id:
            companys = db['companys'].find({"company_id": company_id})
        else:
            companys = db['companys'].find({})
        return_temp = []
        for i in companys:
            return_temp.append(
                Company(company_id=i['company_id'], products=i['products']))
        return return_temp

    def company_to_json(self, companys=[]):
        """Convert object to json."""
        return_list = []
        for c in companys:
            dic = {
                'company_id': c.get_company_id(),
                'products': c.get_products()
            }
            return_list.append(dic)
        return self.tools.convert_data(return_list)
