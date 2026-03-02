#! /usr/bin/env python

from __future__ import print_function
import sys
from optparse import OptionParser
import random

# to make Python2 and Python3 act the same -- how dumb
def random_seed(seed):
    try:
        random.seed(seed, version=1)
    except:
        random.seed(seed)
    return

parser = OptionParser()
parser.add_option('-s', '--seed', default=0, help='随机种子',              action='store', type='int', dest='seed')
parser.add_option('-j', '--jobs', default=3, help='系统中的作业数', action='store', type='int', dest='jobs')
parser.add_option('-l', '--jlist', default='', help='而不是随机作业，提供逗号分隔的运行时间和票证值列表（例如10:100,20:100表示两个作业，运行时间分别为10和20，每个都有100张票证）',  action='store', type='string', dest='jlist')
parser.add_option('-m', '--maxlen',  default=10,  help='作业的最大长度',         action='store', type='int', dest='maxlen')
parser.add_option('-T', '--maxticket', default=100, help='随机分配的最大票证值',          action='store', type='int', dest='maxticket')
parser.add_option('-q', '--quantum', default=1,   help='时间片长度', action='store', type='int', dest='quantum')
parser.add_option('-c', '--compute', help='为我计算答案', action='store_true', default=False, dest='solve')

(options, args) = parser.parse_args()

random_seed(options.seed)

print('ARG jlist', options.jlist)
print('ARG jobs', options.jobs)
print('ARG maxlen', options.maxlen)
print('ARG maxticket', options.maxticket)
print('ARG quantum', options.quantum)
print('ARG seed', options.seed)
print('')

print('以下是作业列表，包括每个作业的运行时间：')

import operator


tickTotal = 0
runTotal  = 0
joblist = []
if options.jlist == '':
    for jobnum in range(0,options.jobs):
        runtime = 0
        while runtime == 0:
            runtime = int(options.maxlen * random.random())
        tickets = 0
        while tickets == 0:
            tickets = int(options.maxticket * random.random())
        runTotal += runtime
        tickTotal += tickets
        joblist.append([jobnum, runtime, tickets])
        print('  Job %d ( length = %d, tickets = %d )' % (jobnum, runtime, tickets))
else:
    jobnum = 0
    for entry in options.jlist.split(','):
        (runtime, tickets) = entry.split(':')
        joblist.append([jobnum, int(runtime), int(tickets)])
        runTotal += int(runtime)
        tickTotal += int(tickets)
        jobnum += 1
    for job in joblist:
        print('  Job %d ( length = %d, tickets = %d )' % (job[0], job[1], job[2]))
print('\n')

if options.solve == False:
    print('以下是您需要的随机数集合（至多）：')
    for i in range(runTotal):
        r = int(random.random() * 1000001)
        print('随机', r)

if options.solve == True:
    print('** 解决方案 **\n')

    jobs  = len(joblist)
    clock = 0
    for i in range(runTotal):
        r = int(random.random() * 1000001)
        winner = int(r % tickTotal)

        current = 0
        for (job, runtime, tickets) in joblist:
            current += tickets
            if current > winner:
                (wjob, wrun, wtix) = (job, runtime, tickets)
                break

        print('随机', r, '-> 获胜票 %d (共 %d) -> 运行 %d' % (winner, tickTotal, wjob))
        # print('Winning ticket %d (of %d) -> Run %d' % (winner, tickTotal, wjob))

        print('  作业：',)
        for (job, runtime, tickets) in joblist:
            if wjob == job:
                wstr = '*'
            else:
                wstr = ' '

            if runtime > 0:
                tstr = tickets
            else:
                tstr = '---'
            print(' (%s 作业:%d 剩余时间:%d 票:%s ) ' % (wstr, job, runtime, tstr), end='')
        print('')

        # now do the accounting
        if wrun >= options.quantum:
            wrun -= options.quantum
        else:
            wrun = 0

        clock += options.quantum

        # job completed!
        if wrun == 0:
            print('--> 作业 %d 在时间 %d 完成' % (wjob, clock))
            tickTotal -= wtix
            wtix = 0
            jobs -= 1

        # update job list
        joblist[wjob] = (wjob, wrun, wtix)

        if jobs == 0:
            print('')
            break




