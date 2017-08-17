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


from datetime import datetime
import time
import settings
from utils import *

def get_schedule():
    out = syscall('ls -1 cron/')
    out.remove('settings.py')
    out.remove('utils.py')
    s = {}
    for p in out:
        t = p.split('_')
        s[t[1]] = int(t[0])
    return s

def update_schedule(s1, s2):
    s = {}
    for k1, v1 in s1.items():
        if k1 in s2:
            if s1[k1] <= 0:
                s[k1] = s2[k1]
            else:
                s[k1] = s1[k1]
    for k2, v2 in s2.items():
        if k2 not in s:
            print('{0}: running {1}'.format(datetime.now(), k2))
            syscall_bg('python run/{0} > /dev/null'.format(k2))
            s[k2] = s2[k2]
    return s

def run_schedule(s):
    for key, value in s.items():
        s[key] = s[key] - settings.CRONSNAP
        if s[key] <= 0:
            print('{0}: running {1}'.format(datetime.now(), key))
            syscall_bg('python run/{0} > /dev/null'.format(key))
    return s

if __name__ == "__main__":
    try:
        print('procman {0} cron running...'.format(settings.VERSION))
        s1 = {}
        while True:
            s2 = get_schedule()
            s1 = update_schedule(s1, s2)
            s1 = run_schedule(s1)
            print('{0}: current schedule: {1}'.format(datetime.now(), s1))
            time.sleep(settings.CRONSNAP)

    except KeyboardInterrupt:
        print('')
        print('exiting procman cron...')
