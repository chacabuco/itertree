from __future__ import absolute_import

import timeit
import os

#max_items = 5000
max_items = 500000

repeat = 4

print('We run for treesizes: %i with %i repetitions'%(max_items,repeat))

from itertree import *

root=None

TMP_FOLDER=os.path.abspath('../test/tmp')

if not os.path.exists(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)

def performance_dt_build_insert():
    #tag access
    global dt_root,max_items
    dt = iTree('root')
    #dt.pre_alloc_list(max_items)
    #append itertree with items
    for i in range(max_items):
        dt.insert(1,iTree('%i' % i))

def performance_dt_build():
    #tag access
    global dt_root,max_items
    dt = iTree('root')
    #dt.pre_alloc_list(max_items)
    #append itertree with items
    for i in range(max_items):
        dt += iTree('%i' % i)
    dt_root=dt

def performance_dt_build2():
    #tag access
    global dt_root,max_items
    dt = iTree('root')
    #append itertree with items
    dt=iTree('root',subtree=[iTree('%i' % i) for i in range(max_items)])
    dt_root=dt

def performance_dt_get_tags():
    #tag access
    global dt_root,max_items
    dt=dt_root

    #read itertree items per tag and index
    for i in range(max_items):
        a = dt['%i' % i]

def performance_dt_get_tag_idx():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    # we use a pre allocation
    for i in range(max_items):
        a = dt[TagIdx('%i' % i,0)]

def performance_dt_get_idx():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    for i in range(max_items):
        a = dt[i]

def performance_dt_dump():
    global dt_root,TMP_FOLDER
    dt_root.dump(TMP_FOLDER+'/perfomance1.dtz',overwrite=True)

def performance_dt_load():
    global dt_root, TMP_FOLDER
    root=iTree('tmp').load(TMP_FOLDER+'/perfomance1.dtz')

a = timeit.timeit(performance_dt_build_insert, number=repeat)
print('Exectime time itertree build (with insert): {}'.format(a / repeat))
a = timeit.timeit(performance_dt_build, number=repeat)
print('Exectime time itertree build: {}'.format(a / repeat))
a = timeit.timeit(performance_dt_build2, number=repeat)
print('Exectime time itertree build: with subtree list comprehension: {}'.format(a / repeat))
a = timeit.timeit(performance_dt_get_tags, number=repeat)
print('Exectime time itertree tag access: {}'.format(a / repeat))
a = timeit.timeit(performance_dt_get_tag_idx, number=repeat)
print('Exectime time itertree tag index access: {}'.format(a / repeat))
a = timeit.timeit(performance_dt_get_idx, number=repeat)
print('Exectime time itertree index access: {}'.format(a / repeat))

a = timeit.timeit(performance_dt_dump, number=repeat)
print('Exectime time itertree save to file: {}'.format(a / repeat))
a = timeit.timeit(performance_dt_load, number=repeat)
print('Exectime time itertree load from file: {}'.format(a / repeat))

# we compare here with dict, OrderedDict and list
print('-- Standard classes -----------------------------------')


def performance_dict_build():
    #tag access
    global dt_root,max_items
    dt = {}
    #append itertree with items
    for i in range(max_items):
        dt['%i' % i]=0
    dt_root=dt

def performance_dict_get_keys():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    for i in range(max_items):
        a = dt['%i' % i]

def performance_dict_get_idx():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    for i in range(max_items):
        a = list(dt.keys())[i]

def performance_list_build():
    #tag access
    global dt_root,max_items
    dt = []
    #append itertree with items
    #for i in range(max_items):
    #    dt.append(['%i' % i])
    dt=['%i'%i for i in range(max_items)]
    dt_root=dt

def performance_list2_build():
    #tag access
    global dt_root,max_items
    dt = []
    #append itertree with items
    #for i in range(max_items):
    #    dt.append(['%i' % i])
    for i in range(max_items):
        dt.append('%i'%i)
    dt_root=dt

def performance_list3_build():
    #tag access
    global dt_root,max_items
    dt = []
    #append itertree with items
    #for i in range(max_items):
    #    dt.append(['%i' % i])
    for i in range(max_items):
        dt.insert(0,'%i'%i)
    dt_root=dt

