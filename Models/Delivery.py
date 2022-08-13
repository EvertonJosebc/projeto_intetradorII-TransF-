from config import db
from flask import jsonify,request
from datetime import date, datetime, timedelta
from click import DateTime
from .Request import Request

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    date_delivery = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    id_request = db.Column(db.Integer, db.ForeignKey('request.id'))
    id_store = db.Column(db.Integer, db.ForeignKey('store.id'))
    id_address = db.Column(db.Integer, db.ForeignKey('address.id'))
    shipping_value = db.Column(db.Float)

    def json_return(self):
       return { "id" : self.id,
        "date" : self.date,
        "date_delivery" : self.date_delivery,
        "status" : self.status,
        "id_request" : self.id_request,
        "id_store" : self.id_store,
        "id_address": self.id_address,
        "shipping_value" : self.shipping_value 
       }

#insert Delivery
    def insert(id_request,id_address):
        if request.is_json:
            deliveryJson = request.get_json()
            requestStore = Request.query.get(id_request)
            delivery = Delivery(
                date = datetime.today(),
                date_delivery = datetime.today() + timedelta(30),
                id_request = id_request,
                id_address = id_address,
                id_store = requestStore.id_store,
                shipping_value= deliveryJson['shipping_value']
                )
            db.session.add(delivery)
            db.session.commit()
            return 201
        return 405
#all Delivery
    def get_all(id_request):
        delivery = Delivery.query.filter_by(id_request=id_request).all()
        if delivery is not None:
            return jsonify([d.json_return() for d in delivery])
        return 405
#id Delivery get
    def get_id(id):
        delivery = Delivery.query.get(id)
        if delivery is not None:
            return jsonify(delivery.json_return())
        return 405
#update Delivery
    def update(id_delivery,id_address):
        delivery = Delivery.query.get(id_delivery)
        delivery.id_address = id_address
        db.session.add(delivery)
        db.session.commit()
        
#delete Delivery

    def delete(id):
        delivery = Delivery.query.get(id)
        if delivery is not None:
            delivery.status_activate = 0
            db.session.add(delivery)
            db.session.commit()
            return 200
        return 405
