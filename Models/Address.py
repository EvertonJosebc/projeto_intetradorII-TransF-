from audioop import add
from config import db
from flask import jsonify,request
import requests

class Address(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    locality = db.Column(db.String(50))
    local = db.Column(db.String(50))
    district = db.Column(db.String(50))
    number = db.Column(db.String(50))   
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))
    cep = db.Column(db.String(10))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    status_activate  = db.Column(db.Integer)

#return Address
    def return_json(self):
        return{
            "id": self.id,
            "locality": self.locality,
            "local": self.local,
            "district": self.district,
            "number": self.number,
            "id_client": self.id_client,
            "cep": self.cep,
            "city": self.city,
            "state": self.state,
            "status_activate": self.status_activate
        }
#insert Address
    def insert(address):
        db.session.add(address)
        db.session.commit()
        return 201
#all Address
    def get_all(id_client):
        address = Address.query.filter_by(id_client=id_client).all()
        if address is not None:
            return jsonify([a.return_json() for a in address])
        return 405
#id Address get
    def get_id(id):
        address = Address.query.get(id)
        if address is not None:
            return jsonify(address.return_json())
        return 405
#update Address
    def update(id):
        address = Address.query.get(id)
        if address is not None:
            if request.is_json:
                addressJson = request.get_json()
                if("locality" in addressJson):
                    address.locality = addressJson['locality']
                if("local" in addressJson):
                    address.local = addressJson['local']
                if("district" in addressJson):
                    address.district = addressJson['district']
                if("cep" in addressJson):
                    address.cep = addressJson['cep']
                    URL = 'https://ws.apicep.com/cep/{}.json'
                    cep = addressJson['cep']
                    response = requests.get(URL.format(cep))
                    if response.status_code == 200:
                        responseJson = response.json()
                        address.city =  responseJson['city']
                        address.state = responseJson['state']
                    else:
                        address.city =  "not Found"
                        address.state = "not Found"
                db.session.add(address)
                db.session.commit()
                return 200
            return 415
        return 405

                
#delete Address

    def delete(id):
        address = Address.query.get(id);
        if address is not None:
            address.status_activate = 0
            db.session.add(address)
            db.session.commit()
            return 200
        return 405






    def json_return(self):
        return {
            "id" : self.id,
            "locality": self.locality,
            "local": self.local,
            "district": self.district,
            "number": self.number,
            "id_client": self.id_client,
            "cep": self.cep,
            "city": self.city,
            "state": self.state,
            "status_activate": self.status_activate
        }
