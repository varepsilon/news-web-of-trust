from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_cors import CORS
import docs

app = Flask(__name__)
CORS(app)
api = Api(app)

class StorageAccessor(Resource):
    def put(self):
        return docs.get_similar_docs(request.form['url'], 10)


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

class Dummy(Resource):
    def put(self):
        return {
                'result': 'fake',
                'doc': [
                    {
                        'url': 'http://foo',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                        'status': 'fake',
                        'friend': 'Boo, a friend of Baa'
                    }, {
                        'url': 'http://bar',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                        'status': 'real',
                        'friend': 'Maa'
                    }]
        }

# Example:
# curl http://localhost:8000/storage -d "url=https://www.bbc.com/news/world-us-canada-45517260" -X PUT
api.add_resource(StorageAccessor, '/storage')
# Example:
# curl http://localhost:8000/vote -d "url=https://www.bbc.com/news/world-us-canada-45517260" -d "user=u2" -d "ranking=2.0" -X PUT
api.add_resource(Voter, '/vote')
api.add_resource(Dummy, '/test')

if __name__ == '__main__':
     app.run(port='8000')
