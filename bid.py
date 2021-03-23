import json
from flask import Flask, jsonify, request
import requests
import pymongo

count = -1


class Bid:
    def __init__(self, bid):
        self.bid_id = None
        self.hourly_rate = bid['hourly_rate']
        self.weekly_limit = bid['weekly_limit']
        self.proposal = bid['proposal']
        self.project_id = bid['project_id']
        self.bidder_id = bid['bidder_id']
    # def __repr__(self):
    #     return str(self.hourly_rate) + " " +str(self.weekly_limit)


def create_bid(bid):
    global count
    count += 1
    new_bid = Bid(bid)
    new_bid.bid_id = count
    return new_bid
