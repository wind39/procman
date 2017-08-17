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


import sys
import optparse
import requests
import settings

if __name__ == "__main__":

    parser = optparse.OptionParser(version=settings.VERSION)
    parser.add_option('-l', '--list-servers', dest='listservers', default=False, action="store_true", help='list servers: -l')
    parser.add_option('-s', '--server', dest='server', nargs=1, default='localhost', help='specify server: -s <server>')
    parser.add_option('-m', '--mode', dest='mode', nargs=1, default='fg', help='specify execution mode: -m <fg|bg>')
    parser.add_option('-p', '--program', dest='program', nargs=1, default='check.py', help='specify program to be executed: -c <program>')
    parser.add_option('-a', '--arguments', dest='arguments', nargs=1, default=False, help='specify program arguments: -a <arg1,arg2,...>')
    (options, args) = parser.parse_args()

    if options.listservers:
        for key, value in settings.SERVERS.items():
            print('{0} = {1}'.format(key, value))
        sys.exit(0)
    else:
        url = 'http://'
        if options.server:
            if options.server in settings.SERVERS:
                url = url + settings.SERVERS[options.server]
            else:
                print('ERROR: There is no server "{0}".'.format(options.server))
                sys.exit(1)
        else:
            if 'localhost' in settings.SERVERS:
                url = url + settings.SERVERS[options.server]
            else:
                print('ERROR: There is no server "localhost".')
                sys.exit(1)
        if options.mode:
            if options.mode in ['fg', 'bg']:
                url = url + '/' + options.mode
            else:
                print('ERROR: There is no mode "{0}".'.format(options.mode))
                sys.exit(1)
        else:
            url = url + '/fg'
        if options.program:
            url = url + '/' + options.program
        else:
            print('ERROR: You need to specify a program to be executed.')
            sys.exit(1)
        if options.arguments:
            url = url + '?' + options.arguments.replace(',', '&')

        r = requests.get(url)
        print(r.text)
