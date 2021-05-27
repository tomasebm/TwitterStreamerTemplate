# -*- coding: utf-8 -*-

import datetime

currentDT = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

CONNECTION_STRING = "sqlite:////home/ubuntu/TwitterStreamerTemplate/data/tweets.db"
TABLE_NAME = "streamer"

CSV_NAME = currentDT + '_' + TABLE_NAME + '.csv'
EXPORT_LOC = '../data/' + CSV_NAME
 
