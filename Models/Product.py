from itertools import product
from config import db
from flask import jsonify,request

class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50), nullable = True)
    unitary_value = db.Column(db.Float)
    weigth = db.Column(db.Float)
    id_store = db.Column(db.Integer,db.ForeignKey('store.id'))
    status_activate = db.Column(db.Integer)

    def return_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'unitary_value': self.unitary_value,
            'weigth': self.weigth,
            'id_store': self.id_store,
            'status_activate': self.status_activate }
    
    #insert Product
    def insert(Product):
        db.session.add(Product)
        db.session.commit()
        return 201


#all Product
    def get_all(id_store):
        product = Product.query.filter_by(id_store=id_store).all()
        if Product is not None:
            return jsonify([p.return_json() for p in product])
        return 405


#id Product get
    def get_id(id):
        product = Product.query.get(id)
        if product is not None:
            return jsonify(product.return_json())
        return 405


#uProductdate Product
    def update(id):
        product = Product.query.get(id)
        if product is not None:
            if request.is_json:
                productJson = request.get_json()
                if('name' in productJson):
                    product.name = productJson['name']
                if('unitary_value' in productJson):
                    product.unitary_value = productJson['unitary_value']
                if('weigth' in productJson):
                    product.weigth = productJson['weigth']
                
                db.session.add(product)
                db.session.commit()
                return 200
            return 415
        return 405


#delete Product
    def delete(id):
        product = Product.query.get(id)
        if product is not None:
            product.status_activate = 0
            db.session.add(product)
            db.session.commit()
            return 200
        return 405