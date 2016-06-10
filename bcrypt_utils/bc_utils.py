import bcrypt
import sqlite3
import os

dbpath = os.path.dirname(os.path.realpath(__file__))+'/db.sqlite'

def reinit_db(dbpath):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute('CREATE TABLE users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT UNIQUE, hash TEXT UNIQUE)')

def add_user(username,password):
    pwhash = bcrypt.hashpw(password,bcrypt.gensalt(14))
    print username, pwhash
    try:
        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
    except:
        print 'cannot open database'
        return False
    try:
        cur.execute('INSERT INTO users (username,hash) VALUES ( ? , ? )', (username,pwhash))
        conn.commit()
        print 'Added user', username
    except:
        print 'cannot add user possibly duplicate'
        return False
    return True

def are_valid_creds(username,password):
    try:
        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
    except:
        print 'cannot open database'
        return False
    try:
        cur.execute('SELECT hash FROM users WHERE username=?',(username,))
        pwhash = str(cur.fetchone()[0])
        print 'Found user', username
        print 'Pwhash is', pwhash
    except:
        print 'cannot find user', username, 'in database'
        return False
    if bcrypt.hashpw(password,pwhash) == pwhash:
        return True
    else:
        return False

if __name__ == '__main__':
    username = raw_input('User name:')
    password = raw_input('Password:')
    try:
        print are_valid_creds(username,password)
    except:
        print 'uncaught exception'
