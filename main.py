import json
from flask import Flask, jsonify, request
import requests
import pymongo
from bson import json_util, ObjectId
from bid import Bid, create_bid
from project import Project, add_project
from profile import Profile, create_profile

my_client = pymongo.MongoClient("mongodb://localhost:27017/")

my_db = my_client['webiste']

users = my_db['user_data']
projects = my_db['project_info']
bids = my_db['bids']

# my_db.bids.drop()

users.create_index("user_id", unique=True)
users.create_index("username", unique=True)
users.create_index("email", unique=True)
projects.create_index("project_id", unique=True)
bids.create_index("bid_id", unique=True)


app = Flask(__name__)


@ app.route('/api/create_profile', methods=['POST'])
def new_profile():
    json_request = request.get_json()
    new_profile = create_profile(json_request['profile'])
    response = str(users.insert_one(new_profile.__dict__))
    return jsonify(response), 201


@ app.route('/api/post_project', methods=['POST'])
def post_project():
    json = request.get_json()
    new_project = add_project(json['project'])
    user = users.find_one({"user_id": new_project.user_id})
    project_array = user["projects"]
    project_array.append(new_project.project_id)
    newvalues = {"$set": {"projects": project_array}}
    users.update_one({"user_id": new_project.user_id}, newvalues)
    response = str(projects.insert_one(new_project.__dict__))
    return jsonify(response), 201


@ app.route('/api/place_bid', methods=['POST'])
def create_new_bid():
    json = request.get_json()
    new_bid = create_bid(json['bid'])
    myquery = {"project_id": new_bid.project_id}
    mydoc = projects.find_one(myquery)
    new_bids = mydoc["bids"]
    new_bids.append(new_bid.bid_id)
    newvalues = {"$set": {"bids": new_bids}}
    projects.update_one(myquery, newvalues)
    response = "success"
    return jsonify(response), 201

@ app.route('/api/search_project/<int:id>',methods=['GET'])
def search_project(id):
    myquery= {"project_id": id}
    mydoc=projects.find_one(myquery)
    return jsonify(str(mydoc)),201

@ app.route('/api/close_project/<int:id>',methods=['PUT'])
def close_Project(id):
    myquery= {"project_id": id}
    # mydoc=mycol2.find_one(myquery)
    newvalues={"$set":{"status":0}}
    projects.update_one(myquery, newvalues)
    response ="success"
    return jsonify(response),201

@ app.route('/api/get_bids/<int:id>',methods=['PUT'])
def show_bids(id):
    myquery={"project_id":id}
    temp=projects.find_one(myquery)
    return jsonify(temp["bids"]),temp


@ app.route('/api/view_profile/<int:id>',methods=['GET'])
def show_profile(id):
    myquery= {"user_id": id}
    temp=users.find_one(myquery)
    return json_util.dumps(temp),201

@ app.route('/api/get_my_projects/<int:id>',methods=['PUT'])
def get_my_projects(id):
    myquery= {"user_id":id}
    temp= users.find_one(myquery)
    project_arr=temp["projects"]
    list1=[]
    for i in project_arr:
        new_proj=projects.find_one({"project_id":i})
        list1.append(json_util.dumps(new_proj))
    return jsonify(list1)

@ app.route('/api/get_projects',methods=['GET'])
def get_projects():
    temp=projects.find()
    temp=list(temp)
    temp=json_util.dumps(temp)
    return temp,201


app.run(host='0.0.0.0', port=5000)
