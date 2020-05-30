#! /usr/bin/env python

from __future__ import print_function
from collections import *
from optparse import OptionParser
import random
import string

# to make Python2 and Python3 act the same -- how dumb
def random_seed(seed):
    try:
        random.seed(seed, version=1)
    except:
        random.seed(seed)
    return

def random_randint(low, hi):
    return int(low + random.random() * (hi - low + 1))

def random_choice(L):
    return L[random_randint(0, len(L)-1)]




class ssd:
    def __init__(self, ssd_type, num_logical_pages, num_blocks, pages_per_block,
                 block_erase_time, page_program_time, page_read_time,
                 high_water_mark, low_water_mark, trace_gc, show_state):
        # type
        self.TYPE_DIRECT = 1
        self.TYPE_LOGGING = 2
        self.TYPE_IDEAL = 3
        
        if ssd_type == 'direct':
            self.ssd_type = self.TYPE_DIRECT
        elif ssd_type == 'log':
            self.ssd_type = self.TYPE_LOGGING
        elif ssd_type == 'ideal':
            self.ssd_type = self.TYPE_IDEAL
        else:
            print('bad SSD type (%s)' % ssd_type)
            exit(1)
        
        # size
        self.num_logical_pages = num_logical_pages
        self.num_blocks = num_blocks
        self.pages_per_block = pages_per_block

        # parameters
        self.block_erase_time = block_erase_time
        self.page_program_time = page_program_time
        self.page_read_time = page_read_time

        # init each page of each block to INVALID
        self.STATE_INVALID = 1
        self.STATE_ERASED = 2
        self.STATE_VALID = 3
        
        self.num_pages = self.num_blocks * self.pages_per_block
        self.state = {}
        for i in range(self.num_pages):
            self.state[i] = self.STATE_INVALID

        # data itself
        self.data = {}
        for i in range(self.num_pages):
            self.data[i] = ' '

        # LOGGING stuff
        # reverse map: for each physical page, what LOGICAL page refers to it?
        # which page to write to right now?
        self.current_page = -1
        self.current_block = 0
        
        # gc counts
        self.gc_count = 0
        self.gc_current_block = 0
        self.gc_high_water_mark = high_water_mark
        self.gc_low_water_mark = low_water_mark
        
        self.gc_trace = trace_gc
        self.show_state = show_state

        # can use this as a log block
        self.gc_used_blocks = {}
        for i in range(self.num_blocks):
            self.gc_used_blocks[i] = 0

        # counts so as to help the GC
        self.live_count = {}
        for i in range(self.num_blocks):
            self.live_count[i] = 0

        # FTL
        self.forward_map = {}
        for i in range(self.num_logical_pages):
            self.forward_map[i] = -1

        self.reverse_map = {}
        for i in range(self.num_pages):
            self.reverse_map[i] = -1

        # stats
        self.physical_erase_count = {}
        self.physical_read_count = {}
        self.physical_write_count = {}

        for i in range(self.num_blocks):
            self.physical_erase_count[i] = 0
            self.physical_read_count[i] = 0
            self.physical_write_count[i] = 0

        self.physical_erase_sum = 0
        self.physical_write_sum = 0
        self.physical_read_sum = 0

        self.logical_trim_sum = 0
        self.logical_write_sum = 0
        self.logical_read_sum = 0

        self.logical_trim_fail_sum = 0
        self.logical_write_fail_sum = 0
        self.logical_read_fail_sum = 0
        return

    def blocks_in_use(self):
        used = 0
        for i in range(self.num_blocks):
            used += self.gc_used_blocks[i]
        return used

    def physical_erase(self, block_address):
        page_begin = block_address * self.pages_per_block
        page_end = page_begin + self.pages_per_block - 1
        
        for page in range(page_begin, page_end + 1):
            self.data[page] = ' '
            self.state[page] = self.STATE_ERASED

        # now, definitely NOT in use
        self.gc_used_blocks[block_address] = 0

        # STATS
        self.physical_erase_count[block_address] += 1
        self.physical_erase_sum += 1
        return

    def physical_program(self, page_address, data):
        self.data[page_address] = data
        self.state[page_address] = self.STATE_VALID
        # STATS
        self.physical_write_count[int(page_address / self.pages_per_block)] += 1
        self.physical_write_sum += 1
        return 

    def physical_read(self, page_address):
        # STATS
        self.physical_read_count[int(page_address / self.pages_per_block)] += 1
        self.physical_read_sum += 1
        return self.data[page_address]

    def read_direct(self, address):
        return self.physical_read(address)

    def write_direct(self, page_address, data):
        block_address = int(page_address / self.pages_per_block)
        page_begin = block_address * self.pages_per_block
        page_end = page_begin + self.pages_per_block - 1

        old_list = []
        for old_page in range(page_begin, page_end + 1):
            if self.state[old_page] == self.STATE_VALID:
                old_data = self.physical_read(old_page)
                old_list.append((old_page, old_data))

        self.physical_erase(block_address)
        for (old_page, old_data) in old_list:
            if old_page == page_address:
                continue
            self.physical_program(old_page, old_data)
            
        self.physical_program(page_address, data)
        self.forward_map[page_address] = page_address
        self.reverse_map[page_address] = page_address
        return 'success'

    def write_ideal(self, page_address, data):
        self.physical_program(page_address, data)
        self.forward_map[page_address] = page_address
        self.reverse_map[page_address] = page_address
        return 'success'

    def is_block_free(self, block):
        first_page = block * self.pages_per_block
        if self.state[first_page] == self.STATE_INVALID or self.state[first_page] == self.STATE_ERASED:
            if self.state[first_page] == self.STATE_INVALID:
                self.physical_erase(block)
            self.current_block = block
            self.current_page = first_page
            self.gc_used_blocks[block] = 1
            return True
        return False

    def get_cursor(self):
        if self.current_page == -1:
            for block in range(self.current_block, self.num_blocks):
                if self.is_block_free(block):
                    return 0
            for block in range(0, self.current_block):
                if self.is_block_free(block):
                    return 0
            return -1
        return 0

    def update_cursor(self):
        self.current_page += 1
        if self.current_page % self.pages_per_block == 0:
            self.current_page = -1
        return

    def write_logging(self, page_address, data, is_gc_write=False):
        if self.get_cursor() == -1:
            self.logical_write_fail_sum += 1
            return 'failure: device full'
        # NORMAL MODE writing
        assert(self.state[self.current_page] == self.STATE_ERASED)
        self.physical_program(self.current_page, data)
        self.forward_map[page_address] = self.current_page
        self.reverse_map[self.current_page] = page_address
        self.update_cursor()
        return 'success'

    def garbage_collect(self):
        blocks_cleaned = 0
        # for block in range(self.gc_current_block, self.num_blocks) + range(0, self.gc_current_block):
        # tricky flattening generator expression (https://stackoverflow.com/questions/18317913/how-can-i-combine-range-functions)
        for block in (x for y in (range(self.gc_current_block, self.num_blocks), range(0, self.gc_current_block)) for x in y):
            # don't GC the block currently being written to
            if block == self.current_block:
                continue

            # page to start looking for live blocks
            page_start = block * self.pages_per_block
            
            # is this page (and hence block) already erased? then don't bother
            if self.state[page_start] == self.STATE_ERASED:
                continue

            # collect list of live physical pages in this block
            live_pages = []
            for page in range(page_start, page_start + self.pages_per_block):
                logical_page = self.reverse_map[page]
                if logical_page != -1 and self.forward_map[logical_page] == page:
                    live_pages.append(page)

            # if ONLY live blocks, don't clean it! (why bother with move?)
            if len(live_pages) == self.pages_per_block:
                continue

            # live pages should be copied to current writing location
            for page in live_pages:
                # live: so copy it someplace new
                if self.gc_trace:
                    print('gc %d:: read(physical_page=%d)' % (self.gc_count, page))
                    print('gc %d:: write()' % self.gc_count)
                data = self.physical_read(page)
                self.write(self.reverse_map[page], data)

            # finally, erase the block and see if we're done
            blocks_cleaned += 1
            self.physical_erase(block)

            if self.gc_trace:
                print('gc %d:: erase(block=%d)' % (self.gc_count, block))
                if self.show_state:
                    print('')
                    self.dump()
                    print('')

            if self.blocks_in_use() <= self.gc_low_water_mark:
                # done! record where we stopped and return
                self.gc_current_block = block
                self.gc_count += 1
                return

        # END: block iteration
        return

    def upkeep(self):
        # GARBAGE COLLECTION
        if self.blocks_in_use() >= self.gc_high_water_mark:
            self.garbage_collect()
        # WEAR LEVELING: for future
        return

    def trim(self, address):
        self.logical_trim_sum += 1
        if address < 0 or address >= self.num_logical_pages:
            self.logical_trim_fail_sum += 1
            return 'fail: illegal trim address'
        if self.forward_map[address] == -1:
            self.logical_trim_fail_sum += 1
            return 'fail: uninitialized trim'
        self.forward_map[address] = -1
        return 'success'

    def read(self, address):
        self.logical_read_sum += 1
        if address < 0 or address >= self.num_logical_pages:
            self.logical_read_fail_sum += 1
            return 'fail: illegal read address'
        if self.forward_map[address] == -1:
            self.logical_read_fail_sum += 1
            return 'fail: uninitialized read'
        # USED for DIRECT and LOGGING and IDEAL
        return self.read_direct(self.forward_map[address])

    def write(self, address, data):
        self.logical_write_sum += 1
        if address < 0 or address >= self.num_logical_pages:
            self.logical_write_fail_sum += 1
            return 'fail: illegal write address'
        if self.ssd_type == self.TYPE_DIRECT:
            return self.write_direct(address, data)
        elif self.ssd_type == self.TYPE_IDEAL:
            return self.write_ideal(address, data)
        else:
            return self.write_logging(address, data)

    def printable_state(self, s):
        if s == self.STATE_INVALID:
            return 'i'
        elif s == self.STATE_ERASED:
            return 'E'
        elif s == self.STATE_VALID:
            return 'v'
        else:
            print('bad state %d' % s)
            exit(1)

    def stats(self):
        print('Physical Operations Per Block')
        print('Erases ', end='')
        for i in range(self.num_blocks):
            print('%3d        ' % self.physical_erase_count[i], end='')
        print('  Sum: %d' % self.physical_erase_sum)

        print('Writes ', end='')
        for i in range(self.num_blocks):
            print('%3d        ' % self.physical_write_count[i], end='')
        print('  Sum: %d' % self.physical_write_sum)

        print('Reads  ', end='')
        for i in range(self.num_blocks):
            print('%3d        ' % self.physical_read_count[i], end='')
        print('  Sum: %d' % self.physical_read_sum)
        print('')
        print('Logical Operation Sums')
        print('  Write count %d (%d failed)' % (self.logical_write_sum, self.logical_write_fail_sum))
        print('  Read count  %d (%d failed)' % (self.logical_read_sum, self.logical_read_fail_sum))
        print('  Trim count  %d (%d failed)' % (self.logical_trim_sum, self.logical_trim_fail_sum))
        print('')
        print('Times')
        print('  Erase time %.2f' % (self.physical_erase_sum * self.block_erase_time))
        print('  Write time %.2f' % (self.physical_write_sum * self.page_program_time))
        print('  Read time  %.2f' % (self.physical_read_sum * self.page_read_time))
        total_time = self.physical_erase_sum * self.block_erase_time + self.physical_write_sum * self.page_program_time + self.physical_read_sum * self.page_read_time
        print('  Total time %.2f' % total_time)
        return

    def dump(self):
        # FTL
        print('FTL   ', end='')
        count = 0
        ftl_columns = int((self.pages_per_block * self.num_blocks) / 7)
        for i in range(self.num_logical_pages):
            if self.forward_map[i] == -1:
                continue
            count += 1
            print('%3d:%3d ' % (i, self.forward_map[i]), end='')
            if count > 0 and count % ftl_columns == 0:
                print('\n      ', end='')
        if count == 0:
            print('(empty)', end='')
        print('')

        # FLASH?
        print('Block ', end='')
        for i in range(self.num_blocks):
            out_str = '%d' % i
            print(out_str + ' ' * (self.pages_per_block - len(out_str) + 1), end='')
        print('')

        max_len = len(str(self.num_pages))
        for n in range(max_len, 0, -1):
            if n == max_len:
                print('Page  ', end='')
            else:
                print('      ', end='')
            for i in range(self.num_pages):
                out_str = str(i).zfill(max_len)[max_len - n]
                print(out_str, end='')
                if i > 0 and (i+1) % 10 == 0:
                    print(end=' ')
            print('')

        print('State ', end='')
        for i in range(self.num_pages):
            print('%s' % self.printable_state(self.state[i]), end='')
            if i > 0 and (i+1) % 10 == 0:
                print(end=' ')
        print('')

        # DATA
        print('Data  ', end='')
        for i in range(self.num_pages):
            if self.state[i] == self.STATE_VALID:
                print('%s' % self.data[i], end='')
            else:
                print(' ', end='')
            if i > 0 and (i+1) % 10 == 0:
                print(end=' ')
        print('')

        # LIVE
        print('Live  ', end='')
        for i in range(self.num_pages):
            if self.state[i] == self.STATE_VALID and self.forward_map[self.reverse_map[i]] == i:
                print('+', end='')
            else:
                print(' ', end='')
            if i > 0 and (i+1) % 10 == 0:
                print(end=' ')
        print('')
        return




