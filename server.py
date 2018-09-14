from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
import urllib

app = Flask(__name__)
api = Api(app)

class Vote():
    def __init__(self, user_id, ranking):
        self.user = user_id
        self.ranking = ranking

    def __str__(self):
        return '(%s, %f)' % (self.user, self.ranking)

    def get(self):
        return (self.user, self.ranking)


class Document():
    def __init__(self, url):
        resp = urllib.request.urlopen(url)
        self.html = resp.read()

    def hash(self):
        return hash(self.html)

    def getHTML(self):
        return self.html


class DocumentStorage():
    def __init__(self):
        self.doc_to_votes = {}

    def add(self, doc, vote):
        if doc not in self.doc_to_votes:
            self.doc_to_votes[doc] = []
        self.doc_to_votes[doc].append(vote)

    def get(self):
        return self.doc_to_votes
 
storage = DocumentStorage()

class StorageGetter(Resource):
    def get(self):
        doc_to_votes = storage.get()
        return jsonify({doc.hash(): [vote.get() for vote in doc_to_votes[doc]] for doc in doc_to_votes})


class NewsPutter(Resource):
    def put(self):
        doc = Document(request.form['url'])
        vote = Vote(request.form['user'], request.form['ranking'])
        storage.add(doc, vote)

api.add_resource(StorageGetter, '/storage')
api.add_resource(NewsPutter, '/vote')

if __name__ == '__main__':
     app.run(port='8000')
