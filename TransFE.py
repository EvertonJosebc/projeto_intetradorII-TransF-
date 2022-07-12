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
app = Flask(__name__)

#funções para abrir e fechar o banco

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

#MÉTODO PARA EXECUTAR COMMITS NO BANCO

def commitdb(query):
    cursor = g.conn.cursor()
    cursor.execute(query)
    g.conn.commit()


#MÉTODOS PARA PESQUISAR NO BANCO

def search(table,column, value):
    query = """
    SELECT * FROM {} WHERE {} = {};
    """.format(table,column,value)
    cursor = g.conn.execute(query)
    return cursor


#MÉTODOS DE DELIVERY

@app.route('/delivery/store/<int:id>', methods=['GET'])
def getDeliveryStore(id):
    delivery = search("delivery","id_store",id)

    result_delivery = [dict((delivery.description[i][0], value) \
       for i, value in enumerate(row)) for row in delivery.fetchall()]
    return {"delivery":result_delivery}, 200



@app.route('/delivery/client/<int:id>', methods=['GET'])
def getDeliveryClient(id):
    delivery = search("delivery","id_client",id)

    result_delivery = [dict((delivery.description[i][0], value) \
       for i, value in enumerate(row)) for row in delivery.fetchall()]
    return {"delivery":result_delivery}, 200

@app.route('/delivery/request/<int:id>',methods=['POST'])
def CreatDelivery(id):
    date = datetime.today
    date_delivery = date + timedelta(30)
    status = 0
    freiht_value = 0

    cursor = search("request","id_store",int(id))
    request = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    response = request[0]


        

    query = """
    INSERT INTO delivery(date,date_deliver,status,freiht_value,id_store,id_request)
    VALUES({},{},{},{},{});
    """.format(date,date_delivery,status,freiht_value,response["id_store"],id)
    commitdb(query)
    return {"msg":"Delivery OK !"}, 200

@app.route('/delivery/<int:id>', methods=["PUT"])
def putDelivery(id):
    return "put delivery"

@app.route('/delivery/<int:id>', methods=["DELETE"])
def deleteDelivery(id):
    return "DELETE delivery"

@app.route('/delivery/<int:id>', methods=["GET"])
def getidDelivery(id):
    cursor = search("delivery","id",id)

    delivery = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]

    return {"delivery":delivery}, 200






#ÁREA DOS MÉTODOS DO CLIENTE
@app.route('/client/store/<int:id>',methods=['GET'])
def getClient(id):
    query = """
    SELECT * FROM client where id_store = {};
    """.format(id)
    cursor = g.conn.execute(query)
    client_dict = [{'name':row[1],'cpf':row[2],'phone':row[3]}
                    for row in cursor.fetchall()]
    return {"client":client_dict}

@app.route('/client/store/<int:id>',methods=['POST'])
def postClient(id):
    if request.get_json:
        client = request.get_json()
        name,cpf,phone = client["name"],client["cpf"],client["phone"]

        query = """
            INSERT INTO client (name,cpf,phone,id_store)
            VALUES ("{}","{}","{}",{});
        """.format(name,cpf,phone,int(id))
        commitdb(query)
        return "Saved successfully !", 201
    return "error: fail to post", 405

@app.route('/client/<int:id>',methods=['PUT'])
def putClient(id):
    if request.get_json:

        client = request.get_json()
        query = f'UPDATE client SET name = "{client["name"]}", cpf = "{client["cpf"]}", phone = "{client["phone"]}" where id = {id}'
        commitdb(query)
        
        return "Update client successfully !", 200
    return   "error: fail to update", 405

@app.route('/client/<int:id>',methods=['DELETE'])
def DELETEClient(id):
    query = """
        DELETE FROM client WHERE id={}
    """.format(id)
    commitdb(query)
    return "destroy client successfully", 200


@app.route('/client/<int:id>',methods=['GET'])
def GETIDClient(id):
    query = """
            SELECT name,cpf,phone from client
            where id = {};
    """.format(id)
    cursor = g.conn.execute(query)

    client = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]

    if client:
        return {'client':client}, 200
    return 'error: fail to get',405










