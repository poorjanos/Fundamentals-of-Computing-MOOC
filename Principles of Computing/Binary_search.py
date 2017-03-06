#binary search - returns True or False
def binary_search(ordered_list, k):
    if len(ordered_list) == 0:
        return False
    else:
        mid = len(ordered_list)//2
        if ordered_list[mid] == k:
            return True
        else:
            if ordered_list[mid] < k:
                return binary_search(ordered_list[mid:], k)
            elif ordered_list[mid] > k:
                return binary_search(ordered_list[:mid], k)
                       
#binary search - returns index             
def binary_search_i(l, value, low = 0, high = -1):
    if not l:
        return -1
    if high == -1:
        high = len(l)-1
    if low >= high:
        if l[low] == value:
            return low
        else:
            return -1
    mid = (low+high)//2
    if l[mid] > value:
        return binary_search_i(l, value, low, mid-1)
    elif l[mid] < value:
        return binary_search_i(l, value, mid+1, high)
    else:
        return mid   

print binary_search(range(5), 4)
print binary_search_i(range(5), 4, 0, 4)