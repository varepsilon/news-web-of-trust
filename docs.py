import heapq
import re
import requests
import json

from lib import Doc2Vec

doc_to_vec = Doc2Vec('./model/GoogleNews-vectors-negative300-SLIM.bin')

document_storage = {}


class WebDocument:
    def __init__(self, url, content=None, vector=None):
        if content is None:
            content = _html_to_text(url)
        if vector is None:
            vector = doc_to_vec.get_vector(content)
        self.url = url
        self.content = content
        self.vector = vector

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        content_truncated = self.content[:300]
        if len(content_truncated) < len(self.content):
            content_truncated = content_truncated[:-3] + '...'
        return json.dumps({'url': self.url, 'content': content_truncated})


def _html_to_text(path):
    url = "http://fuckyeahmarkdown.com/go/"
    # construct query
    params = {
            "u": path, # url encoded URI to parse
            "read": 1, # whether to run Readability or not, 0 turns off
            "md": 1, # whether to run Markdownify or not, 0 turns off
            "output": "json", # type of text to return: json, url (encoded), or markdown
    }
    response = requests.get(url, params=params, timeout=2)
    words = []
    for word in response.text.split(' '):
        if re.fullmatch('[a-zA-Z_]+', word):
            words.append(word.lower())
    return ' '.join(words)

def add_new_doc(url, user, ranking):
    doc = WebDocument(url)
    document_storage.setdefault(url, {'doc': doc, 'ranking': {}})
    document_storage[url]['ranking'][user] = ranking

def get_storage():
    return document_storage

def get_similar_docs(this_doc, top_n):
    h = []
    v1 = this_doc.vector
    for stored in document_storage.values():
        that_doc = stored['doc']
        v2 = that_doc.vector
        sim = doc_to_vec.sim(v1, v2)
        if sim != 1:
            heapq.heappush(h, (sim, that_doc))
    top = heapq.nlargest(top_n, h)
    return [(sim, doc.toJSON()) for sim, doc in top]

