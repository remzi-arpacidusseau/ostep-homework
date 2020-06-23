#! /usr/bin/env python

#
# lfs.py
#
# A simple simulator to emulate the behavior of LFS.
#
# Make lots of simplifying assumptions including things like:
# - all entities take up exactly one block
# - no segments or buffering of writes in memory
# - many other things
# 

from __future__ import print_function
import math
import sys
from optparse import OptionParser
import random
import copy

# to make Python2 and Python3 act the same -- how dumb
def random_seed(seed):
    try:
        random.seed(seed, version=1)
    except:
        random.seed(seed)
    return

# fixed addr
ADDR_CHECKPOINT_BLOCK = 0

# These are not (yet) things you can change
NUM_IMAP_PTRS_IN_CR       = 16
NUM_INODES_PER_IMAP_CHUNK = 16
NUM_INODE_PTRS            = 8

NUM_INODES = NUM_IMAP_PTRS_IN_CR * NUM_INODES_PER_IMAP_CHUNK

# block types
BLOCK_TYPE_CHECKPOINT     = 'type_cp'
BLOCK_TYPE_DATA_DIRECTORY = 'type_data_dir'
BLOCK_TYPE_DATA_BLOCK     = 'type_data'
BLOCK_TYPE_INODE          = 'type_inode'
BLOCK_TYPE_IMAP           = 'type_imap'

# inode types
INODE_DIRECTORY           = 'dir'
INODE_REGULAR             = 'reg'

# root inode is "well known" per Unix conventions
ROOT_INODE                = 0

# policies
ALLOCATE_SEQUENTIAL       = 1
ALLOCATE_RANDOM           = 2

