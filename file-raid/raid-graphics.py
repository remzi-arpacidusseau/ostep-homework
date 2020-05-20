#! /usr/bin/env python

from Tkinter import *
from types import *
import math, random, time, sys, os
from optparse import OptionParser

# states that a request/disk go through
STATE_NULL   = 0
STATE_SEEK   = 1
STATE_XFER   = 2
STATE_DONE   = 3

# request states
REQ_NOT_STARTED = 0
REQ_DO_READ = 1
REQ_DO_WRITE = 2
# used by parity requests
REQ_PARITY_READ_PHASE_DONE = 4
REQ_PARITY_WRITE_PHASE_BEGIN = 5
# all requests end in DONE state
REQ_DONE = 10

# whether req is read or write
OP_READ = 1
OP_WRITE = 2

class Request:
    def __init__(self, logical_address, op_type):
        self.logical_address = logical_address
        assert(op_type == OP_WRITE or op_type == OP_READ)
        self.op_type = op_type
        self.disk_to_index_map = {}
        self.full_stripe_write = False
        self.full_stripe_write_parity = False
        self.start_time = -1
        return

    def MarkFullStripeWrite(self, parity=False):
        self.full_stripe_write = True
        self.full_stripe_write_parity = parity
        return

    def FullStripeWriteStatus(self):
        return (self.full_stripe_write, self.full_stripe_write_parity)

    def GetType(self):
        return self.op_type

    def GetLogicalAddress(self):
        return self.logical_address

    def GetStatus(self, index):
        return self.status[index]

    def GetStatusByDisk(self, disk):
        index = self.disk_to_index_map[disk]
        return self.status[index]

    def SetStatus(self, index, status):
        # print 'STATUS', self.phys_disk_list[index], self.PrintableStatus(status)
        self.status[index] = status

    def SetPhysicalAddress(self, disk_list, offset):
        self.phys_disk_list = disk_list
        cnt = 0
        for disk in self.phys_disk_list:
            self.disk_to_index_map[disk] = cnt
            cnt += 1
        self.phys_offset = offset
        self.status = []
        for disk in self.phys_disk_list:
            self.status.append(REQ_NOT_STARTED)
        return

    def PrintableStatus(self, status):
        if status == REQ_NOT_STARTED:
            return 'REQ_NOT_STARTED'
        if status == REQ_DO_WRITE:
            return 'REQ_DO_WRITE'
        if status == REQ_DO_READ:
            return 'REQ_DO_READ'
        if status == REQ_DONE:
            return 'REQ_DONE'
        if status == REQ_PARITY_READ_PHASE_DONE:
            return 'REQ_PARITY_READ_PHASE_DONE'
        if status == REQ_PARITY_WRITE_PHASE_BEGIN:
            return 'REQ_PARITY_WRITE_PHASE_BEGIN'
        print 'BAD STATUS', status
        exit(1)
        return

    def MarkStart(self, timer):
        if self.start_time == -1:
            self.start_time = timer
        return

    def RequestLevel0Done(self, disk, timer):
        index = self.disk_to_index_map[disk]
        if self.status[index] == REQ_DO_READ or self.status[index] == REQ_DO_WRITE:
            self.status[index] = REQ_DONE
        return (True, timer - self.start_time)

    def RequestLevel1Done(self, disk, timer):
        index = self.disk_to_index_map[disk]
        if self.status[index] == REQ_DO_READ:
            self.status[index] = REQ_DONE
            return (True, timer - self.start_time)
        # this is for WRITES (only done when BOTH writes are done)
        assert(self.status[index] == REQ_DO_WRITE)
        self.status[index] = REQ_DONE
        if self.status[1-index] == REQ_DONE:
            return (True, timer - self.start_time)
        return (False, -1)

    # this is for RAID4 right now
    def RequestLevel4Done(self, disk, timer):
        index = self.disk_to_index_map[disk]
        # print 'Done', self.PrintableStatus(self.status[index])
        if self.op_type == OP_READ:
            return (True, timer - self.start_time)
        # this is for WRITES (which have two phases)
        if self.status[index] == REQ_DO_READ:
            self.status[index] = REQ_PARITY_READ_PHASE_DONE
        elif self.status[index] == REQ_DO_WRITE:
            self.status[index] = REQ_DONE
        if self.status[index] == REQ_PARITY_READ_PHASE_DONE and self.status[1-index] == REQ_PARITY_READ_PHASE_DONE:
            self.status[0] = REQ_PARITY_WRITE_PHASE_BEGIN
            self.status[1] = REQ_PARITY_WRITE_PHASE_BEGIN
        if self.status[index] == REQ_DONE and self.status[1-index] == REQ_DONE:
            return (True, timer - self.start_time)
        return (False, -1)

    def GetPhysicalOffset(self):
        return self.phys_offset

    def GetPhysicalDiskList(self):
        return self.phys_disk_list


