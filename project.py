import json
from flask import Flask, jsonify, request
import requests
import pymongo
import shutil
import hashlib
import enum
import random
from bid import Bid, create_bid

count = 0


class Project:
    def __init__(self, project):
        self.name = project['name']
        self.project_id = None
        self.description = project['description']
        self.skills = project['skills']
        self.status = 1
        self.bids = []
        self.user_id = project['user_id']
        # add timestamp, file upload

    

    def reopen_project(self):
        self.status = 1

    def add_bid(self, bid):
        new_bid = create_bid(bid)
        self.bids.append(new_bid)
        return 'success1'

def close_project(project):
        project["status"] = 0

def get_status(project):
        return project["status"]

def add_project(project):
    global count
    count += 1
    new_project = Project(project)
    new_project.project_id = count
    return new_project