#ÁREA DOS MÉTODOS DE ENDEREÇO
@app.route('/address/client/<int:id>',methods=['GET'])
def getAddress(id):
    query = """
    SELECT * FROM address WHERE id_client = {};
    """.format(id)
    cursor = g.conn.execute(query)
    address_dict = [{'locality':row[1],'local':row[2],'discrict':row[3],'cep':row[4],'city':row[5],'state':row[6],'number':row[8]}
                    for row in cursor.fetchall()]
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
        query = """
            INSERT INTO address (locality,local,discrict,number,id_client,cep,city,state)
            VALUES ("{}","{}","{}","{}",{},"{}","{}","{}");
        """.format(locality,local,discrict,number,int(id),cep,city,state)
        commitdb(query)
        return "Saved successfully !", 201
    return "error: fail to update", 405

@app.route('/address/<int:id>',methods=['PUT'])
def putaddress(id):
    if request.get_json:
        address = request.get_json()
        query =  f'UPDATE address SET locality = "{address["locality"]}", local = "{address["local"]}", discrict = "{address["discrict"]}", number = "{address["number"]}",cep = "{address["cep"]}" where id = {id}'
        commitdb(query)
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
        query = f'UPDATE address SET city = "{city}", state = "{state}" WHERE id={id}'
        commitdb(query)
        
        return "Update address successfully !", 200
    return   "error: fail to update", 405

@app.route('/address/<int:id>',methods=['DELETE'])
def DELETEaddress(id):
    query = """
        DELETE FROM address WHERE id={};
    """.format(id)
    commitdb(query)
    return "destroy address successfully", 200

@app.route('/address/<int:id>',methods=['GET'])
def GETidaddress(id):
        query = """
            SELECT * from address
            where id = {};
        """.format(int(id))
        cursor = g.conn.execute(query)

        address = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
        return {'address':address} , 200











#ÁREA DOS MÉTODOS DE PRODUTO
@app.route('/products/store/<int:id>',methods=['GET'])
def getproducts(id):
    query = """
    SELECT * FROM product WHERE id_store = {};
    """.format(id)
    cursor = g.conn.execute(query)
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
        
            query = """
            INSERT INTO product (name,unitary_value,weigth,id_store)
            VALUES ("{}",{},{},{});
            """.format(name,unitary_value,Weigth,int(id))
            commitdb(query)
            return "Saved successfully !", 201
        return "error: fail to post", 405

@app.route('/products/<int:id>',methods=['PUT'])
def putproducts(id):
    if request.get_json:
        product  = request.get_json();

        query = f'UPDATE product SET name = "{product["name"]}", unitary_value = {product["unitary_value"]}, weigth = {product["weigth"]} ;'
        commitdb(query)

        return "Update product successfully !", 200
    return   "error: fail to update", 405

@app.route('/products/<int:id>',methods=['DELETE'])
def DELETEproducts(id):
    query = """
    DELETE FROM product WHERE id={}
    """.format(id)
    commitdb(query)
    return "destroy product successfully", 200     
    

@app.route('/products/<int:id>',methods=['GET'])
def GETidproducts(id):
    query = """
    SELECT * FROM product WHERE id = {};
    """.format(int(id))
    cursor = g.conn.execute(query)
    product = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"products":product}, 200












#AREA DE MÉTODOS DE LOJA

@app.route('/store',methods=['GET'])
def getstore():
    query = """
        SELECT * FROM store;
    """
    cursor = g.conn.execute(query)
    store_dict = [{'cnpj':row[1],'name':row[2],'email':row[3]}
                    for row in cursor.fetchall()]
    return {"store":store_dict}

@app.route('/store',methods=['POST'])
def poststore():
    if request.get_json:
        store = request.get_json()
        name = store["name"]
        cnpj = store["cnpj"]
        email = store["email"]

        query = """
            INSERT INTO store (name,cnpj,email)
            VALUES ("{}","{}","{}");
        """.format(name,cnpj,email)
        commitdb(query)
        return "Saved successfully !", 201
    return {"error: fail to save"}, 405