class Raid:
    def __init__(self, mapping, addr_desc, addr, disk_count, seek_speed, seed, balance, read_fraction, window, animate_delay):
        self.mapping = mapping
        self.disk_count = disk_count
        self.seek_speed = seek_speed
        self.addr_desc = addr_desc
        self.balance = balance
        self.addr = addr
        self.read_fraction = read_fraction
        self.window = window
        self.animate_delay = animate_delay

        random.seed(seed)
        
        self.root = Tk()
        self.canvas = Canvas(self.root, width=560, height=530)
        self.canvas.pack()

        # make the disks
        disk_width = 100
        self.head_width = 10
        self.head_height = 20

        # now distribute blocks - assume striping first
        self.block_offset = {}

        # maps for scheduling
        self.offset_to_ypos = {}

        # maps for coloring blocks of the "disk"
        self.disk_and_offset_to_rect_id = {}

        self.color_map = {}

        if self.mapping == 0:
            # CREATE STRIPED CONFIGURATION
            self.block_count = 80
            for i in range(self.block_count):
                disk = i % self.disk_count
                offset = i / self.disk_count
                rect_x = 40 + ((20 + disk_width) * disk)
                rect_y = (20 * offset) + 100
                self.color_map[(disk, offset)] = 'gray'
                rect_id = self.canvas.create_rectangle(rect_x, rect_y, rect_x+disk_width, rect_y+20, fill='gray', outline='black')
                text_id = self.canvas.create_text(rect_x + disk_width - disk_width/2.0, rect_y+10, text='%s' % i, anchor='c')
                self.block_offset[i] = rect_y
                self.offset_to_ypos[offset] = rect_y
                self.disk_and_offset_to_rect_id[(disk, offset)] = rect_id

        elif self.mapping == 1:
            # CREATE MIRRORED CONFIGURATION
            self.block_count = 40
            effective_disks = self.disk_count / 2
            assert(self.disk_count % 2 == 0)
            for i in range(self.block_count):
                INDEX = i % effective_disks
                disk_1 = INDEX * 2
                disk_2 = disk_1 + 1
                offset = i / effective_disks
                rect_y = (20 * offset) + 100

                rect_x = 40 + ((20 + disk_width) * disk_1)
                self.color_map[(disk_1, offset)] = 'gray'
                rect_id_1 = self.canvas.create_rectangle(rect_x, rect_y, rect_x+disk_width, rect_y+20, fill='gray', outline='black')
                text_id_1 = self.canvas.create_text(rect_x + disk_width - disk_width/2.0, rect_y+10, text='%s' % i, anchor='c')

                rect_x = 40 + ((20 + disk_width) * disk_2)
                self.color_map[(disk_2, offset)] = 'gray'
                rect_id_2 = self.canvas.create_rectangle(rect_x, rect_y, rect_x+disk_width, rect_y+20, fill='gray', outline='black')
                text_id_2 = self.canvas.create_text(rect_x + disk_width - disk_width/2.0, rect_y+10, text='%s' % i, anchor='c')

                self.block_offset[i] = rect_y
                self.offset_to_ypos[offset] = rect_y
                self.disk_and_offset_to_rect_id[(disk_1, offset)] = rect_id_1
                self.disk_and_offset_to_rect_id[(disk_2, offset)] = rect_id_2

        elif self.mapping == 4:
            # CREATE SIMPLE PARITY CONFIGURATION
            self.block_count_full = 80
            self.block_count = 60
            for i in range(self.block_count):
                disk = i % (self.disk_count-1)
                offset = i / (self.disk_count-1)
                rect_x = 40 + ((20 + disk_width) * disk)
                rect_y = (20 * offset) + 100
                self.color_map[(disk, offset)] = 'lightgray'
                rect_id = self.canvas.create_rectangle(rect_x, rect_y, rect_x+disk_width, rect_y+20, fill='lightgray', outline='black')
                text_id = self.canvas.create_text(rect_x + disk_width - disk_width/2.0, rect_y+10, text='%s' % i, anchor='c')
                self.block_offset[i] = rect_y
                self.offset_to_ypos[offset] = rect_y
                self.disk_and_offset_to_rect_id[(disk, offset)] = rect_id

            # now make parity blocks
            for i in range(self.block_count_full/self.disk_count):
                disk = 3
                offset = i
                rect_x = 40 + ((20 + disk_width) * disk)
                rect_y = (20 * offset) + 100
                self.color_map[(disk, offset)] = 'darkgray'
                rect_id = self.canvas.create_rectangle(rect_x, rect_y, rect_x+disk_width, rect_y+20, fill='darkgray', outline='black')
                text_id = self.canvas.create_text(rect_x + disk_width - disk_width/2.0, rect_y+10, text='P%s' % i, anchor='c')
                self.block_offset['p' + str(i)] = rect_y
                self.offset_to_ypos[offset] = rect_y
                self.disk_and_offset_to_rect_id[(disk, offset)] = rect_id
            
        elif self.mapping == 5:
            # CREATE RAID-5 config
            self.block_count_full = 80
            self.block_count = 60
            for i in range(self.block_count):
                offset = i / (self.disk_count-1)
                if offset % 4 == 0:
                    disk = i % (self.disk_count-1)
                elif offset % 4 == 1:
                    disk = i % (self.disk_count-1)
                    if disk >= 2:
                        disk += 1
                elif offset % 4 == 2:
                    disk = i % (self.disk_count-1)
                    if disk >= 1:
                        disk += 1
                elif offset % 4 == 3:
                    disk = i % (self.disk_count-1)
                    disk += 1
                rect_x = 40 + ((20 + disk_width) * disk)
                rect_y = (20 * offset) + 100
                self.color_map[(disk, offset)] = 'gray'
                rect_id = self.canvas.create_rectangle(rect_x, rect_y, rect_x+disk_width, rect_y+20, fill='gray', outline='black')
                text_id = self.canvas.create_text(rect_x + disk_width - disk_width/2.0, rect_y+10, text='%s' % i, anchor='c')
                self.block_offset[i] = rect_y
                self.offset_to_ypos[offset] = rect_y
                self.disk_and_offset_to_rect_id[(disk, offset)] = rect_id

            # now make parity blocks
            for i in range(self.block_count_full/self.disk_count):
                offset = i
                if offset % 4 == 0:
                    disk = 3
                elif offset % 4 == 1:
                    disk = 2
                elif offset % 4 == 2:
                    disk = 1
                elif offset % 4 == 3:
                    disk = 0
                rect_x = 40 + ((20 + disk_width) * disk)
                rect_y = (20 * offset) + 100
                self.color_map[(disk, offset)] = 'darkgray'
                rect_id = self.canvas.create_rectangle(rect_x, rect_y, rect_x+disk_width, rect_y+20, fill='darkgray', outline='black')
                text_id = self.canvas.create_text(rect_x + disk_width - disk_width/2.0, rect_y+10, text='P%s' % i, anchor='c')
                self.block_offset['p' + str(i)] = rect_y
                self.offset_to_ypos[offset] = rect_y
                self.disk_and_offset_to_rect_id[(disk, offset)] = rect_id
            
        else:
            print 'mapping', self.mapping, 'not supported'
            exit(1)

        # now draw "disk heads"
        self.head_ids = {}
        self.head_position = {}
        self.disk_state = {}
        for disk in range(self.disk_count):
            rect_x = 40 - self.head_width + ((20 + disk_width) * disk)
            rect_y = 100
            head_id = self.canvas.create_rectangle(rect_x, rect_y,
                                                   rect_x+self.head_width, rect_y+self.head_height,
                                                   fill='black', outline='black')
            self.head_ids[disk] = head_id
            self.head_position[disk] = {'x1':rect_x, 'y1':rect_y, 'x2':rect_x+self.head_width, 'y2':rect_y+self.head_height}
            self.disk_state[disk] = STATE_NULL

        # seek targets
        self.last_target = {}
        self.current_target = {}
        self.current_optype = {}
        self.seek_delta = {}
        for disk in range(self.disk_count):
            self.last_target[disk] = -1
            self.current_target[disk] = -1
            self.current_optype[disk] = -1
            self.seek_delta[disk] = 0

        self.transfer_count = {}
        self.rotate_count = {}
        for disk in range(self.disk_count):
            self.transfer_count[disk] = -1
            self.rotate_count[disk] = -1

        # initial requests
        self.request_queue = {}
        self.request_count = 0

        effective_disk_count = 4
        if self.mapping == 4:
            effective_disk_count = 3
        
        if self.addr == '':
            # use 'addr_desc' (num to generate, max, min) to generate these
            tmp = self.addr_desc.split(',')
            num = int(tmp[0])
            req_max = int(tmp[1])
            if req_max == -1:
                req_max = self.block_count
            req_min = int(tmp[2])
            if self.balance:
                disk_min = num / effective_disk_count
            if req_min >= req_max:
                print 'bad addr_desc: min should be lower than max', req_min, req_max
                exit(1)
            target_disk = 0
            for i in range(num):
                while True:
                    req = int(random.random() * req_max)
                    if req % effective_disk_count != target_disk:
                        continue
                    target_disk += 1
                    if target_disk == effective_disk_count:
                        target_disk = 0
                    # print target_disk
                    if req >= req_min:
                        if random.random() < read_fraction:
                            self.request_queue[i] = Request(req, OP_READ)
                        else:
                            self.request_queue[i] = Request(req, OP_WRITE)
                        break
        else:
            # HAND-PASSED IN addresses
            # argument: comma-separated list of numbers
            tmp = self.addr.split(',')
            for i in range(len(tmp)):
                if tmp[i][0] == 'r':
                    self.request_queue[i] = Request(int(tmp[i].replace('r','')), OP_READ)
                elif tmp[i][0] == 'w':
                    self.request_queue[i] = Request(int(tmp[i].replace('w','')), OP_WRITE)
                else:
                    print 'Must specify reads vs writes, e.g., r10 or w6'
                    exit(1)

        self.request_count_needed = len(self.request_queue)

        # fill in extra info about requests
        if self.mapping == 0:
            # STRIPING
            for i in range(len(self.request_queue)):
                request = self.request_queue[i]
                logical = request.GetLogicalAddress()
                assert(logical < self.block_count)
                disk = logical % self.disk_count
                offset = logical / self.disk_count
                request.SetPhysicalAddress([disk], offset)
        elif self.mapping == 1:
            # MIRRORING
            for i in range(len(self.request_queue)):
                request = self.request_queue[i]
                if request.GetType() == OP_WRITE:
                    self.request_count_needed += 1
                effective_disks = self.disk_count / 2
                logical = request.GetLogicalAddress()
                assert(logical < self.block_count)
                disk_1 = 2 * (logical % effective_disks)
                disk_2 = disk_1 + 1
                offset = logical / effective_disks
                request.SetPhysicalAddress([disk_1, disk_2], offset)
        elif self.mapping == 4:
            # RAID-4 (PARITY DISK)
            for i in range(len(self.request_queue)):
                request = self.request_queue[i]
                if request.GetType() == OP_WRITE:
                    self.request_count_needed += 3
                logical = request.GetLogicalAddress()
                assert(logical < self.block_count)
                disk = logical % (self.disk_count-1)
                offset = logical / (self.disk_count-1)
                request.SetPhysicalAddress([disk, 3], offset)

            # XXX This really only works for SOME demos
            # (it is not a general purpose feature)
            for i in range(0,len(self.request_queue),3):
                if i+2 >= len(self.request_queue):
                    continue
                logical = self.request_queue[i].GetLogicalAddress()
                if self.request_queue[i+1].GetLogicalAddress() == logical + 1:
                    if self.request_queue[i+2].GetLogicalAddress() == logical + 2:
                        # full stripe detected: now mark and handle differently when scheduling
                        for j in range(i, i+2):
                            self.request_queue[j].MarkFullStripeWrite()
                        self.request_queue[i+2].MarkFullStripeWrite(True)
                        self.request_count_needed -= 8

        elif self.mapping == 5:
            # RAID-5 (ROTATED PARITY)
            for i in range(len(self.request_queue)):
                request = self.request_queue[i]
                if request.GetType() == OP_WRITE:
                    self.request_count_needed += 3
                logical = request.GetLogicalAddress()
                assert(logical < self.block_count)
                disk = logical % (self.disk_count-1)
                offset = logical / (self.disk_count-1)
                if offset % 4 == 0:
                    parity_disk = 3
                elif offset % 4 == 1:
                    parity_disk = 2
                    if disk >= 2:
                        disk += 1
                elif offset % 4 == 2:
                    parity_disk = 1
                    if disk >= 1:
                        disk += 1
                elif offset % 4 == 3:
                    parity_disk = 0
                    disk += 1

                # print 'LOGICAL', logical, 'offset', offset, 'disk', disk, 'paritydisk', parity_disk
                request.SetPhysicalAddress([disk, parity_disk], offset)


        # draw request queue
        self.request_queue_box_ids = []
        self.request_queue_text_ids = []
        self.request_queue_count_ids = []
        self.request_queue_counts = []

        x_start = 40
        x = x_start
        y = 32
        sz = 10

        font = ('Helvetica', sz+4)
        font_small = ('Helvetica', 8)

        for index in range(len(self.request_queue)):
            if x > 500:
                x = x_start
                y += (2*sz) + 2

            request = self.request_queue[index]
            logical = request.GetLogicalAddress()
            self.request_queue_box_ids.append(self.canvas.create_rectangle(x-sz,y-sz,x+sz,y+sz,fill='white',outline=''))
            self.request_queue_text_ids.append(self.canvas.create_text(x, y, text=str(logical), anchor='c', font=font))
            self.request_queue_count_ids.append(self.canvas.create_text(x+8, y+8, text=str(0), anchor='c', font=font_small))
            self.request_queue_counts.append(0)
                
            x += (2*sz) 
            
        # BINDINGS
        self.root.bind('s', self.Start)
        self.root.bind('p', self.Pause)
        self.root.bind('q', self.Exit)

        # draw current limits of queue
        self.windowID = -1
        self.DrawWindow()

        # TIME INFO and other stats
        self.timeID = self.canvas.create_text(10, 10, text='Time: 0.00', anchor='w')
        self.timer = 0

        self.logical_requests = 0
        self.latency_total = 0

        # read/write counts
        self.count_reads = {}
        self.count_writes = {}
        self.count_reads_id = {}
        self.count_writes_id = {}
        x = disk_width - 10
        font = ('Helvetica', 14)
        for i in range(self.disk_count):
            self.count_reads[i] = 0
            self.count_writes[i] = 0
            self.canvas.create_rectangle(x-50,510,x,530, fill='orange', outline='')
            self.canvas.create_rectangle(x+50,510,x,530, fill='yellow', outline='')
            self.count_reads_id[i] = self.canvas.create_text(x-20, 520, text='R:0', anchor='c', font=font)
            self.count_writes_id[i] = self.canvas.create_text(x+20, 520, text='W:0', anchor='c', font=font)
            x += disk_width + 20
        

        # set up animation loop
        self.do_animate = True
        self.is_done = False
        return

    # call this to start simulation
    def Go(self):
        self.root.mainloop()
        return

    #
    # BUTTONS
    #
    def Start(self, event):
        self.GetNextIOs()
        self.Animate()
        return

    def Pause(self, event):
        if self.do_animate == False:
            self.do_animate = True
        else:
            self.do_animate = False
        return

    def Exit(self, event):
        sys.exit(0)
        return

    #
    # ROUTINES
    #
    def UpdateWriteCounter(self, disk, how_much):
        self.count_writes[disk] += how_much
        self.canvas.itemconfig(self.count_writes_id[disk], text='W:%d' % self.count_writes[disk])
        return

    def UpdateReadCounter(self, disk, how_much):
        self.count_reads[disk] += how_much
        self.canvas.itemconfig(self.count_reads_id[disk], text='R:%d' % self.count_reads[disk])
        return

    def UpdateTime(self):
        self.canvas.itemconfig(self.timeID, text='Time: ' + str(self.timer))
        return
    
    def DrawWindow(self):
        return

    def BlockSetColor(self, disk, offset, color):
        block_id = self.disk_and_offset_to_rect_id[(disk, offset)]
        self.canvas.itemconfig(block_id, fill=color)
        return

    def QueueSetColor(self, index, fill_color):
        box_id = self.request_queue_box_ids[index]
        self.canvas.itemconfig(box_id, fill=fill_color)
        self.request_queue_counts[index] += 1
        count_id = self.request_queue_count_ids[index]
        self.canvas.itemconfig(count_id, text='%d' % self.request_queue_counts[index])
        return

    def SetSeekDirection(self, disk, dest_block):
        if self.GetHeadPosition(disk) < self.block_offset[dest_block]:
            self.seek_delta[disk] = self.seek_speed
        else:
            self.seek_delta[disk] = -self.seek_speed
        return

    def StartRead(self, disk, offset, logical_address, request, queue_index):
        self.current_optype[disk] = OP_READ
        self.StartRequest(disk, offset, logical_address, request, queue_index, 'orange')
        return

    def StartWrite(self, disk, offset, logical_address, request, queue_index):
        self.current_optype[disk] = OP_WRITE
        self.StartRequest(disk, offset, logical_address, request, queue_index, 'yellow')
        return

    def StartRequest(self, disk, offset, logical_address, request, queue_index, fill_color):
        self.QueueSetColor(queue_index, fill_color)
        self.disk_state[disk] = STATE_SEEK
        self.BlockSetColor(disk, offset, fill_color)
        self.SetSeekDirection(disk, logical_address)
        self.last_target[disk] = self.current_target[disk]
        self.current_target[disk] = request
        return
        
    def DoStripeScheduling(self, disk, index):
        request = self.request_queue[index]
        logical = request.GetLogicalAddress()
        if request.GetStatus(0) == REQ_NOT_STARTED and logical % self.disk_count == disk:
            offset = request.GetPhysicalOffset()
            request.MarkStart(self.timer)
            if request.GetType() == OP_READ:
                request.SetStatus(0, REQ_DO_READ)
                self.StartRead(disk, offset, logical, request, index)
            else:
                request.SetStatus(0, REQ_DO_WRITE)
                self.StartWrite(disk, offset, logical, request, index)
            return
        return
        
    def DoMirrorScheduling(self, disk, index):
        request = self.request_queue[index]
        logical = request.GetLogicalAddress()

        disks = request.GetPhysicalDiskList()
        if disks[0] == disk:
            disk_index = 0
        elif disks[1] == disk:
            disk_index = 1
        else:
            return

        if request.GetStatus(disk_index) == REQ_NOT_STARTED and (disk == disks[0] or disk == disks[1]):
            offset = request.GetPhysicalOffset()
            request.MarkStart(self.timer)
            if request.GetType() == OP_READ:
                request.SetStatus(disk_index, REQ_DO_READ)
                request.SetStatus(1 - disk_index, REQ_DONE)
                self.StartRead(disk, offset, logical, request, index)
            else:
                request.SetStatus(disk_index, REQ_DO_WRITE)
                self.StartWrite(disk, offset, logical, request, index)
            return
        return

    def DoRaid4Scheduling(self, disk, index):
        request = self.request_queue[index]
        logical = request.GetLogicalAddress()

        # reads: easy case, just like striped read
        if request.GetType() == OP_READ and request.GetStatus(0) == REQ_NOT_STARTED and logical % (self.disk_count-1) == disk:
            request.MarkStart(self.timer)
            request.SetStatus(0, REQ_DO_READ)
            offset = request.GetPhysicalOffset()
            self.StartRead(disk, offset, logical, request, index)
            return

        # now focus on writes: which turn into two reads, two writes
        if request.GetType() != OP_WRITE:
            return
        disks = request.GetPhysicalDiskList()
        if disks[0] != disk and disks[1] != disk:
            return

        if disks[0] == disk:
            disk_index = 0
        elif disks[1] == disk:
            disk_index = 1

        # check for possible FULL STRIPE WRITE
        (full_stripe_write, do_parity) = request.FullStripeWriteStatus()
        if full_stripe_write:
            offset = request.GetPhysicalOffset()
            if do_parity == False and request.GetStatus(disk_index) == REQ_NOT_STARTED:
                # print 'doing FULL STRIPE WRITE (parity)'
                # in this case, turn off both reads and write to parity disk
                request.MarkStart(self.timer)
                request.SetStatus(disk_index, REQ_DO_WRITE)
                request.SetStatus(1-disk_index, REQ_DONE)
                self.StartWrite(disk, offset, logical, request, index)
                return
            if do_parity == True and request.GetStatus(disk_index) == REQ_NOT_STARTED:
                # in this case, turn off reads but ensure both writes happen
                request.MarkStart(self.timer)
                request.SetStatus(disk_index, REQ_DO_WRITE)
                # request.SetStatus(1, REQ_DO_WRITE)
                # print 'doing FULL STRIPE WRITE (non-parity)'
                self.StartWrite(disk, offset, logical, request, index)
            return

        # normal case: SUBTRACTIVE PARITY handling
        # handle a LOGICAL WRITE that has not yet started
        # it starts with a READ
        if request.GetStatus(disk_index) == REQ_NOT_STARTED:
            request.MarkStart(self.timer)
            request.SetStatus(disk_index, REQ_DO_READ)
            offset = request.GetPhysicalOffset()
            self.StartRead(disk, offset, logical, request, index)
            return

        # handle a LOGICAL write that is mid way
        # it is ended with a WRITE
        if request.GetStatus(disk_index) == REQ_PARITY_WRITE_PHASE_BEGIN:
            request.SetStatus(disk_index, REQ_DO_WRITE)
            offset = request.GetPhysicalOffset()
            self.StartWrite(disk, offset, logical, request, index)
            return
        return

    def DoRaid5Scheduling(self, disk, index):
        request = self.request_queue[index]
        logical = request.GetLogicalAddress()

        # reads: easy case, just like striped read
        if request.GetType() == OP_READ and request.GetStatus(0) == REQ_NOT_STARTED and request.GetPhysicalDiskList()[0] == disk:
            request.MarkStart(self.timer)
            request.SetStatus(0, REQ_DO_READ)
            offset = request.GetPhysicalOffset()
            # print 'start', disk, offset
            self.StartRead(disk, offset, logical, request, index)
            return

        # now focus on writes: which turn into two reads, two writes
        if request.GetType() != OP_WRITE:
            return
        disks = request.GetPhysicalDiskList()
        if disks[0] != disk and disks[1] != disk:
            return

        if disks[0] == disk:
            disk_index = 0
        elif disks[1] == disk:
            disk_index = 1

        # normal case: SUBTRACTIVE PARITY handling
        # handle a LOGICAL WRITE that has not yet started
        # it starts with a READ
        if request.GetStatus(disk_index) == REQ_NOT_STARTED:
            request.MarkStart(self.timer)
            request.SetStatus(disk_index, REQ_DO_READ)
            offset = request.GetPhysicalOffset()
            # print 'start read', logical, disk, offset
            self.StartRead(disk, offset, logical, request, index)
            return

        # handle a LOGICAL write that is mid way
        # it is ended with a WRITE
        if request.GetStatus(disk_index) == REQ_PARITY_WRITE_PHASE_BEGIN:
            request.SetStatus(disk_index, REQ_DO_WRITE)
            offset = request.GetPhysicalOffset()
            # print 'start write', logical, disk, offset
            self.StartWrite(disk, offset, logical, request, index)
            return
        return
        

    def GetNextIOs(self):
        # check if done: if so, print stats and end animation
        if self.request_count == self.request_count_needed:
            self.UpdateTime()
            self.PrintStats()
            self.do_animate = False
            self.is_done = True
            return

        # scheduler
        for disk in range(self.disk_count):
            count = 0
            for index in self.request_queue:
                if self.window != -1 and count >= self.window:
                    continue
                count += 1
                if self.mapping == 0:
                    if self.disk_state[disk] == STATE_NULL:
                        self.DoStripeScheduling(disk, index)
                elif self.mapping == 1:
                    if self.disk_state[disk] == STATE_NULL:
                        self.DoMirrorScheduling(disk, index)
                elif self.mapping == 4:
                    if self.disk_state[disk] == STATE_NULL:
                        self.DoRaid4Scheduling(disk, index)
                elif self.mapping == 5:
                    if self.disk_state[disk] == STATE_NULL:
                        self.DoRaid5Scheduling(disk, index)
        return

    def GetHeadPosition(self, disk):
        return self.head_position[disk]['y1']

    def MoveHead(self, disk):
        self.head_position[disk]['y1'] += self.seek_delta[disk]
        self.head_position[disk]['y2'] += self.seek_delta[disk]
        self.canvas.coords(self.head_ids[disk],
                           self.head_position[disk]['x1'], self.head_position[disk]['y1'],
                           self.head_position[disk]['x2'], self.head_position[disk]['y2'])
        return

    def DoneWithSeek(self, disk):
        request = self.current_target[disk]
        if self.GetHeadPosition(disk) == self.offset_to_ypos[request.GetPhysicalOffset()]:
            return True
        return False

    def StartTransfer(self, disk):
        offset_current = self.current_target[disk].GetPhysicalOffset()
        if self.last_target[disk] == -1:
            offset_last = -1
        else:
            # print self.last_target[disk]
            offset_last = self.last_target[disk].GetPhysicalOffset()
        if offset_current == offset_last + 1:
            self.transfer_count[disk] = 1
        else:
            self.transfer_count[disk] = 10
        return

    def DoneWithTransfer(self, disk):
        return self.transfer_count[disk] == 0

    # called when a single IO is finished
    # note: request (as in mirrored or parity write) contains multiple IOs
    def MarkDone(self, disk):
        request = self.current_target[disk]
        low_level_op_type = self.current_optype[disk]
        
        if low_level_op_type == OP_WRITE:
            self.UpdateWriteCounter(disk, 1)
        elif low_level_op_type == OP_READ:
            self.UpdateReadCounter(disk, 1)

        # this is to move IOs through different phases
        if self.mapping == 4 or self.mapping == 5:
            (request_done, latency) = request.RequestLevel4Done(disk, self.timer)
        elif self.mapping == 1:
            (request_done, latency) = request.RequestLevel1Done(disk, self.timer)
        elif self.mapping == 0:
            (request_done, latency) = request.RequestLevel0Done(disk, self.timer)

        if request_done:
            self.logical_requests += 1
            self.latency_total += latency
            # print 'LATENCY', latency
            if self.window > 0:
                self.window += 1
        return

    def Animate(self):
        if self.do_animate == False:
            self.root.after(self.animate_delay, self.Animate)
            return

        # timer
        self.timer += 1
        self.UpdateTime()

        # move the blocks
        # now check if something should be happening
        for disk in range(self.disk_count):
            if self.disk_state[disk] == STATE_SEEK:
                if self.DoneWithSeek(disk):
                    self.disk_state[disk] = STATE_XFER
                    block_id = self.disk_and_offset_to_rect_id[(disk, self.current_target[disk].GetPhysicalOffset())]
                    self.StartTransfer(disk)
                else:
                    self.MoveHead(disk)
            if self.disk_state[disk] == STATE_XFER:
                self.transfer_count[disk] -= 1
                if self.DoneWithTransfer(disk):
                    offset = self.current_target[disk].GetPhysicalOffset()
                    self.MarkDone(disk)
                    self.request_count += 1
                    self.disk_state[disk] = STATE_NULL
                    self.BlockSetColor(disk, self.current_target[disk].GetPhysicalOffset(), self.color_map[(disk, offset)])
                    self.GetNextIOs()

        # make sure to keep the animation going!
        self.root.after(self.animate_delay, self.Animate)
        return

    def DoRequestStats(self):
        return

    def PrintStats(self):
        print 'Total Time:   ', self.timer
        print '  Requests:   ', self.logical_requests
        print '  Avg Latency: %.2f' % (float(self.latency_total) / float(self.logical_requests))
        return
        