#
# Heart of simulation is found here
#
class LFS:
    def __init__(self, use_disk_cr=False, no_force_checkpoints=False,
                 inode_policy=ALLOCATE_SEQUENTIAL, solve=False):
        # whether to read checkpoint region and imap pieces from disk (if True)
        # or instead just to use "in-memory" inode map instead
        self.use_disk_cr          = use_disk_cr

        # to force an update of the checkpoint region after each write
        self.no_force_checkpoints = no_force_checkpoints

        # inode allocation policy
        assert(inode_policy == ALLOCATE_SEQUENTIAL or inode_policy == ALLOCATE_RANDOM)
        self.inode_policy = inode_policy

        # whether to show "answers" to things or not
        self.solve                = solve

        # dump assistance
        self.dump_last            = 1
        
        # ALL blocks are in the "disk"
        self.disk = []

        # checkpoint region (first block)
        self.cr    = [3,-1,-1,-1,
                      -1,-1,-1,-1,
                      -1,-1,-1,-1,
                      -1,-1,-1,-1]
        assert(len(self.cr) == NUM_IMAP_PTRS_IN_CR)

        # create first checkpoint region
        self.log({'block_type':BLOCK_TYPE_CHECKPOINT, 'entries': self.cr})
        assert(len(self.disk) == 1)

        # init root dir data
        self.log(self.make_new_dirblock(ROOT_INODE, ROOT_INODE))
        assert(len(self.disk) == 2)

        # root inode
        root_inode = self.make_inode(itype=INODE_DIRECTORY, size=1, refs=2)
        root_inode['pointers'][0] = 1
        root_inode_address = self.log(root_inode)
        assert(len(self.disk) == 3)

        # init in memory imap
        self.inode_map = {}
        for i in range(NUM_INODES):
            self.inode_map[i] = -1
        self.inode_map[ROOT_INODE] = root_inode_address
        
        # imap piece
        self.log(self.make_imap_chunk(ROOT_INODE))
        assert(len(self.disk) == 4)

        # error code: tracking
        self.error_clear()
        return

    def make_data_block(self, data):
        return {'block_type':BLOCK_TYPE_DATA_BLOCK, 'contents':data}

    def make_inode(self, itype, size, refs):
        return {'block_type':BLOCK_TYPE_INODE, 'type':itype, 'size':size, 'refs':refs,
                'pointers':[-1,-1,-1,-1,-1,-1,-1,-1]}

    def make_new_dirblock(self, parent_inum, current_inum):
        dirblock = self.make_empty_dirblock()
        dirblock['entries'][0] = ('.', current_inum)
        dirblock['entries'][1] = ('..', parent_inum)
        return dirblock

    def make_empty_dirblock(self):
        return {'block_type':BLOCK_TYPE_DATA_DIRECTORY,
                'entries': [('-',-1), ('-',-1), ('-',-1), ('-',-1),
                            ('-',-1), ('-',-1), ('-',-1), ('-',-1)]}
    
    def make_imap_chunk(self, cnum):
        imap_chunk = {}
        imap_chunk['block_type'] = BLOCK_TYPE_IMAP
        imap_chunk['entries'] = list()
        start = cnum * NUM_INODES_PER_IMAP_CHUNK
        for i in range(start, start + NUM_INODES_PER_IMAP_CHUNK):
            imap_chunk['entries'].append(self.inode_map[i])
        return imap_chunk

    def make_random_blocks(self, num):
        contents = []
        for i in range(num):
            L = chr(ord('a') + int(random.random() * 26))
            contents.append(str(16 * ('%s%d' % (L, i))))
        return contents

    def inum_to_chunk(self, inum):
        return int(inum / NUM_INODES_PER_IMAP_CHUNK)

    def determine_liveness(self):
        # first, assume all are dead
        self.live = {}
        for i in range(len(self.disk)):
            self.live[i] = False

        # checkpoint region
        self.live[0] = True

        # now mark latest pieces of imap as live
        for ptr in self.cr:
            if ptr == -1:
                continue
            self.live[ptr] = True

        # go through imap, find live inodes and their addresses
        # latest inodes are all live, by def
        inodes = []
        for i in range(len(self.inode_map)):
            if self.inode_map[i] == -1:
                continue
            self.live[self.inode_map[i]] = True
            inodes.append(i)

        # go through live inodes and find blocks each points to
        for i in inodes:
            inode = self.disk[self.inode_map[i]]
            for ptr in inode['pointers']:
                self.live[ptr] = True
        return

    def error_log(self, s):
        self.error_list.append(s)
        return

    def error_clear(self):
        self.error_list = []
        return

    def error_dump(self):
        for i in self.error_list:
            print('  %s' % i)
        return

    def dump_partial(self, show_liveness, show_checkpoint):
        if show_checkpoint or not self.no_force_checkpoints:
            self.__dump(0, 1, show_liveness)
        if not self.no_force_checkpoints:
            print('...')
        self.__dump(self.dump_last, len(self.disk), show_liveness)
        self.dump_last = len(self.disk)
        return

    def dump(self, show_liveness):
        self.__dump(0, len(self.disk), show_liveness)
        return

    def __dump(self, start, end, show_liveness):
        self.determine_liveness()

        for i in range(start, end):
            # print ADDRESS on disk
            b = self.disk[i]
            block_type = b['block_type']
            print('[ %3d ]' % i, end='')

            # print LIVENESS
            if show_liveness or self.solve:
                if self.live[i]:
                    print(' live', end=' ')
                else:
                    print('     ', end=' ')
            else:
                print(' ?   ', end=' ')

            
            if block_type == BLOCK_TYPE_CHECKPOINT:
                print('checkpoint:', end=' ')
                for e in b['entries']:
                    if e != -1:
                        print(e,  end=' ')
                    else:
                        print('--', end=' ')
                print('')
            elif block_type == BLOCK_TYPE_DATA_DIRECTORY:
                for e in b['entries']:
                    if e[1] != -1:
                        print('[%s,%s]' % (str(e[0]), str(e[1])), end=' ')
                    else:
                        print('--', end=' ')
                print('')
            elif block_type == BLOCK_TYPE_DATA_BLOCK:
                print (b['contents'])
            elif block_type == BLOCK_TYPE_INODE:
                print('type:'+b['type'], 'size:'+str(b['size']), 'refs:'+str(b['refs']), 'ptrs:',  end=' ')
                for p in b['pointers']:
                    if p != -1:
                        print('%s' % p, end=' ')
                    else:
                        print('--', end=' ')
                print('')
            elif block_type == BLOCK_TYPE_IMAP:
                print('chunk(imap):', end=' ')
                for e in b['entries']:
                    if e != -1:
                        print(e, end=' ')
                    else:
                        print('--', end=' ')
                print('')
            else:
                print('error: unknown block_type', block_type)
                exit(1)
        return

    def log(self, block):
        new_address = len(self.disk)
        self.disk.append(copy.deepcopy(block))
        return new_address

    def allocate_inode(self):
        if self.inode_policy == ALLOCATE_SEQUENTIAL:
            for i in range(len(self.inode_map)):
                if self.inode_map[i] == -1:
                    # ugh: temporary holder until real on-disk location filled in
                    self.inode_map[i] = 1 
                    return i
        elif self.inode_policy == ALLOCATE_RANDOM:
            # inefficiently ensure that space exists
            # better done with counter of alloc/free but this is ok for now
            space_exists = False
            imap_len = len(self.inode_map)
            for i in range(imap_len):
                if self.inode_map[i] == -1:
                    space_exists = True
                    break
            if not space_exists:
                return -1
            while True:
                index = int(random.random() * imap_len)
                if self.inode_map[index] == -1:
                    self.inode_map[index] = 1
                    return index
        # no free inode found
        return -1
            

    def free_inode(self, inum):
        assert(self.inode_map[inum] != -1)
        self.inode_map[inum] = -1
        return

    def remap(self, inode_number, inode_address):
        self.inode_map[inode_number] = inode_address
        return

    def dump_inode_map(self):
        for i in range(len(self.inode_map)):
            if self.inode_map[i] != -1:
                print('  ', i, '->', self.inode_map[i])
        print('')
        return

    def cr_sync(self):
        # only place in code where an OVERWRITE occurs
        self.disk[ADDR_CHECKPOINT_BLOCK] = copy.deepcopy({'block_type':BLOCK_TYPE_CHECKPOINT, 'entries': self.cr})
        return 0

    def get_inode_from_inumber(self, inode_number):
        imap_entry_index = int(inode_number / NUM_INODES_PER_IMAP_CHUNK)
        imap_entry_offset = inode_number % NUM_INODES_PER_IMAP_CHUNK

        if self.use_disk_cr:
            # this is the disk path
            checkpoint_block = self.disk[ADDR_CHECKPOINT_BLOCK]
            assert(checkpoint_block['block_type'] == BLOCK_TYPE_CHECKPOINT)

            imap_block_address = checkpoint_block['entries'][imap_entry_index]
            imap_block = self.disk[imap_block_address]
            assert(imap_block['block_type'] == BLOCK_TYPE_IMAP)

            inode_address = imap_block['entries'][imap_entry_offset]
        else:
            # this is the just-use-the-mem-inode_map path
            inode_address = self.inode_map[inode_number]

        assert(inode_address != -1)
        inode = self.disk[inode_address]
        assert(inode['block_type'] == BLOCK_TYPE_INODE)
        return inode

    def __lookup(self, parent_inode_number, name):
        parent_inode = self.get_inode_from_inumber(parent_inode_number)
        assert(parent_inode['type'] == INODE_DIRECTORY)
        for address in parent_inode['pointers']:
            if address == -1:
                continue
            directory_block = self.disk[address]
            assert(directory_block['block_type'] == BLOCK_TYPE_DATA_DIRECTORY)
            for entry_name, entry_inode_number in directory_block['entries']:
                if entry_name == name:
                    return (entry_inode_number, parent_inode)
        return (-1, parent_inode)

    def __walk_path(self, path):
        split_path = path.split('/')
        if split_path[0] != '':
            self.error_log('path malformed: must start with /')
            return -1, '', -1, ''
        inode_number = -1 
        parent_inode_number = ROOT_INODE # root inode number is well known
        for i in range(1, len(split_path) - 1):
            inode_number, inode = self.__lookup(parent_inode_number, split_path[i])
            if inode_number == -1:
                self.error_log('directory %s not found' % split_path[i])
                return -1, '', -1, ''
            if inode['type'] != INODE_DIRECTORY:
                self.error_log('invalid element of path [%s] (not a dir)' % split_path[i])
                return -1, '', -1, ''
            parent_inode_number = inode_number

        file_name = split_path[len(split_path) - 1]
        inode_number, parent_inode = self.__lookup(parent_inode_number, file_name)
        return inode_number, file_name, parent_inode_number, parent_inode

    def update_imap(self, inum_list):
        chunk_list = list()
        for inum in inum_list:
            cnum = self.inum_to_chunk(inum)
            if cnum not in chunk_list:
                chunk_list.append(cnum)
                self.log(self.make_imap_chunk(cnum))
                self.cr[cnum] = len(self.disk) - 1
        return

    def __read_dirblock(self, inode, index):
        return self.disk[inode['pointers'][index]]        

    # return (inode_index, dirblock_index)
    def __find_matching_dir_slot(self, name, inode):
        for inode_index in range(inode['size']):
            directory_block = self.__read_dirblock(inode, inode_index)
            assert(directory_block['block_type'] == BLOCK_TYPE_DATA_DIRECTORY)

            for slot_index in range(len(directory_block['entries'])):
                entry_name, entry_inode_number = directory_block['entries'][slot_index]
                if entry_name == name:
                    return inode_index, slot_index
        return -1, -1

    def __add_dir_entry(self, parent_inode, file_name, inode_number):
        # this will be the directory block to contain the new name->inum mapping
        inode_index, dirblock_index = self.__find_matching_dir_slot('-', parent_inode)

        if inode_index != -1:
            # there is room in existing block: make copy, update it, and log it
            index_to_update = inode_index
            parent_size = parent_inode['size']

            new_directory_block = copy.deepcopy(self.__read_dirblock(parent_inode, inode_index))
            new_directory_block['entries'][dirblock_index] = (file_name, inode_number)
        else:
            # no room in existing directory block: allocate new one IF there is room in inode to point to it
            if parent_inode['size'] != NUM_INODE_PTRS:
                index_to_update = parent_inode['size']
                parent_size = index_to_update + 1

                new_directory_block = self.make_empty_dirblock()
                new_directory_block['entries'][0] = (file_name, inode_number)
            else:
                return -1, -1, {}
        return index_to_update, parent_size, new_directory_block

    # create (file OR dir)
    def __file_create(self, path, is_file):
        inode_number, file_name, parent_inode_number, parent_inode = self.__walk_path(path)
        if inode_number != -1:
            # self.error_log('create failed: file %s already exists' % path)
            self.error_log('create failed: file already exists')
            return -1

        if parent_inode_number == -1:
            self.error_log('create failed: walkpath returned error [%s]' % path)
            return -1

        # finally, allocate inode number for new file/dir
        new_inode_number = self.allocate_inode()
        if new_inode_number == -1:
            self.error_log('create failed: no more inodes available')
            return -1

        # this will be the directory block to contain the new name->inum mapping
        index_to_update, parent_size, new_directory_block = self.__add_dir_entry(parent_inode, file_name, new_inode_number)
        if index_to_update == -1:
            self.error_log('error: directory is full (path %s)' % path)
            self.free_inode(new_inode_number);
            return -1
        
        # log directory data block (either new version of old OR new one entirely)
        new_directory_block_address = self.log(new_directory_block)

        # now have to make new version of directory inode
        # update size (if needed), inc refs if this is a dir, point to new dir block addr
        new_parent_inode = copy.deepcopy(parent_inode)
        new_parent_inode['size'] = parent_size
        if not is_file:
            new_parent_inode['refs'] += 1
        new_parent_inode['pointers'][index_to_update] = new_directory_block_address

        # if directory, must create empty dir block
        if not is_file:
            self.log(self.make_new_dirblock(parent_inode_number, new_inode_number))
            new_dirblock_address = len(self.disk) - 1

        # and the new inode itself
        if is_file:
            # create empty file by default
            new_inode = self.make_inode(itype=INODE_REGULAR, size=0, refs=1)
        else:
            # create directory inode and point it to the one dirblock it owns
            new_inode = self.make_inode(itype=INODE_DIRECTORY, size=1, refs=2)
            new_inode['pointers'][0] = new_dirblock_address

        #
        # ADD updated parent inode, file/dir inode TO LOG
        #
        new_parent_inode_address = self.log(new_parent_inode)
        new_inode_address = self.log(new_inode)

        # and new imap entries for both parent and new inode
        self.remap(parent_inode_number, new_parent_inode_address)
        self.remap(new_inode_number, new_inode_address)

        # finally, create new chunk of imap
        self.update_imap([parent_inode_number, new_inode_number])

        # SYNC checkpoint region
        if not self.no_force_checkpoints:
            self.cr_sync()
        return 0

    # file_create()
    def file_create(self, path):
        self.error_clear()
        return self.__file_create(path, True)

    # dir_create()
    def dir_create(self, path):
        self.error_clear()
        return self.__file_create(path, False)

    # link()
    def file_link(self, srcpath, dstpath):
        self.error_clear()

        src_inode_number, src_file_name, src_parent_inode_number, src_parent_inode = self.__walk_path(srcpath)
        if src_inode_number == -1:
            self.error_log('link failed, src [%s] not found' % srcpath)
            return -1

        src_inode = self.get_inode_from_inumber(src_inode_number)
        if src_inode['type'] != INODE_REGULAR:
            self.error_log('link failed: cannot link to non-regular file [%s]' % srcpath)
            return -1

        dst_inode_number, dst_file_name, dst_parent_inode_number, dst_parent_inode = self.__walk_path(dstpath)
        if dst_inode_number != -1:
            self.error_log('link failed, dst [%s] exists' % dstpath)
            return -1

        # this will be the directory block to contain the new name->inum mapping
        dst_index_to_update, dst_parent_size, new_directory_block = self.__add_dir_entry(dst_parent_inode, dst_file_name, src_inode_number)
        if dst_index_to_update == -1:
            self.error_log('error: directory is full [path %s]' % dstpath)
            return -1
        
        # log directory data block (either new version of old OR new one entirely)
        new_directory_block_address = self.log(new_directory_block)

        # now have to make new version of directory inode
        # update size (if needed), inc refs if this is a dir, point to new dir block addr
        new_dst_parent_inode = copy.deepcopy(dst_parent_inode)
        new_dst_parent_inode['size'] = dst_parent_size
        new_dst_parent_inode['pointers'][dst_index_to_update] = new_directory_block_address

        # ADD updated parent inode TO LOG
        new_dst_parent_inode_address = self.log(new_dst_parent_inode)

        # inode must change too: to reflect NEW refs count
        new_src_inode = copy.deepcopy(src_inode)
        new_src_inode['refs'] += 1
        new_src_inode_address = self.log(new_src_inode)

        # and new imap entries for both parent and new inode
        self.remap(dst_parent_inode_number, new_dst_parent_inode_address)
        self.remap(src_inode_number, new_src_inode_address)

        # finally, create new chunk of imap
        self.update_imap([dst_parent_inode_number])

        # SYNC checkpoint region
        if not self.no_force_checkpoints:
            self.cr_sync()
        return 0
        
    def file_write(self, path, offset, num_blks):
        self.error_clear()

        # just make up contents of data blocks - up to the max spec'd by write
        # note: may not write all of these, because of running out of room in inode...
        contents = self.make_random_blocks(num_blks)

        inode_number, file_name, parent_inode_number, parent_inode = self.__walk_path(path)
        if inode_number == -1:
            self.error_log('write failed: file not found [path %s]' % path)
            return -1

        inode = self.get_inode_from_inumber(inode_number)
        if inode['type'] != INODE_REGULAR:
            self.error_log('write failed: cannot write to non-regular file %s' % path)
            return -1

        if offset < 0 or offset >= NUM_INODE_PTRS:
            self.error_log('write failed: bad offset %d' % offset)
            return -1

        # create potential write list -- up to max file size
        current_log_ptr = len(self.disk)
        current_offset = offset
        potential_writes = []
        while current_offset < NUM_INODE_PTRS and current_offset < offset + len(contents):
            potential_writes.append((current_offset, current_log_ptr))
            current_offset += 1
            current_log_ptr += 1

        # write data block(s)
        for i in range(len(potential_writes)):
            self.log(self.make_data_block(contents[i]))
            
        # write new version of inode, with updated size
        new_inode = copy.deepcopy(inode)
        new_inode['size'] = max(current_offset, inode['size'])
        for new_offset, new_addr in potential_writes:
            new_inode['pointers'][new_offset] = new_addr
        new_inode_address = self.log(new_inode)

        # write new chunk of imap
        self.remap(inode_number, new_inode_address)
        self.log(self.make_imap_chunk(self.inum_to_chunk(inode_number)))
        self.cr[self.inum_to_chunk(inode_number)] = len(self.disk) - 1

        # write checkpoint region
        if not self.no_force_checkpoints:
            self.cr_sync()

        # return size of write (total # written, not desired, may be less than asked for)
        return current_offset - offset

    def file_delete(self, path):
        self.error_clear()

        inode_number, file_name, parent_inode_number, parent_inode = self.__walk_path(path)
        if inode_number == -1:
            self.error_log('delete failed: file not found [%s]' % path)
            return -1

        inode = self.get_inode_from_inumber(inode_number)
        if inode['type'] != INODE_REGULAR:
            self.error_log('delete failed: cannot delete non-regular file [%s]' % path)
            return -1

        # have to check: is the file actually down to its last ref?
        if inode['refs'] == 1:
            self.free_inode(inode_number)

        # now, find entry in DIRECTORY DATA BLOCK and zero it
        inode_index, dirblock_index = self.__find_matching_dir_slot(file_name, parent_inode)
        assert(inode_index != -1)
        new_directory_block = copy.deepcopy(self.__read_dirblock(parent_inode, inode_index))
        new_directory_block['entries'][dirblock_index] = ('-', -1)

        # this leads to DIRECTORY DATA, DIR INODE, (and hence IMAP_CHUNK, CR_SYNC) writes
        dir_addr = self.log(new_directory_block)
        
        new_parent_inode = copy.deepcopy(parent_inode)
        new_parent_inode['pointers'][inode_index] = dir_addr
        new_parent_inode_addr = self.log(new_parent_inode)
        self.remap(parent_inode_number, new_parent_inode_addr)

        # if this ISNT the last link, decrease ref count and output new version
        if inode['refs'] > 1:
            new_inode = copy.deepcopy(inode)
            new_inode['refs'] -= 1
            new_inode_addr = self.log(new_inode)
            self.remap(inode_number, new_inode_addr)

        # create new chunk of imap
        self.update_imap([inode_number, parent_inode_number])
            
        # and sync if need be
        if not self.no_force_checkpoints:
            self.cr_sync()
        return 0

    def sync(self):
        self.error_clear()
        return self.cr_sync()

