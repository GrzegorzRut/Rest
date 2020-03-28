"""
Registration of a user - 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on database for 1 token
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import bcrypt
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017') #default mongo port
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):        
        # step 1 get posted data by user
        postedData = request.get_json()
        
        # get the data
        username = postedData["username"]
        password = postedData["password"]
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        
        # store username and pw into database
        users.insert({
        "Username": username,
        "Password": hashed_pw,
        "Sentence":"",
        "Tokens":6
        })
        retJson = {"status":200,
                   "msg":"You successfully signed up for the API"}
        return retJson
    
def verifyPw(username, password):
    hashed_pw = users.find({
        "Username":username})[0]["Password"]
    if bcrypt.hashpw(password.encode('utf8'), 
                                     hashed_pw) == hashed_pw:
        return True
    else:
        return False
    
def countTokens(username):
    tokens = users.find({
        "Username":username})[0]["Tokens"]
    return tokens

class Store(Resource):
    def post(self):
        # get the posted data
        postedData = request.get_json()
        
        #read data
        username = postedData['username']
        password = postedData['password']
        sentence = postedData['sentence']
        
        # verify username, password
        correct_pw = verifyPw(username, password)
        
        if not correct_pw:
            retJson = {
                'status':302
            }
            return jsonify(retJson)
        
        # verify token availability
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                'status':301
            }
            return jsonify(retJson)
        
        # store sentence
        users.update({
            "Username": username}, {"$set": {
                                            "Sentence": sentence,
                                            "Tokens": num_tokens-1
                                            }
                                   })
        retJson = {
                    "status": 200,
                    "sentence": users\
                    .find({"Username":username})[0]["Sentence"]
                    }
        return jsonify(retJson)

class Get(Resource):
    def post(self):
        # get the posted data
        postedData = request.get_json()
        
        #read data
        username = postedData['username']
        password = postedData['password']

        # verify username, password
        correct_pw = verifyPw(username, password)
        
        if not correct_pw:
            retJson = {
                'status':302
            }
            return jsonify(retJson)
        else:
            sen =  users.find({
            "Username":username})[0]["Sentence"]

            retJson = {"sentence": sen,
                    "status": 200,
                    }
        return jsonify(retJson)


        
        
api.add_resource(Register,"/register")
api.add_resource(Store,"/store")
api.add_resource(Get,"/get")
        
if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000,debug = True)