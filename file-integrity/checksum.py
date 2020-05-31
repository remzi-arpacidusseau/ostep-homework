#! /usr/bin/env python

from __future__ import print_function
import random
from optparse import OptionParser

# to make Python2 and Python3 act the same -- how dumb
def random_seed(seed):
    try:
        random.seed(seed, version=1)
    except:
        random.seed(seed)
    return

def print_hex(v):
    if v < 16:
        return '0x0%x' % v
    else:
        return '0x%x' % v
    
def print_bin(word):
    v = bin(word)
    o = '0b'
    o += ('0' * (10 - len(str(v))))
    o += str(v)[2:]
    return o
    

parser = OptionParser()
parser.add_option('-s', '--seed', default='0', help='Random seed', action='store', type='int', dest='seed')
parser.add_option('-d', '--data_size', default='4', help='Number of bytes in data word', action='store', type='int', dest='data_size')
parser.add_option('-D', '--data', default='', help='Data in comma separated form', action='store', type='string', dest='data')
parser.add_option('-c', '--compute', help='compute answers for me', action='store_true', default=False, dest='solve')
(options, args) = parser.parse_args()

print('')
print('OPTIONS seed', options.seed)
print('OPTIONS data_size', options.data_size)
print('OPTIONS data', options.data)
print('')

random_seed(options.seed)

values = []
if options.data != '':
    tmp = options.data.split(',')
    for t in tmp:
        values.append(int(t))
else:
    for t in range(int(options.data_size)):
        values.append(int(random.random() * 256))


add = 0
xor = 0
fletcher_a, fletcher_b = 0, 0

for value in values:
    add = (add + value) % 256
    xor = xor ^ value
    fletcher_a = (fletcher_a + value) % 255
    fletcher_b = (fletcher_b + fletcher_a) % 255

print('Decimal:  ', end=' ')
for word in values:
    print('%10s' % str(word), end=' ')
print('')

print('Hex:      ', end=' ')
for word in values:
    print('     ', print_hex(word), end=' ')
print('')

print('Bin:      ', end=' ')
for word in values:
    print(print_bin(word), end=' ')
print('')

print('')
if options.solve:
    print('Add:           ', '%3d      ' % add, '(%s)' % print_bin(add))
    print('Xor:           ', '%3d      ' % xor, '(%s)' % print_bin(xor))
    print('Fletcher(a,b): ', '%3d,%3d  ' % (fletcher_a, fletcher_b), '(%s,%s)' % (print_bin(fletcher_a), print_bin(fletcher_b)))
else:
    print('Add:      ?')
    print('Xor:      ?')
    print('Fletcher: ?')
print('')
    


