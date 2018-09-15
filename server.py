from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify

import docs

app = Flask(__name__)
api = Api(app)

class StorageAccessor(Resource):
    def put(self):
        doc = docs.WebDocument(request.form['url'])
        return docs.get_similar_docs(doc, 10)
        # return jsonify(get_storage()


class Voter(Resource):
    def put(self):
        try:
            docs.add_new_doc(request.form['url'], request.form['user'], request.form['ranking'])
            return 'Success!'
        except:
            return 'Failed!'

class SimilarDocsAccessor(Resource):
    def put(self):
        return docs.get_similar_docs

# Example:
# curl http://localhost:8000/storage -X GET
# curl http://localhost:8000/storage -d "url=https://www.bbc.com/news/world-us-canada-45517260" -X PUT
api.add_resource(StorageAccessor, '/storage')
# Example:
# curl http://localhost:8000/vote -d "url=https://www.bbc.com/news/world-us-canada-45517260" -d "user=u2" -d "ranking=2.0" -X PUT
api.add_resource(Voter, '/vote')

if __name__ == '__main__':
     app.run(port='8000')
