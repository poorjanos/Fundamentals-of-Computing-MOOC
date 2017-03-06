"""
Merge function for 2048 game.
"""

def merge(line):
#Three list implementation of merge function   
    result = [0 for idx in range(len(line))]
    
    out_idx = 0
    for idx in range(len(line)):
        if line[idx] != 0:
            result[out_idx] = line[idx]
            out_idx += 1
    
    result2 = list(result)
    
    for idx in range(len(result)):
        if idx < len(result)-1:
            if result[idx] == result[idx+1] and result2[idx] != 0:
                result2[idx] = result[idx] + result[idx+1]
                result2[idx+1] = 0

    result3 = [0 for i in range(len(line))]
    
    out_idx = 0
    for idx in range(len(result2)):
        if result2[idx] != 0:
            result3[out_idx] = result2[idx]
            out_idx += 1
    
    return result3

#alternative solutions##

#pairwise iteration:
def merge2(nums):
    prev = None
    store = []

    for next_ in nums:
        if not next_:
            continue
        if prev is None:
            prev = next_
        elif prev == next_:
            store.append(prev + next_)
            prev = None
        else:
            store.append(prev)
            prev = next_
    if prev is not None:
        store.append(prev)
    store.extend([0] * (len(nums) - len(store)))
    return store

#while loop
def merge3(nums):
  res = [value for value in nums if value != 0]
  i = 0
  while (i < len(res)-1 ):
    if (res[i]==res[i+1]): # if a number is the same as the following
      res[i] *= 2          # double it 
      del res[i+1]         # remove the following
    i += 1
  res.extend([0] * (len(nums)-len(res)))
  return res



#testing
print 'Computed: ', merge([2, 0, 2, 4]), 'Expected: [4, 4, 0, 0]'
print 'Computed: ', merge([0, 0, 2, 2]), 'Expected: [4, 0, 0, 0]'
print 'Computed: ', merge([2, 2, 0, 0]), 'Expected: [4, 0, 0, 0]'
print 'Computed: ', merge([2, 2, 2, 2, 2]), 'Expected: [4, 4, 2, 0, 0]'
print 'Computed: ', merge([8, 16, 16, 8]), 'Expected: [8, 32, 8, 0]'