def performance_list_get_idx():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    for i in range(max_items):
        a = dt[i]

def performance_list_get_key():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    for i in range(max_items):
        a = dt[dt.index('%i'%i)]

a = timeit.timeit(performance_dict_build, number=repeat)
print('Exectime time dict build: {}'.format(a / repeat))
a = timeit.timeit(performance_dict_get_keys, number=repeat)
print('Exectime time dict key access: {}'.format(a / repeat))
if max_items<6000:
    a = timeit.timeit(performance_dict_get_idx, number=repeat)
    print('Exectime time dict index access: {}'.format(a / repeat))
else:
    print('Exectime time dict index access: skipped incredible slow')
a = timeit.timeit(performance_list_build, number=repeat)
print('Exectime time list build (via comprehension): {}'.format(a / repeat))
a = timeit.timeit(performance_list2_build, number=repeat)
print('Exectime time list build (via append): {}'.format(a / repeat))
a = timeit.timeit(performance_list3_build, number=repeat)
print('Exectime time list build (via insert): {}'.format(a / repeat))
a = timeit.timeit(performance_list_get_idx, number=repeat)
print('Exectime time list index access: {}'.format(a / repeat))
if max_items<6000:
    a = timeit.timeit(performance_list_get_key, number=repeat)
    print('Exectime time list key access: {}'.format(a / repeat))
else:
    print('Exectime time list key access: Skipped incredible slow')

from collections import OrderedDict,deque

def performance_odict_build():
    #tag access
    global dt_root,max_items
    dt = OrderedDict()
    #append itertree with items
    for i in range(max_items):
        dt['%i' % i]=0
    dt_root=dt

def performance_odict_get_keys():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    for i in range(max_items):
        a = dt['%i' % i]

def performance_deque_build():
    #tag access
    global dt_root,max_items
    dt = deque()
    #append itertree with items
    for i in range(max_items):
        dt.append(['%i' % i])
    dt_root=dt

def performance_deque_build2():
    #tag access
    global dt_root,max_items
    dt = deque()
    #append itertree with items
    for i in range(max_items):
        dt.insert(0,['%i' % i])

def performance_deque_get_idx():
    #tag access
    global dt_root,max_items
    dt=dt_root
    #read itertree items per tag and index
    for i in range(max_items):
        a = dt[i]

a = timeit.timeit(performance_odict_build, number=repeat)
print('Exectime time OrderedDict build: {}'.format(a / repeat))
a = timeit.timeit(performance_odict_get_keys, number=repeat)
print('Exectime time OrderedDict key access: {}'.format(a / repeat))
a = timeit.timeit(performance_deque_build, number=repeat)
print('Exectime time deque build (append): {}'.format(a / repeat))
a = timeit.timeit(performance_deque_build2, number=repeat)
print('Exectime time deque build (insert): {}'.format(a / repeat))
a = timeit.timeit(performance_deque_get_idx, number=repeat)
print('Exectime time deque index access: {}'.format(a / repeat))

# now we try some external packages (must be installed in the system for the test)

try:
    from sortedcontainers import SortedDict
    print('-- SortedDict ---------------------------------')

    def performance_sdict_build():
        global dt_root,max_items
        dt = SortedDict()
        for i in range(max_items):
            dt['%i' % i] = SortedDict()
        dt_root=dt

    def performance_sdict_get_key():
        global dt_root, max_items
        dt=dt_root
        for i in range(max_items):
            a = dt['%i' % i]

    def performance_sdict_get_idx():
        global dt_root, max_items
        dt=dt_root
        for i in range(max_items):
            a = dt.peekitem(i)

    a = timeit.timeit(performance_sdict_build, number=repeat)
    print('Exectime time SortedDict build: {}'.format(a / repeat))
    a = timeit.timeit(performance_sdict_get_key, number=repeat)
    print('Exectime time SortedDict key access: {}'.format(a / repeat))
    a = timeit.timeit(performance_sdict_get_idx, number=repeat)
    print('Exectime time SortedDict index access: {}'.format(a / repeat))


