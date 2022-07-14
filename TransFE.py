from audioop import add
from crypt import methods
import email
from datetime import date, datetime, timedelta
from itertools import product
from sqlite3 import dbapi2
from click import DateTime
from flask import Flask,request, Response,g
import sqlite3
from sqlite3 import Error
import requests
import random
import string
import db
app = Flask(__name__)

DB_URL = "database1.db"
@app.before_request
def before_request():
    print("conectando ao banco")
    conn = sqlite3.connect(DB_URL)
    g.conn = conn
@app.teardown_request
def after_request(exception):
    print("vamos fechar a conexão")
    if g.conn is not None:
        g.conn.close()
        print('conexão fechada')


@app.route('/')
def index():
    return "<h1>Start Home</h1>"


#MÉTODOS DE GERAÇÃO DE CÓDIGOS
base_cod = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
size = 10

def cod_generator(size=35, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))





#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE DELIVERY

@app.route('/delivery/store/<int:id>', methods=['GET'])
def getDeliveryStore(id):
    delivery = db.search("delivery","id_store",id)

    result_delivery = [dict((delivery.description[i][0], value) \
       for i, value in enumerate(row)) for row in delivery.fetchall()]
    return {"delivery":result_delivery}, 200



@app.route('/delivery/client/<int:id>', methods=['GET'])
def getDeliveryClient(id):
    delivery = db.search("delivery","id_client",id)

    result_delivery = [dict((delivery.description[i][0], value) \
       for i, value in enumerate(row)) for row in delivery.fetchall()]
    return {"delivery":result_delivery}, 200

@app.route('/delivery/request/<int:id>',methods=['POST'])
def CreatDelivery(id):
    date = datetime.today
    date_delivery = date + timedelta(30)
    status = 0
    shipping= 0

    cursor = db.search("request","id_store",int(id))
    request = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    response = request[0]
    id_store = response["id_store"]
    db.insertDelivery(date,date_delivery,shipping,status,int(id_store),int(id))
    return {"msg":"Delivery OK !"}, 200

@app.route('/delivery/<int:id>', methods=["PUT"])
def putDelivery(id):
    if request.get_json():
        status = request["status"]
        db.updateDelivery(status)
    return "put delivery",200

@app.route('/delivery/<int:id>', methods=["DELETE"])
def deleteDelivery(id):
    db.delete("delivery",int(id))
    return "DELETE delivery"

@app.route('/delivery/<int:id>', methods=["GET"])
def getidDelivery(id):
    cursor = db.search("delivery","id",id)

    delivery = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]

    return {"delivery":delivery}, 200

#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE CLIENTE
@app.route('/client/store/<int:id>',methods=['GET'])
def getClient(id):
    cursor = db.search("client","id_store",id)
    client_dict = [{'name':row[1],'cpf':row[2],'phone':row[3]}
                    for row in cursor.fetchall()]
    return {"client":client_dict}

@app.route('/client/store/<int:id>',methods=['POST'])
def postClient(id):
    if request.get_json:
        client = request.get_json()
        name,cpf,phone = client["name"],client["cpf"],client["phone"]
        db.insertClient(name,cpf,phone,int(id))

        return "Saved successfully !", 201
    return "error: fail to post", 405

@app.route('/client/<int:id>',methods=['PUT'])
def putClient(id):
    if request.get_json:

        client = request.get_json()
        db.updateClient(client["name"],client["cpf"],client["phone"],int(id))        
        return "Update client successfully !", 200
    return   "error: fail to update", 405

@app.route('/client/<int:id>',methods=['DELETE'])
def DELETEClient(id):
    db.delete("client","id",int(id))
    return "destroy client successfully", 200


@app.route('/client/<int:id>',methods=['GET'])
def GETIDClient(id):
    cursor = db.search("client","id",int(id))

    client = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]

    if client:
        return {'client':client}, 200
    return 'error: fail to get',405
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE ENDEREÇO
@app.route('/address/client/<int:id>',methods=['GET'])
def getAddress(id):
    cursor = db.search("address","id_client",int(id))
    address_dict = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"address":address_dict}

@app.route('/address/client/<int:id>',methods=['POST'])
def postAddress(id):
    if request.get_json:
        address = request.get_json()
        locality = address["locality"]
        local = address["local"]
        discrict = address["discrict"]
        number = address["number"]
        cep=address["cep"]
        URL = 'https://ws.apicep.com/cep/{}.json'
        response = requests.get(URL.format(cep))
        city = "NULL"
        state = "NULL"
        if response.status_code == 200:
            response_json = response.json()
            city = response_json["city"]
            state = response_json["state"]
        else:
            city = "não localizado"
            state = "não localizado"
        db.insertAddress(locality,local,discrict,number,int(id),cep,city,state)
        return "Saved successfully !", 201
    return "error: fail to update", 405

@app.route('/address/<int:id>',methods=['PUT'])
def putaddress(id):
    if request.get_json:
        address = request.get_json()
        db.updateAddress(address["locality"],address["local"],address["discrict"],address["number"],address["cep"],int(id))
        URL = 'https://ws.apicep.com/cep/{}.json'
        response = requests.get(URL.format(address["cep"]))
        city = "NULL"
        state = "NULL"
        if response.status_code == 200:
            response_json = response.json()
            city = response_json["city"]
            state = response_json["state"]
        else:
            city = "não localizado"
            state = "não localizado"
        db.updateCityState(city,state) 
        return "Update address successfully !", 200
    return   "error: fail to update", 405

