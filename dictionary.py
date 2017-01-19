#!/usr/bin/env python3

import requests, json
import sys
import pprint

lang = sys.argv[0].split('/')[-1]
term = ' '.join(sys.argv[1:])
url = 'http://glosbe.com/gapi/translate?from=' + lang + \
      '&dest=eng&format=json&phrase=' + term + \
        '&pretty=true'


res = requests.get(url)
# need to add a try statement
json_dict = json.loads(res.text)

tuc = json_dict['tuc']

meanings = ['meanings', ]
phrase = []
for i in tuc:
    try:
        data = i['meanings']
        data = data[0]['text']
        meanings.append(data)
    except KeyError:
        data = i['phrase']
        data = data['text']
        phrase.append(data)
 
phrase = set(phrase)
print(meanings[0] + ':\t' + '\n\t\t'.join(meanings[1:]))
print('phrase' + ':\t\t' + '\n\t\t'.join(phrase))


