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

import settings
from utils import *

out = syscall('ps aux | grep "python listener.py" | grep -v grep | tr -s " " | cut -d " " -f 2')['stdout']
if len(out) > 0:
    msg1 = 'procman {0} listener is running on {1}:{2} with PID {3}'.format(settings.VERSION, settings.ADDRESS, settings.PORT, out[0])
else:
    msg1 = 'procman {0} listener is not running on {1}:{2}'.format(settings.VERSION, settings.ADDRESS, settings.PORT)

out = syscall('ps aux | grep "python cron.py" | grep -v grep | tr -s " " | cut -d " " -f 2')['stdout']
if len(out) > 0:
    msg2 = 'procman {0} cron is running on {1}:{2} with PID {3}'.format(settings.VERSION, settings.ADDRESS, settings.PORT, out[0])
else:
    msg2 = 'procman {0} cron is not running on {1}:{2}'.format(settings.VERSION, settings.ADDRESS, settings.PORT)

if settings.SLACK['enabled']:
    notify('procman status on server {0}:\n```\n{1}\n{2}\n```'.format(settings.ADDRESS, msg1, msg2))

print(msg1)
print(msg2)
