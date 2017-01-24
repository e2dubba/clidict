#!/usr/bin/env python3
'''
Add docstring.
Add urlib.parse.quote()
'''

import requests, json
from collist import collist


def hyphen_range(num_string):
    """
    Takes a string of numbers, splits it according to commas, then splits it
    according to hyphens, and then fills out the assumed numbers. Returns a
    list of numbers. Inspired by stackoverflow:
    http://stackoverflow.com/questions/9847601/convert-list-of-numbers-to-string-ranges
    """
    num_list = []
    num_string = num_string.strip()
    for numb in num_string.split(','):
        elem = numb.split('-')
        if len(elem) == 1:
            num_list.append(elem.pop())
        if len(elem) == 2:
            start, end = map(int, elem)
            for i in range(start, end+1):
                num_list.append(i)
        else:
            continue
    return num_list


def parse_input(new_defs, meanings, phrase):
    '''
    Takes the user input list, and then applies it to the list and the
    dictionary derived from the json file from glosbe.
    '''
    for item in new_defs:
        item = item.strip()
        item = item.split(':')
        if item[0] == 'm':
            range_list = hyphen_range(item[1])
            meanstr = '; '.join([meanings[int(i)] for i in range_list])
        if item[0] == 'p':
            range_list = hyphen_range(item[1])
            glosstr = '; '.join([phrase[int(i)] for i in range_list])
    return meanstr, glosstr


def querry_glosbe(lang, term):
    '''
    returns a list and a set based on the json file retrieved from glosbe.com
    '''
    url = 'http://glosbe.com/gapi/translate?from=' + lang + \
      '&dest=eng&format=json&phrase=' + term + \
        '&pretty=true'

    res = requests.get(url)
    # need to add a try statement
    json_dict = json.loads(res.text)

    tuc = json_dict['tuc']

    meanings = []
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
    return meanings, phrase

    
def for_print(meanings, phrase):
    '''
    takes a list and a set to print them in stdout in beautiful colummns thanks
    to ninjaaron's rainbow poo. Returns the set as a dictionary. 
    '''
    glossdict = dict(enumerate(phrase))
    print('phrase' + ':\n' + collist(glossdict))
    print('meanings' + ':\n' + collist(dict(enumerate(meanings))))
    return glossdict


def user_input():
    '''
    The user interface to select different translation values
    '''
    new_defs = input('Enter Selection like:\nm:M0-Mn, Mx, My | p:P0-Pn, Px, Py\n'+\
            'l <for leo> x <for exit>\n')
    if new_defs == 'l':
        import webbrowser
        url = 'https://dict.leo.org/ende/index_de.html#/search=' + \
                term + '&searchLoc=0&resultOrder=basic&multiwordShowSingle=on'
        webbrowser.open(url)
        sys.exit()
    if new_defs == 'x':
        sys.exit() 
    else: 
        new_defs = new_defs.split('|')
        return new_defs
    

if __name__ == '__main__':
    import sys
    import os 
    lang = sys.argv[0].split('/')[-1]
    term = ' '.join(sys.argv[1:])
    file_loc = os.getenv('HOME') + '/' + lang + '.csv'
    new_vocab = open(file_loc, 'a')
    meanings, phrase = querry_glosbe(lang, term)
    glossdict = for_print(meanings, phrase)
    new_defs = user_input() 
    meanings, glosses = parse_input(new_defs, meanings, glossdict) 
    new_vocab.write(term + ', ' + meanings + ', ' + glosses + '\n')
    new_vocab.close()
    
