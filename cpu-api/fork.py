#! /usr/bin/env python3

# from this sort of thing
# a forks b
# a forks c
# a forks d
# b forks e
# b forks f
# d forks g

# to a process tree
#a --- b --- e
#   |     |
#   |     |- f
#   |- c
#   |
#   |- d --- g


from __future__ import print_function
import random
import string
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
#
#
class Forker:
    def __init__(self, fork_percentage, actions, action_list, show_tree, just_final, solve):
        self.fork_percentage = fork_percentage
        self.max_actions = actions
        self.action_list = action_list
        self.show_tree = show_tree
        self.just_final = just_final
        self.solve = solve

        # root process is always this
        self.root_name = 'a'

        # process list: names of all active processes
        self.process_list = [self.root_name]

        # for each process, it's children
        self.children = {}
        self.children[self.root_name] = []

        # and track parents
        self.parents = {}

        # this is for pretty process names...
        self.name_length = 1
        self.base_names = string.ascii_lowercase + string.ascii_uppercase
        self.curr_names = self.base_names
        self.curr_index = 1
        
        return

    def grow_names(self):
        new_names = []
        for b1 in self.curr_names:
            for b2 in self.base_names:
                new_names.append(b1 + b2)
        self.curr_names = new_names
        self.curr_index = 0
        return

    def get_name(self):
        if self.curr_index == len(self.curr_names):
            self.grow_names()
                
        name = self.curr_names[self.curr_index]
        self.curr_index += 1
        return name

    def just_name(self, name):
        return name

    def walk(self, p, level):
        for i in range(level):
            print('   ', end='')
        print('%2s' % self.just_name(p))
        for child in self.children[p]:
            self.walk(child, level + 1)
        return

    def do_fork(self, p, c):
        self.process_list.append(c)
        self.children[c] = []
        self.children[p].append(c)
        self.parents[c] = p
        return '%s forks %s' % (p, c)

    def do_exit(self, p):
        # remove the process from the process list
        exit_parent = self.parents[p]
        self.process_list.remove(p)
        # for each orphan, set its parent to exiting proc's parent
        for orphan in self.children[p]:
            self.parents[orphan] = exit_parent
            self.children[exit_parent].append(orphan)
        # remove the entry from its parent child list
        self.children[exit_parent].remove(p)
        # remove the entry for this proc from children
        self.children[p] = -1
        self.parents[p] = -1
        return '%s EXITS' % p

    def bad_action(self, action):
        print('bad action (%s), must be X+Y or X- where X and Y are processes' % action)
        exit(1)
        return

    def check_legal(self, action):
        if '+' in action:
            tmp = action.split('+')
            if len(tmp) != 2:
                self.bad_action(action)
            return [tmp[0], tmp[1]]
        elif '-' in action:
            tmp = action.split('-')
            if len(tmp) != 2:
                self.bad_action(action)
            return [tmp[0]]
        else:
            self.bad_action(action)
        return 
    
    def run(self):
        print('Initial Process Tree:')
        self.walk(self.root_name, 0)
        print('')

        if self.action_list != '':
            # use specific action list
            action_list = self.action_list.split(',')
        else:
            action_list = []
            actions = 0
            temp_process_list = [self.root_name]
            while actions < self.max_actions:
                if random.random() < self.fork_percentage:
                    # FORK:: pick random parent, add child to it
                    fork_choice = random_choice(temp_process_list)
                    new_child = self.get_name()
                    action_list.append('%s+%s' % (fork_choice, new_child))
                    temp_process_list.append(new_child)
                else:
                    # EXIT:: pick random child, remove it
                    #        exception: no killing root process, sorry
                    exit_choice = random_choice(temp_process_list)
                    if exit_choice == self.root_name:
                        continue
                    temp_process_list.remove(exit_choice)
                    action_list.append('%s-' % exit_choice)
                actions += 1

        for a in action_list:
            tmp = self.check_legal(a)
            if len(tmp) == 2:
                fork_choice, new_child = tmp[0], tmp[1]
                if fork_choice not in self.process_list:
                    self.bad_action(a)
                action = self.do_fork(fork_choice, new_child)
            else:
                exit_choice = tmp[0]
                if exit_choice not in self.process_list:
                    self.bad_action(a)
                action = self.do_exit(exit_choice)
            
            # if we got here, we actually did an action...
            if self.show_tree:
                # SHOW TREES (guess actions)
                if self.solve:
                    print('Action: ', action)
                else:
                    print('Action?')
                print('Process Tree:')
                self.walk(self.root_name, 0)
            else:
                # SHOW ACTIONS (guess tree)
                print('Action: ', end='')
                print(action)
                if not self.just_final:
                    if self.solve:
                        print('Process Tree:')
                        self.walk(self.root_name, 0)
                    else:
                        print('Process Tree?')

        if self.just_final:
            if self.solve:
                print('\nFinal Process Tree:')
                self.walk(self.root_name, 0)
                print('')
            else:
                print('\nFinal Process Tree?\n')
            
        return


#
# main
#

parser = OptionParser()
parser.add_option('-s', '--seed', default=-1, help='the random seed', action='store', type='int', dest='seed')
parser.add_option('-f', '--forks', default=0.7, help='percent of actions that are forks (not exits)', action='store', type='float', dest='fork_percentage')
parser.add_option('-A', '--action_list', default='', help='action list, instead of randomly generated ones (format: a+b,b+c,b- means a fork b, b fork c, b exit)', action='store', type='string', dest='action_list')
parser.add_option('-a', '--actions', default=10, help='number of forks/exits to do', action='store', type='int', dest='actions')
parser.add_option('-t', help='show tree (not actions)', action='store_true', default=False, dest='show_tree')
parser.add_option('-F', help='just show final state', action='store_true', default=False, dest='just_final')
parser.add_option('-c', help='compute answers for me', action='store_true', default=False, dest='solve')

(options, args) = parser.parse_args()

if options.seed != -1:
    random_seed(options.seed)

if options.fork_percentage <= 0.001:
    print('fork_percentage must be > 0.001')
    exit(1)

print('')
print('ARG seed', options.seed)
print('ARG fork_percentage', options.fork_percentage)
print('ARG actions', options.actions)
print('ARG action_list', options.action_list)
print('ARG show_tree', options.show_tree)
print('ARG just_final', options.just_final)
print('ARG solve', options.solve)
print('')

f = Forker(options.fork_percentage, options.actions, options.action_list, options.show_tree, options.just_final, options.solve)
f.run()


