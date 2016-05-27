#!/usr/bin/python
import os

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
render = web.template.render(os.environ['OPENSHIFT_REPO_DIR']+'/templates')
web.config.debug = True
urls = (
        '/', 'index',
        '/cite/(.*)', 'cite'
)

search_form = form.Form(
        form.Textbox('phrase',description='Search term:'),
        form.Button('Search',value=True)
        )

class index:
    def GET(self):
        search_results = []
        try:
            search_term = web.input().phrase
            search_results = search(search_term)
        bibstr = ''
        if list:
            for result in search_results:
                bibstr = bibstr+dict2bibstr(search_results)+'\n\n'
        form = search_form()
        return render.index(form,bibstr)

class cite:
    def GET(self, phrase):
        phrase = phrase.replace(' ','% AND %')
        phrase = '%'+phrase+'%'
        web.header('Content-Type','application/json')
        return json.dumps(search(phrase),indent=4)

application = web.application(urls, globals()).wsgifunc()

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8080, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
    # app = web.application(urls, globals())
    # app.run()
