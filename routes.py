from ast import Return
from http import client
from requests import Response
from config import create_app
from flask_cors import CORS
from Controllers import addressController,clientController,deliveryController,shippingController,storeController,request_prodcutController,requestController,productController,trackingController

app = create_app()
cors = CORS(app)
#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #method Home
@app.route('/')
def index():
    return "<h1>Start Home</h1>"

#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #method delevery

@app.route("/delivery/request/<int:id_request>",methods=["GET"])
def get_delivery(id_request):
    return deliveryController.index(id_request)


@app.route("/delivery/request/<int:id_request>/<int:id_address>",methods=["POST"])
def post_delivery(id_request,id_address):
    return deliveryController.store(id_request,id_address)


@app.route("/delivery/<int:id_delivery>/<int:id_address>",methods=["PUT"])
def put_delivery(id_delivery,id_address):
  return deliveryController.update(id_delivery,id_address)


@app.route("/delivery/<int:id_delivery>",methods=["DELETE"])
def delete_delivery(id_delivery):
  return deliveryController.delete(id_delivery)



@app.route("/delivery/store/<int:id_delivery>",methods=["GET"])
def get_iddelivery(id_delivery):
  return deliveryController.show(id_delivery)




#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods client

@app.route("/client/store/<int:id_store>",methods=["GET"])
def get_client(id_store):
    return clientController.index(id_store)
    

@app.route("/client/store/<int:id_store>",methods=["POST"])
def post_client(id_store):
    return clientController.store(id_store)
 

@app.route("/client/<int:id_client>",methods=["PUT"])
def put_client(id_client):
    return clientController.update(id_client)


@app.route("/client/<int:id_client>",methods=["DELETE"])
def delete_client(id_client):
    return clientController.delete(id_client)


@app.route("/client/<int:id_client>",methods=["GET"])
def get_idclient(id_client):
    return clientController.show(id_client)


#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods address

@app.route("/address/client/<int:id_client>",methods=["GET"])
def get_address(id_client):
    return addressController.index(id_client)

@app.route("/address/client/<int:id_client>",methods=["POST"])
def post_address(id_client):
    return addressController.store(id_client)

@app.route("/address/<int:id_address>",methods=["PUT"])
def put_address(id_address):
    return addressController.update(id_address)

@app.route("/address/<int:id_address>",methods=["DELETE"])
def delete_address(id_address):
    return addressController.delete(id_address)

@app.route("/address/<int:id_address>",methods=["GET"])
def get_idaddress(id_address):
    return addressController.show(id_address)


#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods products

@app.route("/product/store/<int:id_store>",methods=["GET"])
def get_product(id_store):
    return productController.index(id_store)


@app.route("/product/store/<int:id_store>",methods=["POST"])
def post_product(id_store):
    return productController.store(id_store)
    
 

@app.route("/product/<int:id_product>",methods=["PUT"])
def put_product(id_product):
    return productController.update(id_product)


@app.route("/product/<int:id_product>",methods=["DELETE"])
def delete_product(id_product):
    return productController.delete(id_product)


@app.route("/product/<int:id_product>",methods=["GET"])
def get_idproduct(id_product):
    return productController.show(id_product)

#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods store

@app.route("/store",methods=["GET"])
def get_store():
    return storeController.index()

@app.route("/store",methods=["POST"])
def post_store():
    return  storeController.store()

@app.route("/store/<int:id_store>",methods=["PUT"])
def put_store(id_store):
    return  storeController.update(id_store)
    

@app.route("/store/<int:id_store>",methods=["DELETE"])
def delete_store(id_store):
    return storeController.delete(id_store)


@app.route("/store/<int:id_store>",methods=["GET"])
def get_idstore(id_store):
   return storeController.show(id_store)


#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods tracking

@app.route("/tracking/request/<int:id_request>",methods=["GET"])
def get_tracking(id_request):
    return ":)"

@app.route("/tracking/request/<int:id_request>",methods=["POST"])
def post_tracking(id_request):
    return trackingController.store(id_request)
 

@app.route("/tracking/<int:id_tracking>",methods=["PUT"])
def put_tracking(id_tracking):
    return trackingController.update(id_tracking)


@app.route("/tracking/<int:id_tracking>",methods=["DELETE"])
def delete_tracking(id_tracking):
    return "tracking get_tracking"

@app.route("/tracking/<int:id_tracking>",methods=["GET"])
def get_idtracking(id_tracking):
    return trackingController.show(id_tracking)



#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods request

@app.route("/request/client/<int:id_client>",methods=["GET"])
def get_request(id_client):
    return requestController.index(id_client)

@app.route("/request/client/<int:id_client>",methods=["POST"])
def post_request(id_client):
    return requestController.store(id_client)
  

@app.route("/request/<int:id_request>",methods=["PUT"])
def put_request(id_request):
    return requestController.update(id_request)


@app.route("/request/<int:id_request>",methods=["DELETE"])
def delete_request(id_request):
    return requestController.delete(id_request)
  

@app.route("/request/<int:id_request>",methods=["GET"])
def get_idrequest(id_request):
    return requestController.show(id_request)



#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods request_product

@app.route("/request/product/<int:id_request>/<int:id_product>",methods=["POST"])
def post_request_products(id_request,id_product):
    return request_prodcutController.store(id_request,id_product)


#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #methods shipping

@app.route("/calculate_shipping", methods = ["POST"])
def shipping():
    return shippingController.calculate()


#------------------------------------------

#------------------------------------------

#------------------------------------------

#------------------------------------------
            #Setup


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=8090)