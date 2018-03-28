import random

SMALL_MIN = 0
SMALL_MAX = 9999

LARGE_MIN = 1000000
LARGE_MAX = 999999999

SMALL = True
LARGE = False

def unsorted_sample_data(n,small):
    a = []
    for i in range(n):
        if small:
            a.append(random.randint(SMALL_MIN,SMALL_MAX))
        else:
            a.append(random.randint(LARGE_MIN,LARGE_MAX))
    return a
    
def inverted_sample_data(n,small):
    a = unsorted_sample_data(n,small)
    a.sort(reverse=True)
    return a
    
def sorted_sample_data(n,small):
    a = unsorted_sample_data(n,small)
    a.sort()
    return a
    
def unsorted_small(n):
    return unsorted_sample_data(n,SMALL)

def unsorted_large(n):
    return unsorted_sample_data(n,LARGE)
    
def unsorted_mostly_small(n):
    return unsorted_sample_data(n-1,SMALL) + random.randint(LARGE_MIN,LARGE_MAX)
    
def unsorted_mostly_large(n):
    return unsorted_sample_data(n-1,LARGE) + random.randint(SMALL_MIN,SMALL_MAX)
    
def sorted_small(n):
    return sorted_sample_data(n,SMALL)
    
def sorted_large(n):
    return sorted_sample_data(n,LARGE)
    
def inverted_small(n):
    return inverted_sample_data(n,SMALL)
    
def inverted_large(n):
    return inverted_sample_data(n,LARGE)
    
    
# not needed right now, might be useful, i don't know
def scramble(array):
    newarray = []
    length = len(array)
    for i in range(length):
        print(str(i) + " " + str(length))
        newarray.append(array.pop(random.randint(0,length-i-1)))
    return newarray