# END: class Disk


    
#
# MAIN SIMULATOR
#
parser = OptionParser()
parser.add_option('-s', '--seed',            default='0',         help='Random seed',                                             action='store', type='int',    dest='seed')
parser.add_option('-m', '--mapping',         default='0',         help='0-striping, 1-mirroring, 4-raid4, 5-raid5',               action='store', type='int',    dest='mapping')
parser.add_option('-a', '--addr',            default='',          help='Request list (comma-separated) [-1 -> use addrDesc]',     action='store', type='string', dest='addr')
parser.add_option('-r', '--read_fraction',   default='0.5',       help='Fraction of requests that are reads',                     action='store', type='string', dest='read_fraction')
parser.add_option('-A', '--addr_desc',       default='5,-1,0',    help='Num requests, max request (-1->all), min request',        action='store', type='string', dest='addr_desc')
parser.add_option('-B', '--balanced',        default=True,        help='If generating random requests, balance across disks',     action='store_true',           dest='balance')
parser.add_option('-S', '--seek_speed',      default='4',         help='Speed of seek (1,2,4,5,10,20)',                           action='store', type='int',    dest='seek_speed')
parser.add_option('-p', '--policy',          default='FIFO',      help='Scheduling policy (FIFO, SSTF, SATF, BSATF)',             action='store', type='string', dest='policy')
parser.add_option('-w', '--window',          default=-1,          help='Size of scheduling window (-1 -> all)',                   action='store', type='int',    dest='window')
parser.add_option('-D', '--delay',           default=20,          help='Animation delay; bigger is slower',                       action='store', type='int',    dest='animate_delay')
parser.add_option('-G', '--graphics',        default=True,        help='Turn on graphics',                                        action='store_true',           dest='graphics')
parser.add_option('-c', '--compute',         default=False,       help='Compute the answers',                                     action='store_true',           dest='compute')
parser.add_option('-P', '--print_options',   default=False,       help='Print the options',                                       action='store_true',           dest='print_options')
(options, args) = parser.parse_args()

if options.print_options:
    print 'OPTIONS seed', options.seed
    print 'OPTIONS addr', options.addr
    print 'OPTIONS addr_desc', options.addr_desc
    print 'OPTIONS seek_speed', options.seek_speed
    print 'OPTIONS window', options.window
    print 'OPTIONS policy', options.policy
    print 'OPTIONS compute', options.compute
    print 'OPTIONS read_fraction', options.read_fraction
    print 'OPTIONS graphics', options.graphics
    print 'OPTIONS animate_delay', options.animate_delay
    print ''

if options.window == 0:
    print 'Scheduling window (%d) must be positive or -1 (which means a full window)' % options.window
    sys.exit(1)

# set up simulator info
d = Raid(mapping=options.mapping, addr_desc=options.addr_desc, addr=options.addr,
         disk_count=4, seek_speed=options.seek_speed, seed=options.seed, balance=options.balance,
         read_fraction=float(options.read_fraction), window=options.window, animate_delay=options.animate_delay)

# run simulation
d.Go()
