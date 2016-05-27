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
if os.getenv('OPENSHIFT_DATA_DIR'):
    render = web.template.render(os.environ['OPENSHIFT_REPO_DIR']+'/templates')
else:
    render = web.template.render('./templates')
    web.config.debug = True

urls = (
        '/', 'index',
        '/cite/(.*)', 'cite'
)

search_form = form.Form(
        form.Textbox('phrase',description='Search term:',autofocus='autofocus'),
        form.Button('Search',value=True)
        )

class index:
    def GET(self):
        search_results = []
        form = search_form()
        try:
            search_term = web.input().phrase
            form.fill({'phrase':search_term})
            search_term = search_term.replace(' ','* AND *')
            search_term = '*'+search_term+'*'
            search_results = search(search_term)
        except:
            pass
        results_str = ''
        for result in search_results:
            results_str = results_str +dict2bibstr(result)+'\n\n'
        return render.index(form,results_str)

class cite:
    def GET(self,phrase):
        phrase = phrase.replace(' ','* AND *')
        phrase = '*'+phrase+'*'
        web.header('Content-Type','application/json')
        return json.dumps(search(phrase),indent=4)

#
# Below for testing only
#

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
