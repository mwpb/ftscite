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
if os.getenv('OPENSHIFT_DATA_DIR'):
    render = web.template.render(os.environ['OPENSHIFT_REPO_DIR']+'/static/templates')
    web.config.debug = True
else:
    render = web.template.render('./templates')
    web.config.debug = True

urls = (
        '/', 'index',
        '/cite/(.*)', 'cite',
        '/upload', 'upload'
)

search_form = form.Form(
        form.Textbox('phrase',description='Search term:',value='Search'),
        form.Button('search',value=True)
        )

class index:
    def GET(self):
        search_results = []
        form = search_form()
        try:
            search_term = web.input().phrase
            form.fill({'phrase':search_term})
            #search_term = search_term.replace(' ','* AND *')
            #search_term = '*'+search_term+'*'
            search_results = search(prep_phrase(search_term))
        except:
            pass
        results_str = ''
        for result in search_results:
            print result
            results_str = results_str +dict2bibstr(result)+'\n\n'
        return render.index(form,results_str)

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