#
# MAIN PROGRAM
#
parser = OptionParser()
parser.add_option('-s', '--seed',            default=0,          help='the random seed',                         action='store', type='int',    dest='seed')
parser.add_option('-n', '--num_cmds',        default=10,         help='number of commands to randomly generate', action='store', type='int',    dest='num_cmds')
parser.add_option('-P', '--op_percentages',  default='40/50/10', help='if rand, percent of reads/writes/trims',  action='store', type='string', dest='op_percentages')
parser.add_option('-K', '--skew',            default='',         help='if non-empty, skew, e.g., 80/20: 80% of ops to 20% of blocks', action='store', type='string', dest='skew')
parser.add_option('-k', '--skew_start',      default=0,          help='if --skew, skew after this many writes',  action='store', type='int',    dest='skew_start')
parser.add_option('-r', '--read_fails',      default=0,          help='if rand, percent of reads that can fail', action='store', type='int',    dest='read_fail')
parser.add_option('-L', '--cmd_list',        default='',         help='comma-separated list of commands (e.g., r10,w20:a)', action='store', type='string', dest='cmd_list')
parser.add_option('-T', '--ssd_type',        default='direct',   help='SSD type: ideal, direct, log',            action='store', type='string', dest='ssd_type')
parser.add_option('-l', '--logical_pages',   default=50,         help='number of logical pages in interface',    action='store', type='int',    dest='num_logical_pages')
parser.add_option('-B', '--num_blocks',      default=7,          help='number of physical blocks in SSD',        action='store', type='int',    dest='num_blocks')
parser.add_option('-p', '--pages_per_block', default=10,         help='pages per physical block',                action='store', type='int',    dest='pages_per_block')
parser.add_option('-G', '--high_water_mark', default=10,         help='blocks used before gc trigger',           action='store', type='int',    dest='high_water_mark')
parser.add_option('-g', '--low_water_mark',  default=8,          help='gc target before stopping gc',            action='store', type='int',    dest='low_water_mark')
parser.add_option('-R', '--read_time',       default=10,         help='page read time (usecs)',                  action='store', type='int',    dest='read_time')
parser.add_option('-W', '--program_time',    default=40,         help='page program time (usecs)',               action='store', type='int',    dest='program_time')
parser.add_option('-E', '--erase_time',      default=1000,       help='page erase time (usecs)',                 action='store', type='int',    dest='erase_time')
parser.add_option('-J', '--show_gc',         default=False,      help='show garbage collector behavior',         action='store_true',           dest='show_gc')
parser.add_option('-F', '--show_state',      default=False,      help='show flash state',                        action='store_true',           dest='show_state')
parser.add_option('-C', '--show_cmds',       default=False,      help='show commands',                           action='store_true',           dest='show_cmds')
parser.add_option('-q', '--quiz_cmds',       default=False,      help='quiz commands',                           action='store_true',           dest='quiz_cmds')
parser.add_option('-S', '--show_stats',      default=False,      help='show statistics',                         action='store_true',           dest='show_stats')
parser.add_option('-c', '--compute',         default=False,      help='compute answers for me',                  action='store_true',           dest='solve')

