from peewee_init import *
import fileinput
import re
import sqlite3
import bibtexparser
from sys import argv

field_list = ['address','annote','author','booktitle','chapter','edition','editor','howpublished','institution','journal','month','note','number','organisation','startpage','endpage','publisher','school','series','title','ENTRYTYPE','volume','year']

def tex_citations(file_path):
    tex_file = open(file_path).read()
    regex = r"\\"+'cite{(.+?)}'
    citation_list = re.findall(regex,tex_file)
    return citation_list

def bib_entries(file_path):
    bib_file = open(file_path).read()
    regex = r'^@.+{(.+),'
    entries_list = re.findall(regex,bib_file,flags=re.MULTILINE)
    return entries_list

def unknown_entries(tex_path,bib_path):
    diff = set(tex_citations(tex_path))-set(bib_entries(bib_path))
    return list(diff)

def extract_entries(bib_path):
    bibtex_str = open(bib_path).read()
    bib_db = bibtexparser.loads(bibtex_str)
    for entry in bib_db.entries:
        for key in list(entry):
            if key not in field_list:
                del entry[key]
        for field in field_list:
            if field not in entry.keys():
                entry[field] = None
        entry_content = ' '.join([x for x in entry.values() if x != None])
        try:
            Entry.create(**entry)
            EntryIndex.create(content = entry_content)
        except:
            print 'duplicate'
    #Entry.insert_many(bib_db.entries).on_conflict('REPLACE').execute()
    return bib_db.entries

def search(phrase):
    query = (Entry.select(Entry).join(EntryIndex,on=(Entry.id == EntryIndex.docid)).where(EntryIndex.content.contains(phrase.split(' '))).dicts())
    search_results = []
    for row_dict in query:
        search_results.append(row_dict)
    return search_results

def search_unknown(tex_file,bib_file):
    search_results = []
    for entry in unknown_entries(tex_path,bib_path):
        result = search(entry)
        search_results.append(result)
    return search_results

def dict2bibstr(e):
    if e == []:
        return 'no entries to dump'
    nick = str(e['id'])
    nickname = ''.join(x for x in nick if x.isalnum())
    dump_str = '@'+e['ENTRYTYPE']+'{'+nickname+',\n'
    for entry in e.keys():
        if entry != 'ENTRYTYPE':
            if e[entry] != None:
                dump_str = dump_str+entry+' = {'+str(e[entry])+'},\n'
    dump_str = dump_str+'}\n'
    return dump_str

def dump_entry(old_nick,e,bib_file,tex_file):
    if e == []:
        return 'no entries to dump'
    nick = str(e['year'])+e['author']+str(e['id'])
    nickname = ''.join(x for x in nick if x.isalnum())
    dump_str = '@'+e['ENTRYTYPE']+'{'+nickname+',\n'
    for entry in e.keys():
        if entry != 'ENTRYTYPE':
            if e[entry] != None:
                dump_str = dump_str+entry+' = {'+str(e[entry])+'},\n'
    dump_str = dump_str+'}\n'
    with open(bib_file, "a") as myfile:
        myfile.write(dump_str)
    for line in fileinput.FileInput(tex_file,inplace=1):
        line = line.replace('cite{'+old_nick+'}','cite{'+nickname+'}')
        print line,
    return dump_str

if __name__ == '__main__':
    script, tex_path, bib_path = argv
    #print 'tex citations: ', tex_citations(tex_path)
    #print 'bib entries: ', bib_entries(bib_path)
    #print 'unknown entries', unknown_entries(tex_path,bib_path)
    extract_entries('clean_refs.bib')
    ##print 'actual entries:', extract_entries(bib_path)
    #print search('sneak')
    #diff = unknown_entries(tex_path,bib_path)
    #if diff != []:
    #    for entry in diff:
    #        print 'search term:', entry
    #        search_results = search(entry)
    #        for counter,result in enumerate(search_results):
    #            print 'Entry number:', counter
    #            print dict2bibstr(result)
    #        if search_results != [[]]:
    #            choice = int(raw_input('No. of correct entry:'))
    #            dump_entry(entry,search_results[choice],bib_path,tex_path)
