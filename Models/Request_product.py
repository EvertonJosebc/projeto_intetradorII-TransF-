from requests import request
from config import db
from flask import jsonify
class Request_product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_request = db.Column(db.Integer,db.ForeignKey('request.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

    def return_json(self):
        return {
            "id_request":self.id_request,
            "id_product":self.id_product,
            "quantity":self.quantity

        }

#insert Request_product
    def insert(Request_product):
        db.session.add(Request_product)
        db.session.commit()
        return 201



#all Request_product
    def get_all(id_store):
        request_product = Request_product.query.filter_by(id_store=id_store).all()
        if request_product is not None:
            return jsonify([rp.return_json() for rp in request_product])
        return 405



#id Request_product get
    def get_id(id):
        request_product = Request_product.query.get(id).first()
        if request_product is not None:
            return jsonify(request_product.return_json())
        return 405
#update Request_product
    def update(Request_product):
        db.session.add(Request_product)
        db.session.commit()
        return 200



#delete Request_product

    def delete(Request_product,self):
        self.update(Request_product)
        return 200