#
# HELPERs for main
#
def pick_random(a_list):
    if len(a_list) == 0:
        return ''
    index = int(random.random() * len(a_list))
    return a_list[index]

def make_random_file_name(parent_dir):
    L1 = chr(ord('a') + int(random.random() * 26))
    L2 = chr(ord('a') + int(random.random() * 26))
    N1 = str(int(random.random() * 10))
    if parent_dir == '/':
        return '/' + L1 + L2 + N1
    return parent_dir + '/' + L1 + L2 + N1

#
# must be in format: cXX,wXX,etc
# where first letter is command and XX is percent (from 0-100)
#
def process_percentages(percentages):
    tmp = percentages.split(',')
    csum = 0
    for p in tmp:
        cmd = p[0]
        value = int(p[1:])
        if value < 0:
            print('percentages must be positive or zero')
            exit(1)
        csum += int(value)
    if csum != 100:
        print('percentages do not add to 100')
        exit(1)

    p_array = {}

    cmd_list = ['c', 'w', 'd', 'r', 'l', 's']

    for c in cmd_list:
        p_array[c] = (0, 0)
    
    csum = 0
    for p in tmp:
        cmd = p[0]
        if cmd not in cmd_list:
            print('bad command', cmd)
            exit(1)
        value = int(p[1:])
        p_array[cmd] = (csum, csum + value)
        csum += value

    for i in p_array:
        p_array[i] = (p_array[i][0] / 100.0, p_array[i][1] / 100.0)

    return p_array

