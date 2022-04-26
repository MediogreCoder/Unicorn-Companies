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


db.connect()
db.drop_tables([Companies])
db.create_tables([Companies])

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
app.run(debug=True)
