"""
Utility script to get the progress of a session. Pass the name and tasks per stage

progress.py rp.session.two.00000.0000 65
"""
import os
import sys

from pymongo import MongoClient

db = os.environ['RADICAL_PILOT_DBURL'].split('/')[-1]
session = sys.argv[1]
tasks_per_stage = int(sys.argv[2])

collection = MongoClient(os.environ['RADICAL_PILOT_DBURL'])[db][session]

cursor = collection.find()
count = [(unit['state'] == 'DONE') for unit in cursor if unit['type'] == 'unit']

stage, completed = divmod(sum(count), tasks_per_stage)

percentage = round(completed/tasks_per_stage * 100, 2)

print("Stage {} progress: {}/{} ({}%)".format(stage, completed, tasks_per_stage, percentage))
