import json
from flask import Flask, jsonify, request
import requests
import pymongo
import shutil
from bid import Bid
from project import Project,add_project

count=-1

class Profile:
    def __init__(self,info):
        self.name=info['name']
        self.username=info['username']
        self.email=info['email']
        self.user_id=None
        self.projects=[]
        # self.about=info['about']
        # self.nationality=info['nationality']
        # self.activity_status=info['activity_status']
        # self.experience=info['experience']
        # self.education=info['education']
        # self.publications=info['publications']
        # self.reviews=info['reviews']
        # self.amount_earned=info['amount_earned']
        # self.rating=info['rating']
        # self.jobs_completed=info['jobs_completed']
        # self.skills=info['skills']
        # self.balance=info['balance']
        # self.recommendations=info['recommendations']
    def post_project(self,project):
            new_project=add_project(project)
            self.projects.append(new_project)

    def place_bid(self,project,bid):
            project.add_bid(bid)


def create_profile(profile):
    global count
    new_profile=Profile(profile)
    count=count+1
    new_profile.user_id = count
    return new_profile