#! /usr/bin/env python3

from __future__ import print_function
import random
import re
import string
import os
from optparse import OptionParser

#
# to make Python2 and Python3 act the same -- how dumb
# 
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

#
# boilerplate code for .c files used by both readable/runnable code versions
#
class Boilerplate:
    def __init__(self, fd):
        self.fd = fd
        return

    def init(self):
        self.fd.write('#include <assert.h>\n')
        self.fd.write('#include <stdio.h>\n')
        self.fd.write('#include <stdlib.h>\n')
        self.fd.write('#include <string.h>\n')
        self.fd.write('#include <sys/time.h>\n')
        self.fd.write('#include <sys/wait.h>\n')
        self.fd.write('#include <unistd.h>\n')
        self.fd.write('\n')
        self.fd.write('void wait_or_die() {\n')
        self.fd.write('    int rc = wait(NULL);\n')
        self.fd.write('    assert(rc > 0);\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('int fork_or_die() {\n')
        self.fd.write('    int rc = fork();\n')
        self.fd.write('    assert(rc >= 0);\n')
        self.fd.write('    return rc;\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        return

    def init_runnable(self):
        self.init()
        self.fd.write('#define Time_GetSeconds() ({ struct timeval t; int rc = gettimeofday(&t, NULL); assert(rc == 0); (double) t.tv_sec + (double) t.tv_usec/1e6; })\n')
        self.fd.write('\n')
        self.fd.write('double t_start;\n')
        self.fd.write('\n')
        self.fd.write('struct pid_map {\n')
        self.fd.write('    int pid;\n')
        self.fd.write('    char name[10];\n')
        self.fd.write('    struct pid_map *next;\n')
        self.fd.write('};\n')
        self.fd.write('\n')
        self.fd.write('struct pid_map *head = NULL;\n')
        self.fd.write('\n')
        self.fd.write('void Space(char c) {\n')
        self.fd.write('    int i;\n')
        self.fd.write('    for (i = 0; i < 5 * (c - \'a\'); i++) {\n')
        self.fd.write('        printf(\" \"); \n')
        self.fd.write('    }\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('char *Lookup(int pid) {\n')
        self.fd.write('    struct pid_map *curr = head;\n')
        self.fd.write('    while (curr) {\n')
        self.fd.write('        if (curr->pid == pid) \n')
        self.fd.write('	           return(curr->name);\n')
        self.fd.write('	       curr = curr->next;\n')
        self.fd.write('    }\n')
        self.fd.write('    return NULL;\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('void Record(int pid, char *m) {\n')
        self.fd.write('    struct pid_map *n = malloc(sizeof(struct pid_map));\n')
        self.fd.write('    assert(n);\n')
        self.fd.write('    n->pid = pid;\n')
        self.fd.write('    strcpy(n->name, m);\n')
        self.fd.write('    n->next = head;\n')
        self.fd.write('    head = n;\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('void Wait(char *m) {\n')
        self.fd.write('    int rc = wait(NULL);\n')
        self.fd.write('    assert(rc > 0);\n')
        self.fd.write('    double t = Time_GetSeconds() - t_start;\n')
        self.fd.write('    printf(\"%3d \", (int)t);\n')
        self.fd.write('    Space(m[0]);\n')
        self.fd.write('    char *n = Lookup(rc);\n')
        self.fd.write('    assert(n != NULL);\n')
        self.fd.write('    printf(\"%s<-%s\\n\", m, n);\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('void Sleep(int s, char *m) {\n')
        self.fd.write('    sleep(s);\n')
        self.fd.write('    double t = Time_GetSeconds() - t_start;\n')
        self.fd.write('    printf(\"%3d %s\\n\", (int)t, m);\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('void Fork(char *p, char *c) {\n')
        self.fd.write('    double t = Time_GetSeconds() - t_start;\n')
        self.fd.write('    printf(\"%3d \", (int)t);\n')
        self.fd.write('    Space(p[0]);\n')
        self.fd.write('    printf(\"%s->%s\\n\", p, c);\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('void __Begin(char *m) {\n')
        self.fd.write('    double t = Time_GetSeconds() - t_start;\n')
        self.fd.write('    printf(\"%3d \", (int)t);\n')
        self.fd.write('    Space(m[0]);\n')
        self.fd.write('    printf(\"%s+\\n\", m);\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('void __End(char *m) {\n')
        self.fd.write('    double t = Time_GetSeconds() - t_start;\n')
        self.fd.write('    printf(\"%3d \", (int)t);\n')
        self.fd.write('    Space(m[0]);\n')
        self.fd.write('    printf(\"%s-\\n\", m);\n')
        self.fd.write('}\n')
        self.fd.write('\n')
        self.fd.write('#define Begin(m) { __Begin(m); }\n')
        self.fd.write('#define End(m)   { __End(m); exit(0); }\n')
        self.fd.write('\n')
        return

    def fini(self):
        self.fd.write('    return 0;\n')
        self.fd.write('}\n\n')
        return

    def main(self):
        self.fd.write('int main(int argc, char *argv[]) {\n')
        return

    def main_runnable(self):
        self.main()
        self.fd.write('    int rc;\n')
        self.fd.write('    t_start = Time_GetSeconds();\n')
        return

    def __fini__(self):
        close(self.fd)
        return
    

class CodeGeneratorReadable:
    def __init__(self, out_file_base, actions):
        self.out_file = out_file_base + '.c'
        self.actions = actions

        self.tab_level = 1
        self.fd = open(self.out_file, 'w')
        self.boiler = Boilerplate(self.fd)
        return

    def __fini__(self):
        self.fd.close()
        return

    def tab(self):
        for i in range(self.tab_level):
            self.fd.write('    ')
        return

    def add_thread(self, thread_id):
        self.tab()
        self.fd.write('// thread %s\n' % thread_id)
        return

    def add_fork(self):
        self.tab()
        self.fd.write('if (fork_or_die() == 0) {\n')
        self.tab_level += 1
        return

    def add_sleep(self, sleep_time):
        self.tab()
        self.fd.write('sleep(%s);\n' % sleep_time)
        return

    def add_exit(self):
        self.tab()
        self.fd.write('exit(0);\n')
        self.tab_level -= 1
        self.tab()
        self.fd.write('}\n')
        return

    def add_wait(self):
        self.tab()
        self.fd.write('wait_or_die();\n')
        return
        
    def generate(self):
        self.boiler.init()
        self.boiler.main()
        self.add_thread('a')
        for a in actions:
            tmp = a.split(' ')
            if tmp[0] == 'fork':
                # fork thread_id sleep_time
                assert(len(tmp) == 3)
                self.add_fork()
                self.add_sleep(tmp[2])
                self.add_thread(tmp[1])
            elif tmp[0] == 'exit':
                assert(len(tmp) == 1)
                self.add_exit()
            elif tmp[0] == 'wait':
                assert(len(tmp) == 1)
                self.add_wait()
            else:
                print('bad command')
                exit(1)
                return
        self.boiler.fini()
        self.__fini__()
        return

class CodeGeneratorRunnable:
    def __init__(self, out_file_base, actions):
        self.out_file = out_file_base + '.c'
        self.actions = actions

        self.tab_level = 1
        self.fd = open(self.out_file, 'w')
        self.boiler = Boilerplate(self.fd)

        self.parent_list = []
        self.waiting_for = {}

        self.used_times = {}
        return

    def __fini__(self):
        self.fd.close()
        return

    def tab(self):
        for i in range(self.tab_level):
            self.fd.write('    ')
        return

    def add_thread(self, thread_id):
        self.tab()
        self.waiting_for[thread_id] = []
        self.fd.write('Begin(\"%s\");\n' % thread_id)
        self.curr_thread = thread_id
        return

    def add_fork(self, child_thread, sleep_time):
        self.parent_list.append(self.curr_thread)
        self.waiting_for[self.curr_thread].append(child_thread)
        # print('add fork for %s' % self.curr_thread, self.waiting_for[self.curr_thread])
        self.tab()
        self.fd.write('Fork(\"%s\", \"%s\");\n' % (self.curr_thread, child_thread))
        self.tab()
        self.fd.write('if ((rc = fork_or_die()) == 0) {\n')
        self.tab_level += 1
        return

    def add_sleep(self, sleep_time):
        self.tab()
        self.fd.write('sleep(%s);\n' % sleep_time)
        return

    def add_exit(self):
        # MUST HAVE DONE ALL WAITS(!)
        if len(self.waiting_for[self.curr_thread]) > 0:
            print('error: thread cannot exit without performing all needed waits')
            print('  thread %s has outstanding children:' % self.curr_thread, self.waiting_for[self.curr_thread])
            exit(1)
        self.tab()
        self.fd.write('End(\"%s\");\n' % self.curr_thread)
        self.tab_level -= 1
        self.tab()
        self.fd.write('}\n')
        self.tab()
        self.fd.write('Record(rc, \"%s\");\n' % self.curr_thread)
        self.curr_thread = self.parent_list.pop()
        return

    def add_wait(self):
        self.tab()
        # how to know who to wait for?
        waiting_for = self.waiting_for[self.curr_thread].pop(0)
        # print('%s waited for %s' % (self.curr_thread, waiting_for[1]))
        self.fd.write('Wait(\"%s\");\n' % self.curr_thread);
        return
        
    def generate(self):
        self.boiler.init_runnable()
        self.boiler.main_runnable()
        self.add_thread('a')
        for a in actions:
            tmp = a.split(' ')
            if tmp[0] == 'fork':
                # fork thread_id sleep_time
                assert(len(tmp) == 3)
                self.add_fork(tmp[1], tmp[2])
                self.add_sleep(tmp[2])
                self.add_thread(tmp[1])
            elif tmp[0] == 'exit':
                assert(len(tmp) == 1)
                self.add_exit()
            elif tmp[0] == 'wait':
                assert(len(tmp) == 1)
                self.add_wait()
            else:
                print('bad command')
                exit(1)
                return
        self.boiler.fini()
        self.__fini__()
        return

#
# Generates input for C code generators
#
class ProgramGenerator:
    def __init__(self, num_actions):
        self.num_actions = num_actions

        self.names = string.ascii_lowercase + string.ascii_uppercase
        self.name_index = 1

        self.used_times = {}
        self.used_times[0] = True

        return

    def get_next_name(self):
        if self.name_index == len(self.names):
            print('program generator: out of names (too many processes)')
            exit(1)
        n = self.names[self.name_index]
        self.name_index += 1
        return n

    def get_sleep_time(self):
        return random_randint(1, 10)

    def add_fork_begin(self):
        name = self.get_next_name()
        sleep_time = self.get_sleep_time()
        self.actions.append('fork %s %d' % (name, sleep_time))
        self.need_wait[self.fork_level] += 1
        self.fork_level += 1
        self.need_wait[self.fork_level] = 0
        return

    def add_fork_end(self):
        self.actions.append('exit')
        self.fork_level -= 1
        return

    def add_wait(self):
        self.actions.append('wait')
        self.need_wait[self.fork_level] -= 1
        return

    def clean_up(self):
        n = self.need_wait[self.fork_level]
        for i in range(n):
            self.actions.append('wait')
        if self.fork_level > 0:
            self.actions.append('exit')
        return n + 1

    def generate(self):
        self.actions = []
        self.fork_level = 0
        self.need_wait = {}
        self.need_wait[self.fork_level] = 0

        self.fork_chance = 0.4
        self.wait_chance = 0.7
        self.exit_chance = 1.0

        n = 0
        while n < self.num_actions:
            r = random.random()
            if r < self.fork_chance:
                print('fork')
                self.add_fork_begin()
                n += 1
            elif r < self.wait_chance:
                print('wait?')
                if self.need_wait[self.fork_level] > 0:
                    print('wait')
                    self.add_wait()
                    n += 1
            else:    
                print('exit')
                if self.fork_level > 0:
                    # must do all needed waits now
                    # self.add_fork_end()
                    n += self.clean_up()
                    self.fork_level -= 1
            # diagnostics
            print('level', self.fork_level, 'actions', self.actions, 'nw', self.need_wait[self.fork_level])

        # clean up:
        while self.fork_level >= 0:
            self.clean_up()
            self.fork_level -= 1
            
        return self.actions
        
#
# Parses user input into program understood by C code generators
#
class Parser:
    def __init__(self, program):
        self.program = program
        self.orig_program = program

    def abort_if(self, condition, message):
        if condition:
            print('bad program: [%s]' % self.orig_program)
            print(message)
            exit(1)
        return

    def parse(self):
        # remove spaces around commas
        program = self.program
        p = re.compile('\s*,\s*')
        m = p.search(program)
        while m:
            program = program.replace(m.group(), ',', 1)
            m = p.search(program, m.end())
        
        # add spaces around braces
        program = program.replace('{', ' { ')
        program = program.replace('}', ' } ')
    
        # now go through and find the commands
        # easy to parse by just splitting on spaces
        tokens = program.split()
        action_list = []  # add actions understood by generators here
        curr = 0          # where we are in list of tokens
        brace_count = 0   # ensures matching number of braces
        wait_count = {}   # tracks, per fork-nesting level, that enough waits are added
        fork_level = 0    # tracks level of forks
        wait_count[fork_level] = 0
        while curr < len(tokens):
            if tokens[curr] == '':
                curr += 1
                continue
            elif tokens[curr] == 'fork':
                wait_count[fork_level] += 1
                fork_level += 1
                wait_count[fork_level] = 0
                self.abort_if(len(tokens) < curr + 2, 'malformed program: fork needs process name,sleep length plus {description} of what the forked process should do')
                args = tokens[curr + 1]
                args_split = args.split(',')
                self.abort_if(len(args_split) != 2, 'not enough args to fork (process name, sleep time)')
                lbrace = tokens[curr + 2]
                self.abort_if(lbrace != '{', 'must have {} following fork')
                action_list.append('fork %s %s' % (args_split[0], args_split[1]))
                # skip over the argument and the left brace
                curr += 2
                brace_count += 1
            elif tokens[curr] == '}':
                self.abort_if(fork_level == 0, 'extra close brace')
                action_list.append("exit")
                self.abort_if(wait_count[fork_level] != 0, '#waits does not match #forks')
                brace_count -= 1
                fork_level -= 1
            elif tokens[curr] == 'wait':
                wait_count[fork_level] -= 1
                action_list.append("wait")
            else:
                self.abort_if(True, 'unrecognized token %s' % tokens[curr])
            # loop until all done with tokens
            curr += 1

        # some final checks
        self.abort_if(wait_count[0] != 0, '#waits does not match #forks')
        self.abort_if(brace_count != 0, 'unbalanced braces')

        return action_list

#
# MAIN PROGRAM
#

parser = OptionParser()
parser.add_option('-s', '--seed', default=-1, help='random seed', action='store', type='int', dest='seed')
parser.add_option('-r', '--readable', default='read', help='file to read (e.g., read.c)', action='store', type='string', dest='readable')
parser.add_option('-R', '--runnable', default='run', help='file to run (e.g., run.c)', action='store', type='string', dest='runnable')
parser.add_option('-n', '--num_actions', default=10, help='num actions', action='store', type='int', dest='num_actions')
parser.add_option('-A', '--action_list', default='', help='action list, instead of randomly generated ones (simple example: "fork b,10 {} wait" is a program that runs a process (called a) which then forks process b which runs for 10 seconds, and then a waits for b to complete; see README for details', action='store', type='string', dest='action_list')
parser.add_option('-c', '--compute', help='compute answers for me', action='store_true', default=False, dest='solve')

(options, args) = parser.parse_args()

if options.seed != -1:
    random_seed(options.seed)

if options.action_list == '':
    pg = ProgramGenerator(options.num_actions)
    actions = pg.generate()
else:
    action_list = options.action_list
    p = Parser(action_list)
    actions = p.parse()

print(actions)

cg_read = CodeGeneratorReadable(options.readable, actions)
cg_read.generate()

cg_run = CodeGeneratorRunnable(options.runnable, actions)
cg_run.generate()

# now either list the code, or run it
if options.solve:
    os.system('gcc -o %s %s.c -Wall' % (options.runnable, options.runnable))
    os.system('./%s' % options.runnable)
else:
    print('cat %s.c' % options.readable)
    stream = os.popen('cat %s.c' % options.readable)
    output = stream.read()
    print(output)
    # rc = os.system('cat %s.c' % options.readable)
    # print(rc)

    
    
