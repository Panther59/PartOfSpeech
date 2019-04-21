from flask import Flask, request, Response
from flask_jsonpify import jsonify
from feeds import FeedHelper
from datetime import datetime
import json
from database import database
from textparser import textparser

app = Flask(__name__)

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': str(error)}), 500

@app.route("/", methods=["GET"])
def test():
    return jsonify({'text': 'test'})

@app.route("/feeds", methods=["POST"])
def feeds():
    data = str(request.data.decode('utf-8'))
    helper = FeedHelper()
    response = helper.get_news(data)
    return Response(json.dumps(serialise(response), indent=4, default=myconverter),  mimetype='application/json')


@app.route("/news/organizations", methods=["POST"])
def newsOrgs():
    data = str(request.data.decode('utf-8'))
    tp = textparser()
    orgs = tp.findorgs(data)
    db = database()
    knownOrgs = db.getknownorgs()
    response = db.getRelaventOrgs(knownOrgs, orgs)
    return Response(json.dumps(response, indent=4, default=myconverter),  mimetype='application/json')


@app.route("/organizations", methods=["GET"])
def getOrgs():
    db = database()
    knownOrgs = db.getknownorgs()
    return Response(json.dumps(knownOrgs, indent=4, default=myconverter),  mimetype='application/json')


@app.route("/organizations", methods=["PUT"])
def saveOrgs():
    content = request.get_json(silent=True)
    db = database()
    for org in content:
        db.addOrgs(org)
    return Response()


@app.route("/feeds/sources", methods=["GET"])
def getfeedsource():
    db = database()
    knownOrgs = db.getfeedsource()
    return Response(json.dumps(knownOrgs, indent=4, default=myconverter),  mimetype='application/json')


@app.route("/feeds/sources", methods=["PUT"])
def savefeedsource():
    sources = request.get_json(silent=True)
    db = database()
    for source in sources:
        db.addFeedSource(source)
    return Response()

def serialise(obj):
    if isinstance(obj, list):
        return [serialise(o) for o in obj]
    else:
        return {snake_to_camel(k): v for k, v in obj.__dict__.items()}


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def snake_to_camel(s):
    a = s.split('_')
    a[0] = a[0].lower()
    if len(a) > 1:
        a[1:] = [u.title() for u in a[1:]]
    return ''.join(a)


if __name__ == '__main__':
    app.run(port=5002)
