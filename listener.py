'''
MIT License

Copyright (c) 2017 William Ivanski

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


from http.server import BaseHTTPRequestHandler, HTTPServer
import settings
from utils import syscall, syscall_bg

class Request:
    def __init__(self, p_url):
        tmp = p_url.split('?')
        self.v_hook = tmp[0].strip('/')
        tmp2 = self.v_hook.split('/')
        self.v_mode = tmp2[0]
        self.v_controller = tmp2[1]
        self.v_program = settings.CONTROLLERS[self.v_controller]
        self.v_script = '/'.join(tmp2[2:])
        if len(tmp) > 1:
            self.v_parameters = tmp[1].split('&')
        else:
            self.v_parameters = []
        self.v_command = self.v_program + ' run/' + self.v_script + ' ' + ' '.join(self.v_parameters)
        self.v_filename = 'a.out'
    def execute(self):
        if self.v_mode == 'fg':
            out = syscall(self.v_command)
        else:
            out = syscall_bg(self.v_command)
        if out:
            return '\n'.join(out)
        else:
            return ''

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            r = Request(self.path)
            message = r.execute()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Disposition', 'attachment; filename=""'.format(r.v_filename))
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))
        except Exception as exc:
            print('procman error: {0}'.format(str(exc)))
        return

if __name__ == "__main__":
    httpd = HTTPServer((settings.ADDRESS, settings.PORT), RequestHandler)
    print('procman {0} listener running on {1}:{2}...'.format(settings.VERSION, settings.ADDRESS, settings.PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('')
        print('exiting procman listener...')
