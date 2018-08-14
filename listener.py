'''
MIT License

Copyright (c) 2017-2018 William Ivanski
Copyright (c) 2018 Israel Barth Rubio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import tornado.httpserver
import tornado.ioloop
import tornado.web
import ssl
import settings
from utils import *

class Request:
    def __init__(self, p_url):
        v_tmp = p_url.split('?')
        v_hook = v_tmp[0].strip('/')
        v_tmp2 = v_hook.split('/')
        self.mode = v_tmp2[0]
        self.script = '/'.join(v_tmp2[1:])

        if len(v_tmp) > 1:
            self.parameters = v_tmp[1].replace('*', '\*').split('&')
        else:
            self.parameters = []

        self.command = 'python run/' + self.script + ' ' + ' '.join(self.parameters)
        self.fileName = 'a.out'

    def execute(self):
        v_output = None

        if self.mode == 'fg':
            v_output = syscall(self.command)['stdout']
        elif self.mode == 'bg':
            v_output = syscall_bg('{0} > /dev/null'.format(self.command))

        if v_output:
            return '\n'.join(v_output)
        else:
            return ''

class RequestHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            print(self.request.uri)
            v_request = Request(self.request.uri)
            v_message = v_request.execute()
            self.set_header('Content-Type', 'text/plain')
            self.set_header('Content-Disposition', 'attachment; filename=""'.format(v_request.fileName))
            self.write(v_message)
            self.finish()
            print(v_message)
        except Exception as exc:
            print('procman error: {0}'.format(str(exc)))
            notify('procman error: {0}'.format(str(exc)))

if __name__ == '__main__':
    try:
        print('procman {0} listener running on {1}:{2}...'.format(settings.VERSION, settings.ADDRESS, settings.PORT))

        v_app = tornado.web.Application([
            (r'/.*', RequestHandler),
        ])

        v_server = None

        if settings.SSL['enabled']:
            v_ssl = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            v_ssl.load_cert_chain(settings.SSL['CERTIFICATE'], settings.SSL['KEY'])

            v_server = tornado.httpserver.HTTPServer(
                v_app,
                ssl_options = v_ssl
            )
        else:
            v_server = tornado.httpserver.HTTPServer(v_app)

        v_server.listen(settings.PORT)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt as exc:
        print('Exiting ProcMan Listener')
