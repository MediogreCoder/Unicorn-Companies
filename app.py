from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('unicorn_companies', user='em',
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Companies(BaseModel):
    name = CharField()
    valuation = IntegerField()
    industry = CharField()
    country = CharField()
    year_founded = IntegerField()


class Industry(BaseModel):
    name = CharField()
    market_value = IntegerField()


db.connect()
db.drop_tables([Companies])
db.create_tables([Companies])
db.drop_tables([Industry])
db.create_tables([Industry])

Industry(name='Fintech', market_value=305).save()
Industry(name='Artifical Intelligence', market_value=93.5).save()
Industry(name='Supply chain, logistics, & delivery', market_value=156).save()
Industry(name='Internet software & services', market_value=429.59).save()
Industry(name='E-commerce & direct-to-consumer', market_value=10361).save()

Companies(name='ByteDance', valuation=140, industry='Artificial Intelligence',
          country='China', year_founded=2012).save()
Companies(name='Stripe', valuation=95, industry='Fintech',
          country='Sweden', year_founded=2010).save()
Companies(name='Instacart', valuation=39, industry='Supply chain, logistics, & delivery',
          country='China', year_founded=2012).save()
Companies(name='Figma', valuation=10, industry='Internet software & services',
          country='United States', year_founded=2012).save()
Companies(name='reddit', valuation=10, industry='Internet software & services',
          country='United States', year_founded=2005).save()
Companies(name='Epic Games', valuation=42, industry='Internet software & services',
          country='United States', year_founded=1991).save()
Companies(name='OpenSea', valuation=13, industry='E-commerce & direct-to-consumer',
          country='United States', year_founded=2017).save()
Companies(name='Postman', valuation=5.6, industry='Internet software & services',
          country='United States', year_founded=2014).save()

app = Flask(__name__)


@app.route('/')
def index():
    return "Check out our Unicorn Companies API!"


@app.route('/companies/', methods=['GET', 'POST'])
@app.route('/companies/<name>', methods=['GET', 'PUT', 'DELETE'])
def comp(name=None):
    if request.method == 'GET':
        if name:
            return jsonify(model_to_dict(Companies.get(Companies.name == name)))
        else:
            companyList = []
            for company in Companies.select():
                companyList.append(model_to_dict(company))
            return jsonify(companyList)

    if request.method == 'PUT':
        req = request.get_json()
        Companies.update(req).where(Companies.name == name).execute()
        return jsonify(model_to_dict(Companies.get(Companies.name == name)))

    if request.method == 'POST':
        new_company = dict_to_model(Companies, request.get_json())
        new_company.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        return jsonify(Companies.get(Companies.name == name).delete_instance())


@app.route('/industry/', methods=['GET', 'POST'])
@app.route('/industry/<name>', methods=['GET', 'PUT', 'DELETE'])
def indus(name=None):
    if request.method == 'GET':
        if name:
            return jsonify(model_to_dict(Industry.get(Industry.name == name)))
        else:
            industryList = []
            for industry in Industry.select():
                industryList.append(model_to_dict(industry))
            return jsonify(industryList)

    if request.method == 'PUT':
        req = request.get_json()
        Industry.update(req).where(Industry.name == name).execute()
        return jsonify(model_to_dict(Industry.get(Industry.name == name)))

    if request.method == 'POST':
        new_industry = dict_to_model(Industry, request.get_json())
        new_industry.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        return jsonify(Industry.get(Industry.name == name).delete_instance())


app.run(debug=True)
