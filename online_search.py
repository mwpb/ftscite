import urllib
from sys import argv
import json

def online_search(phrase):
    url_str = 'http://ftscite-mwpb.rhcloud.com/cite/'+phrase.replace(' ','%20')
    json_str = urllib.urlopen(url_str).read()
    json_data = json.loads(json_str)
    return json_data

if __name__ == '__main__':
    script, phrase = argv
    print online_search(phrase)
