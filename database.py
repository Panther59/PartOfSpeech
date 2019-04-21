from pymongo import MongoClient
from feeds import News
from dateutil import parser
from jsonconverter import jsonconverter
from textparser import textparser
import json
import glob
import errno


class database(object):

    mongodbURL = "mongodb://localhost:27017"

    def getknownorgs(self):
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["Organizations"]

        cursor = collection.find({})
        return [d for d in cursor]

    def getfeedsource(self):
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["FeedSources"]

        cursor = collection.find({})
        return [d for d in cursor]

    def load(self):
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["News"]

        cursor = collection.find()
        try:
            for doc in cursor:
                conv = jsonconverter()
                out = self.map(doc)
                s = conv.serialise(out)
                print(s)
                self.addnews(out)
        finally:
            cursor.close()

    def map(self, input):
        knownOrgs = self.getknownorgs()
        tparser = textparser()
        orgs = tparser.findorgs(input["text"])
        myorgs = self.getRelaventOrgs(knownOrgs, orgs)
        output = News(input["uuid"], input["title"], input["text"],
                      parser.parse(input["published"], myorgs))
        return output

    def getRelaventOrgs(self, knownOrgs, orgs):
        myorgs = [x["key"] for x in list(
            filter(lambda x: self.hasOrgs(x["values"], orgs), knownOrgs))]
        return myorgs

    def hasOrgs(self, knownOrgs, currentOrgs):
        for o in knownOrgs:
            if any(x.upper() == o.upper() for x in currentOrgs):
                return True
        return False

    def findbykey(self, key):
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["News"]

        return collection.find_one({"key": key})

    def addOrgs(self, org):
        name = org["key"]
        alias = org["values"]
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["Organizations"]

        colcount = collection.find({"key": name}).count()
        if (colcount == 0):
            s = json.dumps(org)
            collection.insert_one(org)
        else:
            for v in alias:
                collection.update(
                    {'key': name}, {'$addToSet': {'values': v}}, upsert=True)

    def addFeedSource(self, source):
        name = source["name"]
        url = source["url"]
        weight = source.get("weight", None)
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["FeedSources"]

        colcount = collection.find({"name": name}).count()
        if (colcount == 0):
            collection.insert_one(source)
        else:
            collection.update_one(
                {'name': name}, {'$set': {'url': url}})

            if(weight != None):
                collection.update_one(
                    {'name': name}, {'$set': {'weight': weight}})

    def update_orgs(self, key, orgs):
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["News"]

        for org in orgs:
            collection.update(
                {'key': key}, {'$push': {'organizations': org}}, upsert=True)

    def addnews(self, news):
        client = MongoClient(self.mongodbURL)
        database = client["Feeds"]
        collection = database["News"]

        colcount = collection.find({"key": news.key}).count()
        if (colcount == 0):
            conv = jsonconverter()
            s = conv.serialise(news)
            collection.insert_one(s)

    def loadFiles(self):
        path = r'E:\Personal\Utkarsh\Projects\CS\Hackathon2019\us-financial-news-articles\New_folder\*.json'
        files = glob.glob(path)
        for name in files:
            with open(name, encoding="utf8") as json_file:
                doc = json.load(json_file)
                out = self.map(doc)
                self.addnews(out)
                print("File imported '{}".format(name))


# database = database()
# o = database.loadFiles()