@app.route('/store/<int:id>',methods=['PUT'])
def putstore(id):
    if request.get_json:
        store = request.get_json()
        query = f'UPDATE store SET name = "{store["name"]}", cnpj = "{store["cnpj"]}", email = "{store["email"]}" where id = {id}'
        commitdb(query)
        return "Update Store successfull", 200
    return   "error: fail to update", 405

@app.route('/store/<int:id>',methods=['DELETE'])
def DELETEstore(id):
    query = """
    DELETE FROM store WHERE id={}
    """.format(int(id))
    commitdb(query)
    return "destroy store successfully", 200

@app.route('/store/<int:id>',methods=['GET'])
def GETidstore(id):
    query = """
            SELECT name,cnpj,email from store
            where id = {};
    """.format(id)
    cursor = g.conn.execute(query)

    store = [dict((cursor.description[i][0], value) \
       for i, value in enumerate(row)) for row in cursor.fetchall()]

    return {'store':store}, 200
    










#ÁREA DOS MÉTODOS DE RASTREIO

@app.route('/tracking/request/<int:id>',methods=['GET'])
def gettracking(id):
    result = search("tracking","id_request",id)
    tracking = [dict((result.description[i][0], value) \
       for i, value in enumerate(row)) for row in result.fetchall()]
    return {"tracking":tracking}

@app.route('/tracking/request/<int:id>',methods=['POST'])
def posttracking(id):
    cod = cod_generator(size,base_cod)
    query = """
        INSERT INTO tracking (cod,id_request)
        VALUES ('{}',{})
    """.format(cod,int(id))

    return "POST tracking"

@app.route('/tracking/<int:id>',methods=['PUT'])
def puttracking(id):
    return "put tracking"

@app.route('/tracking/<int:id>',methods=['DELETE'])
def DELETEtracking(id):
    return "DELETEtracking"

@app.route('/tracking/<int:id>',methods=['GET'])
def GETidtracking(id):
    result = search("tracking","id",id)
    tracking = [dict((result.description[i][0], value) \
       for i, value in enumerate(row)) for row in result.fetchall()]
    return {"tracking":tracking}










#MÉTODOS DE PEDIDO



@app.route("/request/client/<int:id>", methods =["GET"])
def GetRequest(id):
    result = search("request","id_client",id)
    request_client = [dict((result.description[i][0], value) \
       for i, value in enumerate(row)) for row in result.fetchall()]
    return {"request":request_client}, 200


@app.route("/request/client/<int:id>", methods=["POST"])
def PostRequest(id):
    client = search("client","id",int(id))
    request_client = [dict((client.description[i][0], value) \
       for i, value in enumerate(row)) for row in client.fetchall()]
    client = request_client[0]
    id_store = client["id_store"]
    query = """
        INSERT INTO request (id_client,id_store)
        VALUES ({},{});
    """.format(int(id),int(id_store))
    commitdb(query)
    return "Salve ok!", 200
    
    
    
@app.route("/request/<int:id>", methods=["GET"])
def  GetResquetID(id):
        search_request = search("request","id",id)
        search = [{'id':row[0],'cod':row[1],'id_client':row[2],'id_delivery':row[3],'id_store':row[4]}
                    for row in search_request.fetchall()]
        return {"request":search}, 200


#MÉTODO PARA PARA A TABELA request_products

@app.route("/request/products/<int:id_request>/<int:id_product>", methods=["POST"])
def request_product(id_request, id_product):
    if request.get_json:
        quantity = request.get_json()

        query = """
        INSERT INTO request_product (id_request,id_procduct,quantity)
        VALUES ({},{},{});
        """.format(id_request,id_product,quantity["quantity"])
        commitdb(query)
        return "Salve ok!", 200
    return "fail!",405

if __name__ =='__main__':
    app.run(debug=True, host="0.0.0.0",port=8090)





