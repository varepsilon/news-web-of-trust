from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_cors import CORS
import traceback
import json

import docs

app = Flask(__name__)
CORS(app)
api = Api(app)
IDS_TO_USERS = {}
TRUST_GRAPH = {}
TRUST_THRESHOLD = 2

class StorageAccessor(Resource):
    def put(self):
        return docs.get_similar_docs(request.form['url'], 10)


class Voter(Resource):
    def put(self):
        try:
            docs.add_new_doc(request.form['url'], request.form['user'], request.form['ranking'])
            return 'Success!'
        except:
            return 'Failed!\n{}'.format(traceback.format_exc())

def format_result(result):
    chain, doc, ranking = result
    return {
            'url': doc['url'],
            'content': doc['content'],
            'status': 'fake' if ranking == 1 else 'real',
            'friends': [IDS_TO_USERS[id_] for id_ in chain]
    }


class SimilarDocsAccessor(Resource):
    def put(self):
        doc = docs.WebDocument(request.form['url'])
        similar = docs.get_similar_docs(doc, 1000)
        root_user = request.form['user']
        trusted_1 = docs.get_most_trusted_from_similar(similar, TRUST_GRAPH, root_user, TRUST_THRESHOLD)
        trusted_2 = docs.get_most_similar_from_trusted(similar, TRUST_GRAPH, root_user, TRUST_THRESHOLD)
        doc_result_1 = format_result(trusted_1)
        doc_result_2 = format_result(trusted_2)
        outcome = 'Your friends are not sure :('
        if trusted_1[2] == 1 and trusted_2[2] == 1:
            outcome = 'Your friends believe this is truth'
        else:
            outcome = 'Your friends believe this is fake'
        return {
                'result': outcome,
                'doc': [doc_result_1, doc_result_2]
        }

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
# curl http://localhost:8000/ranked -d "url=https://www.bbc.com/news/world-us-canada-45517260" -d  "user=2" -X PUT
api.add_resource(SimilarDocsAccessor, '/ranked')
# Example:
# curl http://localhost:8000/vote -d "url=https://www.bbc.com/news/world-us-canada-45517260" -d "user=u2" -d "ranking=2.0" -X PUT
api.add_resource(Voter, '/vote')
api.add_resource(Dummy, '/test')

if __name__ == '__main__':
    with open('users_json') as user_file:
        user_json = json.load(user_file)
        users = user_json.values()
        for user in users:
            IDS_TO_USERS[user['id']] = "{user['name']} {user['secondName']}"
            TRUST_GRAPH[user['id']] = user['friendsIdList']
    app.run(port='8000')