(options, args) = parser.parse_args()

random_seed(options.seed)

print('ARG seed %s' % options.seed)
print('ARG num_cmds %s' % options.num_cmds)
print('ARG op_percentages %s' % options.op_percentages)
print('ARG skew %s' % options.skew)
print('ARG skew_start %s' % options.skew_start)
print('ARG read_fail %s' % options.read_fail)
print('ARG cmd_list %s' % options.cmd_list)
print('ARG ssd_type %s' % options.ssd_type)
print('ARG num_logical_pages %s' % options.num_logical_pages)
print('ARG num_blocks %s' % options.num_blocks)
print('ARG pages_per_block %s' % options.pages_per_block)
print('ARG high_water_mark %s' % options.high_water_mark)
print('ARG low_water_mark %s' % options.low_water_mark)
print('ARG erase_time %s' % options.erase_time)
print('ARG program_time %s' % options.program_time)
print('ARG read_time %s' % options.read_time)
print('ARG show_gc %s' % options.show_gc)
print('ARG show_state %s' % options.show_state)
print('ARG show_cmds %s' % options.show_cmds)
print('ARG quiz_cmds %s' % options.quiz_cmds)
print('ARG show_stats %s' % options.show_stats)
print('ARG compute %s' % options.solve)
print('')

s = ssd(ssd_type=options.ssd_type,
        num_logical_pages=options.num_logical_pages, num_blocks=options.num_blocks, pages_per_block=options.pages_per_block,
        block_erase_time=float(options.erase_time), page_program_time=float(options.program_time), page_read_time=float(options.read_time),
        high_water_mark=options.high_water_mark, low_water_mark=options.low_water_mark, trace_gc=options.show_gc, show_state=options.show_state)

