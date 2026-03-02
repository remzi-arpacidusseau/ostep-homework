#! /usr/bin/env python

from __future__ import print_function
import sys
from optparse import OptionParser
import random
import math

# to make Python2 and Python3 act the same -- how dumb
def random_seed(seed):
    try:
        random.seed(seed, version=1)
    except:
        random.seed(seed)
    return

def convert(size):
    length = len(size)
    lastchar = size[length-1]
    if (lastchar == 'k') or (lastchar == 'K'):
        m = 1024
        nsize = int(size[0:length-1]) * m
    elif (lastchar == 'm') or (lastchar == 'M'):
        m = 1024*1024
        nsize = int(size[0:length-1]) * m
    elif (lastchar == 'g') or (lastchar == 'G'):
        m = 1024*1024*1024
        nsize = int(size[0:length-1]) * m
    else:
        nsize = int(size)
    return nsize


#
# main program
#
parser = OptionParser()
parser.add_option('-s', '--seed',      default=0,     help='随机种子',                                action='store', type='int', dest='seed')
parser.add_option('-a', '--asize',     default='1k',  help='地址空间大小（例如16、64k、32m、1g）',    action='store', type='string', dest='asize')
parser.add_option('-p', '--physmem',   default='16k', help='物理内存大小（例如16、64k、32m、1g）',  action='store', type='string', dest='psize')
parser.add_option('-n', '--addresses', default=5,     help='生成的虚拟地址数',        action='store', type='int', dest='num')
parser.add_option('-b', '--b',         default='-1',  help='基寄存器的值',                         action='store', type='string', dest='base')
parser.add_option('-l', '--l',         default='-1',  help='限度寄存器的值',                        action='store', type='string', dest='limit')
parser.add_option('-c', '--compute',   default=False, help='为我计算答案',                         action='store_true', dest='solve')


(options, args) = parser.parse_args()

print('')
print('ARG seed', options.seed)
print('ARG address space size', options.asize)
print('ARG phys mem size', options.psize)
print('')

random_seed(options.seed)
asize = convert(options.asize)
psize = convert(options.psize)

if psize <= 1:
    print('错误：必须指定非零物理内存大小。')
    exit(1)

if asize == 0:
    print('错误：必须指定非零地址空间大小。')
    exit(1)

if psize <= asize:
    print('错误：物理内存大小必须大于地址空间大小（在此模拟中）')
    exit(1)

#
# need to generate base, bounds for segment registers
#
limit = convert(options.limit)
base  = convert(options.base)

if limit == -1:
    limit = int(asize/4.0 + (asize/4.0 * random.random()))

# now have to find room for them
if base == -1:
    done = 0
    while done == 0:
        base = int(psize * random.random())
        if (base + limit) < psize:
            done = 1

print('基地址和界限寄存器信息：')
print('')
print('  基地址   : 0x%08x (十进制 %d)' % (base, base))
print('  界限  : %d' % (limit))
print('')

if base + limit > psize:
    print('错误：地址空间不适合该基/界限值的物理内存。')
    print('基地址 + 界限:', base + limit, '  物理内存:', psize)
    exit(1)

#
# now, need to generate virtual address trace
#
print('虚拟地址跟踪')
for i in range(0,options.num):
    vaddr = int(asize * random.random())
    if options.solve == False:
        print('  VA %2d: 0x%08x (十进制: %4d) --> PA或分段违规？' % (i, vaddr, vaddr))
    else:
        paddr = 0
        if (vaddr >= limit):
            print('  VA %2d: 0x%08x (十进制: %4d) --> 分段违规' % (i, vaddr, vaddr))
        else:
            paddr = vaddr + base
            print('  VA %2d: 0x%08x (十进制: %4d) --> 有效: 0x%08x (十进制: %4d)' % (i, vaddr, vaddr, paddr, paddr))

print('')

if options.solve == False:
    print('对于每个虚拟地址，要么写下它转换到的物理地址')
    print('或写下它是越界地址（分段违规）。对于')
    print('此问题，您应该假设一个给定大小的简单虚拟地址空间。')
    print('')





