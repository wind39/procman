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


import os
import datetime
import time
from configparser import ConfigParser
import traceback
import settings
from utils import syscall_bg, notify


class Schedule:
    def __init__(self, p_exec='', p_minute='0', p_hour='*', p_dayOfWeek='*', p_dayOfMonth='*', p_month='*'):
        self.exec = p_exec.strip()
        self.minute = p_minute.strip()
        self.hour = p_hour.strip()
        self.dayOfWeek = p_dayOfWeek.strip()
        self.dayOfMonth = p_dayOfMonth.strip()
        self.month = p_month.strip()

    def __str__(self):
        return '\n'.join([
            'Exec={0}'.format(self.exec),
            'Minute={0}'.format(self.minute),
            'Hour={0}'.format(self.hour),
            'DayOfWeek={0}'.format(self.dayOfWeek),
            'DayOfMonth={0}'.format(self.dayOfMonth),
            'Month={0}'.format(self.month)
        ])

    def parse(self, p_attr='Minute'):
        v_attr = None
        v_defaultStart = 0
        v_defaultEnd = -1

        if p_attr == 'Minute':
            v_attr = self.minute
            v_defaultStart = 0
            v_defaultEnd = 59
        elif p_attr == 'Hour':
            v_attr = self.hour
            v_defaultStart = 0
            v_defaultEnd = 23
        elif p_attr == 'DayOfWeek':
            v_attr = self.dayOfWeek
            v_defaultStart = 1
            v_defaultEnd = 7
        elif p_attr == 'DayOfMonth':
            v_attr = self.dayOfMonth
            v_defaultStart = 1
            v_defaultEnd = 31
        elif p_attr == 'Month':
            v_attr = self.month
            v_defaultStart = 1
            v_defaultEnd = 12
        else:
            return []

        v_parseList = []

        for v_instance in v_attr.split(','):
            v_instanceParseList = []
            v_step = None
            v_start = None
            v_end = None

            if '*' in v_instance:
                v_step = 1

                if v_instance != '*':
                    if '/' in v_instance:
                        v_step = int(v_instance.split('/')[1])
            elif '-' in v_instance:
                v_step = 1

                if '/' in v_instance:
                    v_tokens = v_instance.split('/')
                    v_step = int(v_tokens[1])

                    v_tokens2 = v_tokens[0].split('-')
                    v_start = int(v_tokens2[0])
                    v_end = int(v_tokens2[1])
                else:
                    v_tokens = v_instance.split('-')
                    v_start = int(v_tokens[0])
                    v_end = int(v_tokens[1])
            else:
                v_step = 1
                v_start = int(v_instance)
                v_end = int(v_instance)

            if v_start is None or v_start < v_defaultStart:
                v_start = v_defaultStart

            if v_end is None or v_end > v_defaultEnd:
                v_end = v_defaultEnd

            for i in range(v_start, v_end + 1, v_step):
                v_instanceParseList.append(i)

            v_parseList.extend(v_instanceParseList)

        return list(set(v_parseList))

    def Run(self, p_timeStamp):
        if p_timeStamp.minute not in self.parse('Minute'):
            return

        if p_timeStamp.hour not in self.parse('Hour'):
            return

        if p_timeStamp.isoweekday() not in self.parse('DayOfWeek'):
            return

        if p_timeStamp.day not in self.parse('DayOfMonth'):
            return

        if p_timeStamp.month not in self.parse('Month'):
            return

        print(str(self))

        syscall_bg('python run/{0} > /dev/null'.format(self.exec))


def RunSchedule():
    v_now = datetime.datetime.now()

    print('Running Schedule at {0}'.format(str(v_now)))

    for v_file in os.listdir(os.path.join('.', 'cron')):
        try:
            v_config = ConfigParser()
            v_config.read(os.path.join('.', 'cron', v_file))

            v_schedule = Schedule(
                v_config.get('Schedule', 'Exec'),
                v_config.get('Schedule', 'Minute'),
                v_config.get('Schedule', 'Hour'),
                v_config.get('Schedule', 'DayOfWeek'),
                v_config.get('Schedule', 'DayOfMonth'),
                v_config.get('Schedule', 'Month')
            )

            v_schedule.Run(v_now)
        except Exception as exc:
            notify('Problem occurred in ProcMan Cron at {0}:\n{1}'.format(settings.ADDRESS, traceback.format_exc()))


if __name__ == "__main__":
    try:
        notify('procman {0} cron running at {1}...'.format(settings.VERSION, settings.ADDRESS))

        v_start = datetime.datetime.now()
        v_next = v_start + datetime.timedelta(minutes=1)

        while True:
            RunSchedule()
            v_now = datetime.datetime.now()
            v_sleep = (v_next - v_now).total_seconds()
            time.sleep(v_sleep)
            v_next = v_next + datetime.timedelta(minutes=1)
    except KeyboardInterrupt:
        notify('exiting procman {0} cron running at {1}...'.format(settings.VERSION, settings.ADDRESS))
    except Exception as exc:
        notify('Problem occurred in ProcMan Cron at {0}:\n{1}'.format(settings.ADDRESS, traceback.format_exc()))
