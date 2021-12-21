from flask import Flask, request, redirect, jsonify
from flask.wrappers import Response
from flask_pymongo import PyMongo
from pymongo import message
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.wrappers import response


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def create_user():
    #reciving data
    content = request.get_json(force=True)
    username = content["username"]
    print(username)
    password = content["password"]
    print(password)
    email = content["email"]
    print(email)
    if username and password and email:
        hashed_password = generate_password_hash(password)
        
        id = mongo.db.users.insert_one(
            {"username":username, "email":email, "password":hashed_password}
        )
        response = {
            "id":str(id),
            "username":username,
            "password":hashed_password,
            "email":email
        }

        return jsonify(response)
    
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    user_data = mongo.db.users.find()
    response = json_util.dumps(user_data)
    return Response(response, mimetype='application/json')


@app.route('/users/<id>', methods=['GET'])
def get_filter_user(id):
    user_data = mongo.db.users.find_one_or_404({"_id":ObjectId(id)})
    response = json_util.dumps(user_data)
    return Response(response, mimetype='application/json' )


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({"_id":ObjectId(id)})
    return jsonify({'message':'User Was deleted'})




@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    
    content = request.get_json(force=True)
    username = content["username"] 
    password = content["password"]
    email = content["email"]
    
    if username and password and email:
        hashed_password = generate_password_hash(password)
    
        mongo.db.users.update_one({"_id":ObjectId(id)}, {'$set': {
            'username':username,
            'password':hashed_password,
            'email':email
        }})
        response = jsonify({'message':'user was updated'})

        return response



@app.errorhandler(404)
def not_found(error=None):
    message =jsonify({
        'message':'Resosurce Not Found:' + request.url,
        'status':404
    })
    message.status_code = 404
    return message







if __name__=='__main__':
    app.run(debug=True)