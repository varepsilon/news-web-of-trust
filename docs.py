import re
import requests

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