def make_command_list(num_commands, percent):
    command_list = ''
    existing_files = []
    existing_dirs = ['/']
    while num_commands > 0:
        chances = random.random()
        command = ''
        if chances >= percents['c'][0] and chances < percents['c'][1]:
            pdir = pick_random(existing_dirs)
            if pdir == '':
                continue
            nfile = make_random_file_name(pdir)
            command = 'c,%s' % nfile
            existing_files.append(nfile)
        elif chances >= percents['w'][0] and chances < percents['w'][1]:
            pfile = pick_random(existing_files)
            if pfile == '':
                continue
            woff = int(random.random() * 8)
            wlen = int(random.random() * 8)
            command = 'w,%s,%d,%d' % (pfile, woff, wlen)
        elif chances >= percents['d'][0] and chances < percents['d'][1]: 
            pdir = pick_random(existing_dirs)
            if pdir == '':
                continue
            ndir = make_random_file_name(pdir)
            command = 'd,%s' % ndir
            existing_dirs.append(ndir)
        elif chances >= percents['r'][0] and chances < percents['r'][1]:
            if len(existing_files) == 0:
                continue
            index = int(random.random() * len(existing_files))
            command = 'r,%s' % existing_files[index]
            del existing_files[index]
        elif chances >= percents['l'][0] and chances < percents['l'][1]:
            if len(existing_files) == 0:
                continue
            index = int(random.random() * len(existing_files))
            pdir = pick_random(existing_dirs)
            if pdir == '':
                continue
            nfile = make_random_file_name(pdir)
            command = 'l,%s,%s' % (existing_files[index], nfile)
            existing_files.append(nfile)
        elif chances >= percents['s'][0] and chances < percents['s'][1]:
            command = 's'
        else:
            print('abort: internal error with percent operations')
            exit(1)

        if command_list == '':
            command_list = command
        else:
            command_list += ':' + command

        num_commands -= 1
    return command_list

