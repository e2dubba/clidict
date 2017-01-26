#!/usr/bin/env python3
'''
This is a command line dual language dictionary. It uses the API provided by
Glosbe to look up words in many many languages and return them in attractive
formats at the command line. In addition, you can save the glosses and
definitions you want to save into a csv. This can be imported then into a
flaschcard program; notably Anki.
The ideal way of useing this script is to create a symbolic link to this file
using the ISO abbreviation for the language you want to look up. 
For a list of languages see: https://glosbe.com/all-languages
For German:
    $ ln -s /path/to/dictionary.py /in/your/path/deu
and call it:
    $ deu Wort
'''

import requests, json
from collist import collist
import urllib
import sys


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
            meanstr = meanstr.replace(',', ':')
        if item[0] == 'p':
            range_list = hyphen_range(item[1])
            glosstr = '; '.join([phrase[int(i)] for i in range_list])
            glosstr = glosstr.replace(',', ':')
    return meanstr, glosstr


def querry_glosbe(lang, term):
    '''
    returns a list and a set based on the json file retrieved from glosbe.com
    '''
    url = 'http://glosbe.com/gapi/translate?from=' + lang + \
      '&dest=eng&format=json&phrase=' + urllib.parse.quote(term) + \
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


def user_input(term):
    '''
    The user interface to select different translation values
    '''
    new_defs = input('Enter Selection like:\nm:M0-Mn, Mx, My | p:P0-Pn, Px, Py\n'+\
            'l <for leo> x <for exit>\n')
    if new_defs == 'l':
        url = 'https://dict.leo.org/ende/index_de.html#/search=' + \
                urllib.parse.quote(term) + '&searchLoc=0&resultOrder=basic&multiwordShowSingle=on'
        webbrowser.open(url)
        sys.exit()
    if new_defs == 'x':
        sys.exit() 
    if new_defs == '':
        new_defs = ['m:0', 'p:0-3']
        return new_defs
    else: 
        new_defs = new_defs.split('|')
        return new_defs
    
#def google_translate(term):


def main():
    '''
    if a.googTranslate:
        google_translate(term)
        sys.exit()
    '''

    ap = argparse.ArgumentParser()
    ap.add_argument('term', nargs='+')
    ap.add_argument('-l', '--lang', help='specify the language to look' + \
            ' up--use iso codes')
    ap.add_argument('-s', '--simple', help='look up a word without ' + \
            'adding it to the csv', action='store_true')
    ap.add_argument('-gT', '--googTranslate', help='return results from ' +\
            'Google Translate', action='store_true')
    ap.add_argument('-m' , '--manual', help='add terms manually to the ' +\
            'csv for the specified language. Format: \'term, glosses, ' +\
            'meaning\'', action='store_true')
    a = ap.parse_args()
    term = ' '.join(a.term)
    if a.lang: 
        lang = a.lang
    else: 
        lang = os.path.basename(sys.argv[0])

    if a.simple:
        meanings, phrase = querry_glosbe(lang, term)
        _ = for_print(meanings, phrase)
        sys.exit()
    else:
        file_dir = os.getenv('HOME') + '/.clidict/' 
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        csv_file = file_dir + lang + '.csv'
        new_vocab = open(csv_file, 'a')
        if a.manual:
            new_vocab.write(term + '\n')
            sys.exit()
        meanings, phrase = querry_glosbe(lang, term)
        glossdict = for_print(meanings, phrase)
        new_defs = user_input(term) 
        meanings, glosses = parse_input(new_defs, meanings, glossdict) 
        new_vocab.write(term + ', ' + glosses + ', ' + meanings + '\n')
        new_vocab.close()
 

if __name__ == '__main__':
    import os 
    import webbrowser
    import argparse
    main()
   