#
# generate cmds (if not passed in by cmd_list)
#
hot_cold = False
skew_start = options.skew_start
if options.skew != '':
    hot_cold = True
    skew = options.skew.split('/')
    if len(skew) != 2:
        print('bad skew specification; should be 80/20 or something like that')
        exit(1)
    hot_percent = int(skew[0])/100.0
    hot_target = int(skew[1])/100.0

if options.cmd_list == '':
    max_page_addr = int(options.num_logical_pages)
    
    num_cmds = int(options.num_cmds)
    p = options.op_percentages.split('/')
    assert(len(p) == 3)
    percent_reads, percent_writes, percent_trims = int(p[0]), int(p[1]), int(p[2])
    if percent_writes <= 0:
        print('must have some writes, otherwise nothing in the SSD!')
        exit(1)
    
    printable = string.digits + string.ascii_lowercase + string.ascii_uppercase

    cmd_list = []
    valid_addresses = []
    while len(cmd_list) < num_cmds:
        which_cmd = int(random.random() * 100.0)
        if which_cmd < percent_reads:
            # READ
            if random_randint(0, 99) < int(options.read_fail):
                address = random_randint(0, max_page_addr - 1)
            else:
                if len(valid_addresses) < 2:
                    continue
                address = random_choice(valid_addresses)
            cmd_list.append('r%d' % address)
        elif which_cmd < percent_reads + percent_writes:
            # WRITE
            if skew_start == 0 and hot_cold and random.random() < hot_percent:
                address = random_randint(0, int(hot_target * (max_page_addr - 1)))
            else:
                address = random_randint(0, max_page_addr - 1)
            if address not in valid_addresses:
                valid_addresses.append(address)
            data = random_choice(list(printable))
            cmd_list.append('w%d:%s' % (address, data))
            if skew_start > 0:
                skew_start -= 1
        else:
            # TRIM
            if len(valid_addresses) < 1:
                continue
            address = random_choice(valid_addresses)
            cmd_list.append('t%d' % address)
            valid_addresses.remove(address)
        
