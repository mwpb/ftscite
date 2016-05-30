from peewee import *
from playhouse.sqlite_ext import *
from os.path import expanduser
import os
import errno

if os.getenv('OPENSHIFT_DATA_DIR'):
    dbFolder = os.environ.get('OPENSHIFT_DATA_DIR')
else:
    dbFolder = './database/'

try: 
    os.makedirs(dbFolder)
except OSError:
    if not os.path.isdir(dbFolder):
        raise

dbPath = dbFolder + 'bibDatabase.sqlite'

db = SqliteExtDatabase(dbPath)

class Entry(Model):
    title = CharField()
    idstr = CharField()
    uniquestr = CharField(unique=True)
    address= CharField(null=True)
    annote= CharField(null=True)
    author= CharField()
    booktitle= CharField(null=True)
    chapter= CharField(null=True)
    edition= CharField(null=True)
    editor= CharField(null=True)
    howpublished= CharField(null=True)
    institution= CharField(null=True)
    journal= CharField(null=True)
    month= CharField(null=True)
    note= CharField(null=True)
    number= IntegerField(null=True)
    organisation= CharField(null=True)
    startpage= IntegerField(null=True)
    endpage= IntegerField(null=True)
    publisher= CharField(null=True)
    school= CharField(null=True)
    series= CharField(null=True)
    ENTRYTYPE= CharField(null=True)
    volume= IntegerField(null=True)
    year= IntegerField(null=True)

    class Meta:
        database = db

class EntryIndex(FTSModel):
    content = SearchField()

    class Meta:
        database = db

if __name__ == '__main__':
    db.connect()
    Entry.create_table()
    EntryIndex.create_table()
    Entry.create(title='dummy',author='dummy',uniquestr='dummy',idstr='dummy')
    EntryIndex.create(content='dummy')