#
# MAIN program
#
parser = OptionParser()
parser.add_option('-s', '--seed', default=0, help='the random seed', action='store', type='int', dest='seed')
parser.add_option('-N', '--no_force', help='Do not force checkpoint writes after updates', default=False, action='store_true', dest='no_force_checkpoints')
parser.add_option('-F', '--no_final', help='Do not show the final state of the file system', default=False, action='store_true', dest='no_final')
parser.add_option('-D', '--use_disk_cr', help='use disk (maybe old) version of checkpoint region', default=False, action='store_true', dest='use_disk_cr')
parser.add_option('-c', '--compute', help='compute answers for me', action='store_true', default=False, dest='solve')
parser.add_option('-o', '--show_operations', help='print out operations as they occur', action='store_true', default=False, dest='show_operations')
parser.add_option('-i', '--show_intermediate', help='print out state changes as they occur', action='store_true', default=False, dest='show_intermediate')
parser.add_option('-e', '--show_return_codes', help='show error/return codes', action='store_true', default=False, dest='show_return_codes')
parser.add_option('-v', '--show_live_paths', help='show live paths', action='store_true', default=False, dest='show_live_paths')
parser.add_option('-n', '--num_commands', help='generate N random commands', action='store', default=3, dest='num_commands')
parser.add_option('-p', '--percentages', help='percent chance of: createfile,writefile,createdir,rmfile,linkfile,sync (example is c30,w30,d10,r20,l10,s0)', action='store', default='c30,w30,d10,r20,l10,s0', dest='percentages')
parser.add_option('-a', '--allocation_policy', help='inode allocation policy: "r" for "random" or "s" for "sequential"', action='store', default='s', dest='inode_policy')
parser.add_option('-L', '--command_list', default = '', action='store', type='str', dest='command_list', help='command list in format: "cmd1,arg1,...,argN:cmd2,arg1,...,argN:... where cmds are: c:createfile, d:createdir, r:delete, w:write, l:link, s:sync format: c,filepath d,dirpath r,filepath w,filepath,offset,numblks l,srcpath,dstpath s')