except ImportError:
    pass

try:
    from lldict2 import llDict as llDict2
    print('-- llDict2 ---------------------------------')

    def performance_lldict_build():
        global dt_root,max_items
        dt = llDict2()
        for i in range(max_items):
            dt['%i' % i] = llDict2()
        dt_root=dt

    def performance_lldict_get_key():
        global dt_root, max_items
        dt=dt_root
        for i in range(max_items):
            a = dt['%i' % i]

    def performance_lldict_get_idx():
        global dt_root, max_items
        dt=dt_root
        for i in range(max_items):
            a = dt.peekitem(i)

    a = timeit.timeit(performance_sdict_build, number=repeat)
    print('Exectime time llDict build: {}'.format(a / repeat))
    a = timeit.timeit(performance_sdict_get_key, number=repeat)
    print('Exectime time llDict key access: {}'.format(a / repeat))

except ImportError:
    pass

try:
    from lldict3 import llDict as llDict3
    print('-- llDict3 ---------------------------------')

    def performance_lldict_build():
        global dt_root,max_items
        dt = llDict3()
        for i in range(max_items):
            dt['%i' % i] = llDict3()
        dt_root=dt

    def performance_lldict_get_key():
        global dt_root, max_items
        dt=dt_root
        for i in range(max_items):
            a = dt['%i' % i]

    def performance_lldict_get_idx():
        global dt_root, max_items
        dt=dt_root
        for i in range(max_items):
            a = dt.peekitem(i)

    a = timeit.timeit(performance_sdict_build, number=repeat)
    print('Exectime time llDict3 build: {}'.format(a / repeat))
    a = timeit.timeit(performance_sdict_get_key, number=repeat)
    print('Exectime time llDict3 key access: {}'.format(a / repeat))

except ImportError:
    pass


print('-- xml ElementTree ---------------------------------')

import xml.etree.ElementTree as ET

def performance_et_build():
    global dt_root, max_items
    dt = ET.Element('root')
    for i in range(max_items):
        ET.SubElement(dt,'%i' % i)
    dt_root = dt


def performance_et_get_key():
    global dt_root, max_items
    dt = dt_root
    for i in range(max_items):
        a = dt.find('%i' % i)


def performance_et_get_idx():
    global dt_root, max_items
    dt = dt_root
    for i in range(max_items):
        a=dt[i]


a = timeit.timeit(performance_et_build, number=repeat)
print('Exectime time xml ElementTree build: {}'.format(a / repeat))
if max_items<6000:
    a = timeit.timeit(performance_et_get_key, number=repeat)
    print('Exectime time xml ElementTree key access: {}'.format(a / repeat))
else:
    print('xml ElementTree key access skipped -> too slow')
a = timeit.timeit(performance_et_get_idx, number=repeat)
print('Exectime time xml ElementTree index access: {}'.format(a / repeat))

try:
    from anytree import Node, search

    print('-- anytree ---------------------------------')

    def performance_at_build():
        global dt_root, max_items,nodes
        dt = Node('root')
        for i in range(5000):
            b=Node('%i' % i, parent=dt)
        dt_root = dt

    def performance_at_get_key():
        global dt_root, max_items
        dt = dt_root
        for i in range(max_items):
            b = search.find(dt, lambda node: node.name == "%i" % i)

    def performance_at_get_idx():
        global dt_root, max_items
        dt = dt_root
        for i in range(max_items):
            b = dt.children[i]

    a = timeit.timeit(performance_at_build, number=repeat)
    print('Exectime time Anytree build: {}'.format(a / repeat))
    if max_items<6000:
        a = timeit.timeit(performance_at_get_key, number=repeat)
        print('Exectime time Anytree key access (no cache): {}'.format(a / repeat))
    else:
        print('Anytree key access skipped -> incredible slow')
    #this is somehow not woking:
    if max_items<6000: # not working for huge sizes!
        a = timeit.timeit(performance_at_get_idx, number=repeat)
        print('Exectime time Anytree index access: {}'.format(a / repeat))
    else:
        print('Exectime time Anytree index access: not working')

except ImportError:
    pass