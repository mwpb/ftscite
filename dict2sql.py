from peewee_init import *

def extract_entry(entry):
    author = ''
    try:
        author = ''.join(x for x in entry['author'] if x.isalnum())
    except:
        pass
    entry['idstr'] = str(entry['year'])+author
    entry['uniquestr'] = str(entry['year'])+author+''.join(x for x in entry['title'] if x.isalnum())
    entry['uniquestr'] = entry['uniquestr'].lower()
    print entry['uniquestr']
    try:
        Entry.create(**entry)
        entry_id = Entry.select().order_by(Entry.id.desc()).get().id
        entry['idstr'] = entry['idstr']+str(entry_id)
        entry_content = ' '.join([x for x in entry.values() if x != None])
        Entry.update(idstr=entry['idstr']).where(Entry.id == entry_id).execute()
        EntryIndex.create(content = entry_content)
        print 'Created entry with idstr:', entry['idstr']
        return True
    except:
        print 'Entry ', entry['idstr'], ' not created. Perhaps duplicate.'
        return False

def extract_entries(bibdict):
    idstrs_added = []
    duplicate_count = 0
    for entry in bibdict:
        if type(entry) != dict:
            print error
        elif extract_entry(entry):
            idstrs_added.append(entry['uniquestr'])
        else:
            duplicate_count = duplicate_count +1
    return idstrs_added, duplicate_count
