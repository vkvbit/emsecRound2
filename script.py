from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb+srv://vaibhav:vaibpasswd@cluster0.vgsxvy5.mongodb.net/EMSEC'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

@app.route('/', methods = ['GET'])
def retrieveAll():
    holder = list()
    currentCollection = mongo.db.user
    for i in currentCollection.find():
        holder.append({'name':i['name'], 'password' : i['password'], 'role' : i['role']})
    return jsonify(holder)

@app.route('/<name>', methods = ['GET'])
@cross_origin()
def retrieveFromName(name):
    currentCollection = mongo.db.user
    data = currentCollection.find_one({"name" : name})
    return jsonify({'name' : data['name'], 'password' : data['password'], 'role' : data['role']})

@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = mongo.db.user
    name = request.json['name']
    password = request.json['password']
    role = request.json['role']
    currentCollection.insert({'name' : name, 'password' : password, 'role' : role})
    return jsonify({'name' : name, 'password' : password, 'role' : role})

@app.route('/deleteData/<name>', methods = ['DELETE'])
def deleteData(name):
    currentCollection = mongo.db.user
    currentCollection.delete_one({'name' : name})
    return redirect(url_for('retrieveAll'))

@app.route('/update/<name>', methods = ['PUT'])
def updateData(name):
    currentCollection = mongo.db.user
    updatedName = request.json['name']
    currentCollection.update_one({'name':name}, {"$set" : {'name' : updatedName}})
    return redirect(url_for('retrieveAll'))

if __name__ == '__main__':
    app.run(debug = True)
