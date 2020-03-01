from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from nocache import nocache

app = Flask(__name__)
api = Api(app)

def checkPostedData(postedData, functionName):
    if functionName == 'add':
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
        
class Add(Resource):
    def post(self):
        #if I'm here, then the resource Add was requested using the method POST
        
        #get posted data
        postedData = request.get_json()
        
        #verify validity of data
        status_code = checkPostedData(postedData,'add')
        
        if status_code!=200:
            retJson = {"Message": "input error",
                    "Status Code": status_code}
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]       
        x = int(x)
        y = int(y)
        
        #add posted data
        ret = x+y  
        
        #return
        retMap = {"Message":ret, 
                  "Status Code": 200}
        
        return jsonify(retMap)
    def get(self):
        return "Hi"
        

class Substract(Resource):
    pass

class Multiply(Resource):
    pass

class divide(Resource):
    pass

api.add_resource(Add, "/add")

@app.route('/')
@nocache
def hello_world():
    return "Hello restful"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port = 80,debug = True)
    