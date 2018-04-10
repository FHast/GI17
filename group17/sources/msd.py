'''
Created on Apr 3, 2018

@author: gereon
'''

import math
from time import clock
import random


def lsd_radix(data, base=10):
    position = int(math.ceil(math.log(max(data), 10))) - 1
    for i in range(position + 1):
        buckets = [[] for _ in range(base)]
        for x in data:
            buckets[(x % pow(base, i + 1)) // pow(base, i)].append(x)
            
        data = []
        for b in buckets:
            data += b
            
    return data


def msd_radix(data, base=10):
    position = int(math.ceil(math.log(max(data), 10))) - 1
    return rec(data, position, base)
    

def rec(data, position, base):
    if data == [] or len(data) == 1: return data
    buckets = [[] for _ in range(base)]
    for x in data:
        buckets[(x % pow(base, position + 1)) // pow(base, position)].append(x)

    result = []
    for b in buckets:
        if position != 0:
            b = rec(b, position - 1, base)
        result += b
        
    return result


def test_msd(amount, max, print_flag=False):
    sample = []
    for x in range(amount):
        sample.append(random.randint(0, max))
    t1 = clock()
    if print_flag:
        print(msd_radix(sample, 10))
    else:
        msd_radix(sample, 10)
    t2 = clock()
    print(t2 - t1)

    
def test_lsd(amount, max, print_flag=False):
    sample = []
    for x in range(amount):
        sample.append(random.randint(0, max))
    t1 = clock()
    if print_flag:
        print(lsd_radix(sample, 10))
    else:
        lsd_radix(sample, 10)
    t2 = clock()
    print(t2 - t1)

    
test_msd(pow(10,5), 10000)
test_lsd(pow(10,5), 10000)
