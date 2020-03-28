"""
Registration of a user - 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on database for 1 token
"""



from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017') #default mongo port
db = client.aNewDB
UserNum = db["UserNum"]
UserNum.insert({
    "num of users": 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num of users']
        new_num = prev_num + 1
        UserNum.update({}, {'$set': {'num of users':new_num}})
        return str('hello user') + " " + str(new_num)

def checkPostedData(postedData, functionName):
    if functionName in ['add','sub','div','mul']:
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData['y']) == 0:
            return 302
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
    def post(self):
        #if I'm here, then the resource Add was requested using the method POST
        
        #get posted data
        postedData = request.get_json()
        
        #verify validity of data
        status_code = checkPostedData(postedData,'sub')
        
        if status_code!=200:
            retJson = {"Message": "input error",
                    "Status Code": status_code}
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]       
        x = int(x)
        y = int(y)
        
        #add posted data
        ret = x-y  
        
        #return
        retMap = {"Message":ret, 
                  "Status Code": 200}
        
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        #if I'm here, then the resource Add was requested using the method POST
        
        #get posted data
        postedData = request.get_json()
        
        #verify validity of data
        status_code = checkPostedData(postedData,'mul')
        
        if status_code!=200:
            retJson = {"Message": "input error",
                    "Status Code": status_code}
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]       
        x = int(x)
        y = int(y)
        
        #add posted data
        ret = x*y  
        
        #return
        retMap = {"Message":ret, 
                  "Status Code": 200}
        
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #if I'm here, then the resource Add was requested using the method POST
        
        #get posted data
        postedData = request.get_json()
        
        #verify validity of data
        status_code = checkPostedData(postedData,'mul')
        
        if status_code!=200:
            retJson = {"Message": "input error",
                    "Status Code": status_code}
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]       
        x = int(x)
        y = int(y)
        
        #add posted data
        ret = x/y  
        
        #return
        retMap = {"Message":ret, 
                  "Status Code": 200}
        
        return jsonify(retMap)

api.add_resource(Add, "/add")
api.add_resource(Substract, "/sub")
api.add_resource(Multiply, "/mul")
api.add_resource(Divide, "/div")
api.add_resource(Visit, "/")

@app.route('/')
def hello_world():
    return "Hello restful"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000,debug = True)
    