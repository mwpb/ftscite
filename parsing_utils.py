from peewee_init import *
import os
import fileinput
import re
import sqlite3
import bibtexparser
from sys import argv

field_list = ['idstr','address','annote','author','booktitle','chapter','edition','editor','howpublished','institution','journal','month','note','number','organisation','startpage','endpage','publisher','school','series','title','ENTRYTYPE','volume','year']

def get_bibpath(tex_path):
    try:
        tex_file = open(tex_path).read()
        regex = r'^\\bibliography{(.+?)}'
        bibname = re.findall(regex,tex_file,flags=re.MULTILINE)
        bibpath = os.getcwd()+'/'+bibname[0]+'.bib'
        return bibpath
    except:
        return False

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

#def extract_entries(bib_path):
#    bibtex_str = open(bib_path).read()
#    bib_db = bibtexparser.loads(bibtex_str)
#    for entry in bib_db.entries:
#        for key in list(entry):
#            if key not in field_list:
#                del entry[key]
#        for field in field_list:
#            if field not in entry.keys():
#                entry[field] = None
#        author = ''.join(x for x in entry['author'] if x.isalnum())
#        entry['idstr'] = str(entry['year'])+author
#        try:
#            Entry.create(**entry)
#            entry_id = Entry.select().order_by(Entry.id.desc()).get().id
#            print 'entry id:', entry_id
#            entry['idstr'] = entry['idstr']+str(entry_id)
#            entry_content = ' '.join([x for x in entry.values() if x != None])
#            Entry.update(idstr=entry['idstr']).where(Entry.id == entry_id).execute()
#            EntryIndex.create(content = entry_content)
#        except:
#            print 'duplicate'
#            #Entry.insert_many(bib_db.entries).on_conflict('REPLACE').execute()
#    return bib_db.entries

def search(phrase):
    search_results = []
    query = (Entry.select(Entry).join(EntryIndex,on=(Entry.id == EntryIndex.docid)).where(EntryIndex.match(phrase)).dicts())
    for row_dict in query:
        search_results.append(row_dict)
    return search_results

def prep_phrase(phrase):
    phrase = phrase.replace(' ','* *')
    phrase = '*'+phrase+'*'
    return phrase

def search_unknown(tex_path,bib_path):
    search_results = []
    for entry in unknown_entries(tex_path,bib_path):
        result = search(entry)
        search_results.append(result)
    return search_results

def dict2bibstr(e):
    if e == []:
        return 'no entries to dump'
    dump_str = '@'+str(e['ENTRYTYPE'])+'{'+str(e['idstr'])+',\n'
    for entry in e.keys():
        if entry != 'ENTRYTYPE':
            if entry != 'idstr':
                if e[entry] != None:
                    dump_str = dump_str+entry+' = {'+str(e[entry])+'},\n'
    dump_str = dump_str+'}\n'
    return dump_str

def update_tex(tex_path,original_search,chosen_entry_idstr):
    for line in fileinput.FileInput(tex_path,inplace=1):
        line = line.replace('cite{'+original_search+'}','cite{'+chosen_entry_idstr+'}')
        print line,
    return 'tex file updated'

def update_bib(bib_path,chosen_entry):
    with open(bib_path, "a") as myfile:
        myfile.write(dict2bibstr(chosen_entry))
    return 'bib file updated'

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
    script, tex_path = argv
    print get_bibpath(tex_path)
    #print 'tex citations: ', tex_citations(tex_path)
    #print 'bib entries: ', bib_entries(bib_path)
    #print 'unknown entries', unknown_entries(tex_path,bib_path)
    #extract_entries('clean_refs.bib')
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
