"""
Utility script to get the progress of a session. Pass the name and tasks per stage

progress.py rp.session.two.00000.0000 65
"""
import os

import click

from pymongo import MongoClient


@click.command()
@click.option('--db-url', default=os.environ['RADICAL_PILOT_DBURL'], help="MongoDB url used to run this script")
@click.option('--session', type=str, help="Radical pilot session name")
@click.option('--tasks-per-stage', default=-1, help="Number of tasks per stage. Used to show progress per stage")
def progress(db_url, session, tasks_per_stage):

    db = db_url.split('/')[-1]

    collection = MongoClient(db_url)[db][session]

    cursor = collection.find()
    count = [(unit['state'] == 'DONE') for unit in cursor if unit['type'] == 'unit']

    if tasks_per_stage == -1:
        tasks_per_stage = sum(count)

    stage, completed = divmod(sum(count), tasks_per_stage)
    percentage = round(completed/tasks_per_stage * 100, 2)

    if sum(count) == len(count):
        # If all the tasks finished then the above gives incorrect result.
        stage -= 1
        completed = tasks_per_stage
        percentage = 100

    click.echo("Stage {} progress: {}/{} ({}%)".format(stage, completed, tasks_per_stage, percentage))
