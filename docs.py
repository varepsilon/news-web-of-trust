import heapq
import re
import requests

from lib import Doc2Vec

#doc_to_vec = Doc2Vec('./model/GoogleNews-vectors-negative300-SLIM.bin')
doc_to_votes = {}

def html_to_text(path):
    url = "http://fuckyeahmarkdown.com/go/"
    # construct query
    params = {
            "u": path, # url encoded URI to parse
            "read": 1, # whether to run Readability or not, 0 turns off
            "md": 1, # whether to run Markdownify or not, 0 turns off
            "output": "json", # type of text to return: json, url (encoded), or markdown
    }
    response = requests.get(url, params=params)
    words = []
    for word in response.text.split(' '):
        if re.fullmatch('[a-zA-Z_]+', word):
            words.append(word)
    return ' '.join(words)

def add_new_doc(url, user, ranking):
    content = html_to_text(url)
    if content not in doc_to_votes:
        doc_to_votes[content] = {}
    doc_to_votes[content][user] = ranking

def get_storage():
    return doc_to_votes

#def get_similar_docs(this_doc, top_n):
#    h = []
#    v1 = doc_to_vec.get_vector(this_doc)
#    for that_doc, users in doc_to_votes:
#        v2 = doc_to_vec.get_vector(that_doc)
#        sim = doc_to_vec.sim(v1, v2)
#        if sim != 1:
#            heapq.heappush(h, (v2, that_doc))
#    top = heapq.nlargest(top_n, h)

