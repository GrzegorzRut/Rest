from flask import Flask,jsonify,request
import numpy as np
app = Flask(__name__)

@app.route('/',methods = ["GET"]) # once server is running, application's waiting for '/', then makes #the function and sends response
def hello_world():
    return "Hello world"


@app.route('/calculate_stuff',methods = ["POST","GET"])
def calculate_stuff():
    
    #Get x, y from posted data
    dataDict = request.get_json()
    if "x" not in dataDict:
        return "Error", 305
    x= dataDict['x']
    y= dataDict['y']
    #calculate z = (x+y)**0.5
    retJSON = {"z": np.sqrt(x +y)}
    return jsonify(retJSON), 200

@app.route('/hithere',methods = ["GET"]) 
def hi_there_everyine():
    c= {'a':1,'b':2}
    d = {
    'field1':[1,2,3],
    'field2':'def',
    'field3': True,
    'field4': None,
    'field5': [0,123,c]
     
    }
    return d

if __name__=="__main__":
    app.run(host='127.0.0.1',port=80,debug = True)
    
   