(options, args) = parser.parse_args()

random.seed(options.seed)

command_list = options.command_list
num_commands = int(options.num_commands)
percents = process_percentages(options.percentages)

if options.inode_policy == 's':
    inode_policy = ALLOCATE_SEQUENTIAL
elif options.inode_policy == 'r':
    inode_policy = ALLOCATE_RANDOM
else:
    print('bad policy', options.inode_policy)
    exit(1)

# where most of the work is done
L = LFS(use_disk_cr=options.use_disk_cr,
        no_force_checkpoints=options.no_force_checkpoints,
        inode_policy=inode_policy,
        solve=options.solve)

# what to show
print_operation = options.show_operations
print_intermediate = options.show_intermediate

# generate some random commands
if command_list == '':
    if num_commands < 0:
        print('num_commands must be greater than zero', num_commands)
        exit(1)
    command_list = make_command_list(num_commands, percents)
    

print('')
print('INITIAL file system contents:')
L.dump(True)
L.dump_last = 4 # ugly ... but needed to make intermediate dumps correct
print('')

#
# this variant allows control over each command
#
files_that_exist = []
dirs_that_exist = []

if command_list != '':
    commands = command_list.split(':')
    for i in range(len(commands)):
        command_and_args = commands[i].split(',')
        if command_and_args[0] == 'c':
            assert(len(command_and_args) == 2)
            if print_operation:
                print('create file', command_and_args[1], end=' ')
            rc = L.file_create(command_and_args[1])
            if rc == 0:
                files_that_exist.append(command_and_args[1])
        elif command_and_args[0] == 'd':
            assert(len(command_and_args) == 2)
            if print_operation:
                print('create dir ', command_and_args[1], end=' ')
            rc = L.dir_create(command_and_args[1])
            if rc == 0:
                dirs_that_exist.append(command_and_args[1])
        elif command_and_args[0] == 'r':
            assert(len(command_and_args) == 2)
            if print_operation:
                print('delete file', command_and_args[1], end=' ')
            rc = L.file_delete(command_and_args[1])
            if rc == 0:
                if command_and_args[1] in files_that_exist:
                    files_that_exist.remove(command_and_args[1])
                else:
                    print('warning: cannot find file', command_and_args[1])
        elif command_and_args[0] == 'l':
            assert(len(command_and_args) == 3)
            if print_operation:
                print('link file  ', command_and_args[1], command_and_args[2], end=' ')
            rc = L.file_link(command_and_args[1], command_and_args[2])
            if rc == 0:
                files_that_exist.append(command_and_args[2])
        elif command_and_args[0] == 'w':
            assert(len(command_and_args) == 4)
            if print_operation:
                print('write file  %s offset=%d size=%d' % (command_and_args[1], int(command_and_args[2]), int(command_and_args[3])), end=' ')
            rc = L.file_write(command_and_args[1], int(command_and_args[2]), int(command_and_args[3]))
        elif command_and_args[0] == 's':
            if print_operation:
                print('sync', end=' ')
            rc = L.sync()
        else:
            print('command not understood so skipping [%s]' % command_and_args[0])

        if not print_operation:
            print('command?', end=' ')

        if print_intermediate:
            print('')
            print('')
            if command_and_args[0] == 's':
                L.dump_partial(False, True)
            else:
                L.dump_partial(False, False)
            print('')

        if options.show_return_codes:
            print('->', rc)
            L.error_dump()
        else:
            print('')

        #if not print_intermediate:
        #    print('\nChanges to log, checkpoint region?')
        #    print('')
            

if not options.no_final:
    print('')
    print('FINAL file system contents:')
    L.dump(False)
    print('')
    if options.show_live_paths:
        print('Live directories: ', dirs_that_exist)
        print('Live files: ', files_that_exist)
        print('')
else:
    print('')
