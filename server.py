from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from docs import add_new_doc

app = Flask(__name__)
api = Api(app)

#class StorageGetter(Resource):
#    def get(self):
#        doc_to_votes = storage.get()
#        return jsonify({doc.getHTML(): [vote.get() for vote in doc_to_votes[doc]] for doc in doc_to_votes})


class Voter(Resource):
    def put(self):
        add_new_doc(request.form['url'], request.form['user'], request.form['ranking'])

#api.add_resource(StorageGetter, '/storage')
# Example:
# "curl http://localhost:8000/vote -d "url=https://www.bbc.com/news/world-us-canada-45517260" -d "user=u2" -d "ranking=2.0" -X PUT
api.add_resource(Voter, '/vote')

if __name__ == '__main__':
     app.run(port='8000')
