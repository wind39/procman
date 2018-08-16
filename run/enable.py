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


import sys
import os

v_script = sys.argv[1]

if not os.path.isfile(os.path.join('run', '{0}.py'.format(v_script))):
    print('File {0}.py not found.'.format(v_script))
    sys.exit(1)

v_minute = sys.argv[2]
v_hour = sys.argv[3]
v_day_of_week = sys.argv[4]
v_day_of_month = sys.argv[5]
v_month = sys.argv[6]

v_file_content = '''[Schedule]
Exec={0}.py
Minute={1}
Hour={2}
DayOfWeek={3}
DayOfMonth={4}
Month={5}
'''.format(
    v_script,
    v_minute,
    v_hour,
    v_day_of_week,
    v_day_of_month,
    v_month
)

with open(os.path.join('cron', '{0}.conf'.format(v_script)), 'w') as v_file:
    v_file.write(v_file_content)
