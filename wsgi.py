#!/usr/bin/python
import os

virtenv = os.environ['APPDIR'] + '/virtenv/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.6/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

import web

urls = (
        '/', 'index',
        '/hello/(.*)', 'hello'
)

class index:
    def GET(self):
        return 'Welcome to my web site!'

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'

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
