from peewee_init import *

def get_entry_by_id(entry_id):
    entry = Entry.get(Entry.id == entry_id)
    return entry._data

def delete_entry_by_id(entry_id):
    pass

if __name__ == '__main__':
    print get_entry_by_id(72)
