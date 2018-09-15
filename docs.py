import heapq
import os
import re
import json
import urllib.request

import newspaper
import shelve

from lib import Doc2Vec

doc_to_vec = Doc2Vec('./model/GoogleNews-vectors-negative300-SLIM.bin')

document_storage = shelve.open('document_storage.cache')

class WebDocument:
    def __init__(self, url, content=None, summary=None, vector=None):
        if content is None:
            content, summary = _get_content_and_summary(url)
        if summary is None or len(summary) == 0:
            summary = content[:300]
            if len(summary) < len(content):
                summary = summary[:-3] + '...'
        if vector is None:
            vector = doc_to_vec.get_vector(content)
        self.url = url
        self.content = content
        self.summary = summary
        self.vector = vector

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        return {'url': self.url, 'content': self.summary}

content_and_summary_cache = shelve.open('content_and_summary.cache')

def _get_content_and_summary(path):
    if path not in content_and_summary_cache:
        news_article = newspaper.Article(path)
        news_article.download()
        news_article.parse()
        content_and_summary_cache[path] = (
                news_article.text, news_article.summary)
        content_and_summary_cache.sync()
    return content_and_summary_cache[path]

def add_new_doc(url, user, ranking):
    if url not in document_storage:
        doc = WebDocument(url)
        document_storage[url] = {'doc': doc, 'ranking': {}}
    document_storage[url]['ranking'][user] = ranking
    document_storage.sync()

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

