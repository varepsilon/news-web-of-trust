import os
import heapq
import re
import json
import html2text
import urllib.request

from lib import Doc2Vec
from fcache.cache import FileCache

doc_to_vec = Doc2Vec('./model/GoogleNews-vectors-negative300-SLIM.bin')

# document_storage = FileCache('document_cache', flag='cs', app_cache_dir=os.path.dirname(os.path.abspath(__file__)))
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
        return {'url': self.url, 'content': content_truncated}

html_to_text_cache = FileCache('html_to_text_cache', flag='cs', app_cache_dir=os.path.dirname(os.path.abspath(__file__)))
html_to_text = html2text.HTML2Text()

def _html_to_text(path):
    if path in html_to_text_cache:
        return html_to_text_cache[path]
    resource = urllib.request.urlopen(path)
    content = resource.read()
    charset = resource.headers.get_content_charset()
    content = content.decode(charset)
    content = html_to_text.handle(content)
    words = []
    for word in content.split(' '):
        if re.fullmatch('[a-zA-Z_]+', word):
            words.append(word)
    result = ' '.join(words)
    html_to_text_cache[path] = result
    return result

def add_new_doc(url, user, ranking):
    doc = WebDocument(url)
    if url not in document_storage:
        document_storage[url] = {'doc': doc, 'ranking': {}}
    document_storage[url]['ranking'][user] = ranking

def get_storage():
    return document_storage

def get_similar_docs(this_doc_url, top_n):
    h = []
    if this_doc_url in document_storage:
        this_doc = document_storage[this_doc_url]['doc']
    else:
        this_doc = WebDocument(this_doc_url)
    v1 = this_doc.vector
    for stored in document_storage.values():
        that_doc = stored['doc']
        v2 = that_doc.vector
        sim = doc_to_vec.sim(v1, v2)
        if sim != 1:
            heapq.heappush(h, (sim, stored))
    top = heapq.nlargest(top_n, h)
    return [(sim, {
        'doc': doc_info['doc'].toJSON(),
        'ranking': json.loads(json.dumps(doc_info['ranking'])),
        }) for sim, doc_info in top]
