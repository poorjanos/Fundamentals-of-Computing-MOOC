'''
All sorts of sorts
http://interactivepython.org/runestone/static/pythonds/SortSearch/toctree.html
'''
l = [54,26,93,17,77,31,44,55,20]

### Naive quadratic sort (Rice Algorithmic Thinking)
def naive_quadratic_sort(alist):
    '''
    O(n2) and not memory efficient since produces extra list for output (not in-place)
    Logic similar to selection sort
    '''
    l = alist[:]
    ans = []
    for passnum in range(len(alist)):
        m = float('inf')
        for i in range(len(l)):
             if l[i] < m:
                 m = l[i]
        l.pop(l.index(m))
        ans.append(m)
    return ans



### Bubble sort
def bubble(alist):
    '''
    The bubble sort makes multiple passes through a list. It compares adjacent
    items and exchanges those that are out of order. Each pass through the list
    places the next largest value in its proper place. In essence, each item
    “bubbles” up to the location where it belongs.
    '''
    #n-1 passes since n-1 comparisons needed
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            temp = 0
            if alist[i] > alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp
    return alist
                
#print bubble(l)

def bubbleshort(alist):
    passnum = len(alist)-1
    exchange = True
    while passnum > 0 and exchange:
        exchange = False
        for i in range(passnum):
            temp = 0
            if alist[i] > alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp
                exchange = True
        passnum -= 1
    return alist

#print bubbleshort(l)
#print counter1

# Selection sort
def selection(alist):
    '''
    The selection sort improves on the bubble sort by making only one exchange
    for every pass through the list. In order to do this, a selection sort
    looks for the largest value as it makes a pass and, after completing the
    pass, places it in the proper location. As with a bubble sort, after the
    first pass, the largest item is in the correct place. After the second
    pass, the next largest is in place. This process continues and requires
    n−1 passes to sort n items, since the final item must be in place after
    the (n−1)st pass.
    '''
    for passnum in range(len(alist)-1,0,-1):
        max_val = -float('Inf')
        max_idx = 0
        for i in range(passnum + 1):
            if alist[i] > max_val:
                max_val = alist[i]
                max_idx = i
        temp = alist[passnum]
        alist[passnum] = alist[max_idx]
        alist[max_idx] = temp
    return alist


#same with fewer lines
def selection2(alist):
    for passnum in range(len(alist)-1,0,-1):
        max_idx = 0
        #range(1, passnum + 1) could be range(passnum + 1): this way one iter less
        for i in range(1, passnum + 1):
            if alist[i] > alist[max_idx]:
                max_idx = i
        temp = alist[passnum]
        alist[passnum] = alist[max_idx]
        alist[max_idx] = temp
    return alist

#same looking for the min
def selection3(alist):
    for passnum in range(0, len(alist)-1):
        min_idx = len(alist)-1
        #range(passnum, len(alist)-1) could be range(passnum, len(alist)): this way one iter less
        for i in range(passnum, len(alist)-1):
            if alist[i] < alist[min_idx]:
                min_idx = i
        temp = alist[passnum]
        alist[passnum] = alist[min_idx]
        alist[min_idx] = temp
    return alist



#print selection3(l)


# Insertion sort
def insertion(alist):
    '''
    The insertion sort, although still O(n2), works in a slightly different
    way. It always maintains a sorted sublist in the lower positions of the
    list. Each new item is then “inserted” back into the previous sublist such
    that the sorted sublist is one item larger.
    '''
    for index in range(1,len(alist)):
        currentvalue = alist[index]
        position = index
        
        # Iterate over sublist and move values to the right until current value
        # reaches the insertion point
        while position > 0 and alist[position-1] > currentvalue:
            alist[position] = alist[position-1]
            position = position - 1
        
        # Insert current value to right place (position is now looped to right index)
        alist[position] = currentvalue
    return alist
    

#print insertion(l)















