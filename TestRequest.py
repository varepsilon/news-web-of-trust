import requests
import json
import httplib2
import nltk
def TestRequest():
    #nltk.download('punkt')

    data={
     'url':'https://www.bbc.com/news/world-us-canada-45517260'
    }
    r=requests.put('http://127.0.0.1:8000/storage', data = data)
    print(r)
if __name__ == '__main__':
    TestRequest()