else:
    cmd_list = options.cmd_list.split(',')

s.dump()
print('')

show_state = options.show_state
show_cmds = options.show_cmds
quiz_cmds = options.quiz_cmds

if quiz_cmds:
    show_state = True

op = 0
for cmd in cmd_list:
    if cmd == '':
        break
    if cmd[0] == 'r':
        # r10
        address = int(cmd.split('r')[1])
        data = s.read(address)
        if show_cmds or (quiz_cmds and options.solve):
            print('cmd %3d:: read(%d) -> %s' % (op, address, data))
        elif quiz_cmds:
            print('cmd %3d:: read(%d) -> ??' % (op, address))
        op += 1
    elif cmd[0] == 'w':
        # w80:b
        parts = cmd.split(':')
        address = int(parts[0].split('w')[1])
        data = parts[1]
        rc = s.write(address, data)
        if show_cmds or (quiz_cmds and options.solve):
            print('cmd %3d:: write(%d, %s) -> %s' % (op, address, data, rc))
        elif quiz_cmds:
            print('cmd %3d:: command(??) -> ??' % op)
        op += 1
    elif cmd[0] == 't':
        address = int(cmd.split('t')[1])
        rc = s.trim(address)
        if show_cmds or (quiz_cmds and options.solve):
            print('cmd %3d:: trim(%d) -> %s' % (op, address, rc))
        elif quiz_cmds:
            print('cmd %d:: command(??) -> ??' % op)
        op += 1

    if show_state:
        print('')
        s.dump()
        print('')

    # Do GC?
    s.upkeep()

if not show_state:
    print('')
    s.dump()
print('')
if options.show_stats:
    s.stats()
    print('')

