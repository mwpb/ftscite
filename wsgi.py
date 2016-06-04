#!/usr/bin/python
import os

if os.getenv('OPENSHIFT_DATA_DIR'):
    virtenv = os.environ['APPDIR'] + '/virtenv/'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.7/site-packages')
    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
    try:
        execfile(virtualenv, dict(__file__=virtualenv))
    except IOError:
        pass

import web
from web import form
import json
from parsing_utils import *
from bib2dict import *
from dict2sql import *
from sql_query import *

if os.getenv('OPENSHIFT_DATA_DIR'):
    render = web.template.render(os.environ['OPENSHIFT_REPO_DIR']+'/templates',base='layout')
    web.config.debug = False
else:
    render = web.template.render('./templates',base='layout')
    web.config.debug = True

urls = (
        '/', 'index',
        '/cite/(.*)', 'cite',
        '/upload', 'upload',
        '/delete/(.*)/', 'delete',
        '/delete/(.*)/yes', 'delete_yes'
)

search_form = form.Form(
        form.Textbox('phrase',description='Search term:'),
        form.Button('search',value=True)
        )

class index:
    def GET(self):
        search_results = []
        search_term = ''
        entry_id = 0
        form = search_form()
        try:
            search_term = web.input().phrase
            form.fill({'phrase':search_term})
            search_results = search(prep_phrase(search_term))
        except:
            pass
        bib_results = map(dict2bibstr,search_results)
        result_ids = map(lambda x:x['id'],search_results)
        search_results = zip(bib_results,result_ids)
        return render.index(form,search_results)

class cite:
    def GET(self,phrase):
        phrase = phrase.replace(' ','* AND *')
        phrase = '*'+phrase+'*'
        web.header('Content-Type','application/json')
        return json.dumps(search(phrase),indent=4)

class upload:
    def GET(self):
        return render.upload('',0)

    def POST(self):
        x = web.input(myfile={})
        web.debug(x['myfile'].filename) 
        bibstr = x['myfile'].value
        web.debug(x['myfile'].file.read()) 
        bibdict = clean_bibdict(bibstr2dict(bibstr))
        idstrs_added, duplicate_count = extract_entries(bibdict)
        print '\n\nIdStr:',idstrs_added,'\n\n'
        return render.upload(idstrs_added,duplicate_count)

class delete:
    def GET(self,entry_id):
        entry = get_entry_by_id(entry_id)
        bibstr = dict2bibstr(entry)
        return render.delete(entry_id,bibstr)

class delete_yes:
    def GET(self,entry_id):
        delete_entry_by_id(entry_id)
        return render.delete_yes(entry_id)

if os.getenv('OPENSHIFT_DATA_DIR'):
    application = web.application(urls, globals()).wsgifunc()
    if __name__ == '__main__':
        from wsgiref.simple_server import make_server
        httpd = make_server('localhost', 8080, application)
        # Wait for a single request, serve it and quit.
        httpd.handle_request()
        # app = web.application(urls, globals())
        # app.run()
else:
    if __name__ == '__main__':
        app = web.application(urls,globals())
        app.run()