@app.route('/address/<int:id>',methods=['DELETE'])
def DELETEaddress(id):
    db.delete("address","id",int(id))
    return "destroy address successfully", 200

@app.route('/address/<int:id>',methods=['GET'])
def GETidaddress(id):
        cursor = db.search("address","id",int(id))
        address = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
        return {'address':address} , 200

#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE PRODUTO
@app.route('/products/store/<int:id>',methods=['GET'])
def getproducts(id):
    cursor = db.search("product","id_store",int(id))
    product_dict = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"products":product_dict}, 200

@app.route('/products/store/<int:id>',methods=['POST'])
def postAdress(id):
        if request.get_json:
            product = request.get_json()
            name = product["name"]
            unitary_value = product["unitary_value"]
            Weigth = product["weigth"]
            db.insertProduct(name,unitary_value,Weigth,int(id))
            return "Saved successfully !", 201
        return "error: fail to post", 405

@app.route('/products/<int:id>',methods=['PUT'])
def putproducts(id):
    if request.get_json:
        product  = request.get_json();
        db.updateProduct(product["name"],product["unitary_value"],product["weigth"])
        return "Update product successfully !", 200
    return   "error: fail to update", 405

@app.route('/products/<int:id>',methods=['DELETE'])
def DELETEproducts(id):
    db.delete("product","id",int(id))
    return "destroy product successfully", 200     
    

@app.route('/products/<int:id>',methods=['GET'])
def GETidproducts(id):
    cursor = db.search("product","id",int(id))
    product = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"products":product}, 200

#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE LOJA

@app.route('/store',methods=['GET'])
def getstore():
    cursor = db.storeAll()
    store_dict = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"store":store_dict}

@app.route('/store',methods=['POST'])
def poststore():
    if request.get_json:
        store = request.get_json()
        name = store["name"]
        cnpj = store["cnpj"]
        email = store["email"]
        db.insertStore(name,cnpj,email)
        return "Saved successfully !", 201
    return {"error: fail to save"}, 405

@app.route('/store/<int:id>',methods=['PUT'])
def putstore(id):
    if request.get_json:
        store = request.get_json()
        db.updateStore(store["name"],store["cnpj"],store["email"], int(id))
        return "Update Store successfull", 200
    return   "error: fail to update", 405

@app.route('/store/<int:id>',methods=['DELETE'])
def DELETEstore(id):
    db.delete("store","id",int(id))
    return "destroy store successfully", 200

@app.route('/store/<int:id>',methods=['GET'])
def GETidstore(id):
    cursor = db.search("store","id",int(id))
    store = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]

    return {'store':store}, 200
    

#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE RASTREIO

@app.route('/tracking/request/<int:id>',methods=['GET'])
def gettracking(id):
    result = db.search("tracking","id_request",id)
    tracking = [dict((result.description[i][0], value) \
       for i, value in enumerate(row)) for row in result.fetchall()]
    return {"tracking":tracking}

@app.route('/tracking/request/<int:id>',methods=['POST'])
def posttracking(id):
    cod = cod_generator(size,base_cod)
    db.insertTracking(cod,int(id))
    return "POST tracking", 200

@app.route('/tracking/<int:id>',methods=['PUT'])
def puttracking(id):
    return "put tracking"

@app.route('/tracking/<int:id>',methods=['DELETE'])
def DELETEtracking(id):
    db.delete("tracking","id",int(id))
    return "DELETEtracking"

@app.route('/tracking/<int:id>',methods=['GET'])
def GETidtracking(id):
    cursor = db.search("tracking","id",id)
    tracking = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"tracking":tracking}

#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE PEDIDO

@app.route("/request/client/<int:id>", methods =["GET"])
def GetRequest(id):
    cursor = db.search("request","id_client",id)
    request_client = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"request":request_client}, 200


@app.route("/request/client/<int:id>", methods=["POST"])
def PostRequest(id):
    client = db.search("client","id",int(id))
    request_client = [dict((client.description[i][0], value) \
       for i, value in enumerate(row)) for row in client.fetchall()]
    client = request_client[0]
    id_store = client["id_store"]
    db.insertRequest(int(id),int(id_store))
    return "Salve ok!", 200
     
@app.route("/request/<int:id>", methods=["GET"])
def  GetResquetID(id):
        cursor = db.search("request","id",id)
        search = [{'id':row[0],'cod':row[1],'id_client':row[2],'id_delivery':row[3],'id_store':row[4]}
                    for row in cursor.fetchall()]
        return {"request":search}, 200


#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
            #MÉTODOS DE PEDIDO_PRODUTO

@app.route("/request/products/<int:id_request>/<int:id_product>", methods=["POST"])
def request_product(id_request, id_product):
    if request.get_json:
        quantity = request.get_json()
        db.insertRequest_Product(int(id_request),int(id_product),quantity["quantity"])
        return "Salve ok!", 200
    return "fail!",405

if __name__ =='__main__':
    app.run(debug=True, host="0.0.0.0",port=8090)





