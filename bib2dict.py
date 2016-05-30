from pyparsing import Literal,Word,nestedExpr,alphas
from sys import argv
import bibtexparser

fieldlist = ['uniquestr','idstr','address','annote','author','booktitle','chapter','edition','editor','howpublished','institution','journal','month','note','number','organization','pages','publisher','school','series','title','ENTRYTYPE','type','volume','year']

def bibfile2dict(bibpath):
    bibstr = open(bibpath).read()
    return bibstr2dict(bibstr)

def bibstr2dict(bibstr):
    bibdict = bibtexparser.loads(bibstr)
    return bibdict.entries

def clean_bibdict(bibdict):
    for entry in bibdict:
        for key in entry.keys():
            if key not in fieldlist:
                del entry[key]
        for field in fieldlist:
            if field not in entry.keys():
                entry[field] = None
    return bibdict

if __name__ == '__main__':
    script, bib_path = argv
    for entry in clean_bibdict(bibfile2dict(bib_path)):
        print entry
