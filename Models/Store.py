from unicodedata import name
from config import db
from flask import jsonify,request

class Store(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50))
    cnpj = db.Column(db.String(50))
    email = db.Column(db.String(50))
    status_activate = db.Column(db.Integer)

    def return_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'cnpj': self.cnpj,
            'email': self.email,
            'status_activate': self.status_activate}

#insert Store
    def insert(Store):
        db.session.add(Store)
        db.session.commit()
        return 201
        
#all Store
    def get_all():
        store = Store.query.all()
        if store is not None:
            return jsonify([s.return_json() for s in store])
        return 405
#id Store get
    def get_id(id):
        store = Store.query.get(id)
        if store is not None:
            return jsonify(store.return_json())
        return 405
#update Store
    def update(id):
        store = Store.query.get(id)
        if store is not None:
            if request.is_json:
                storeJson = request.get_json()
                if ("name" in storeJson):
                    store.name = storeJson['name']
                if ("cnpj" in storeJson):
                    store.cnpj = storeJson['cnpj']
                if ("email" in storeJson):
                    store.email = storeJson['email']
                db.session.add(store)
                db.session.commit()
                return 200
            return 415
        return 405

#delete Store

    def delete(id):
        store = Store.query.get(id);
        if store is not None:
            store.status_activate = 0
            db.session.add(store)
            db.session.commit()
            return 200
        return 405