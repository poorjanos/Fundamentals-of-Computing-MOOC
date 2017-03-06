"""
Student code for Word Wrangler game
"""
import math
import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(180)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    This function can be iterative.
    """
    return [list1[idx]for idx in range(len(list1))
            if idx == len(list1)-1 or list1[idx] != list1[idx +1]]

def remove_duplicates2(list1):
    """
    Eliminate duplicates in a sorted list.
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    This function can be iterative.
    """
    screened = []
    for item in list1:
        if item not in screened:
            screened.append(item)
    return screened


#forum version
def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    # Determine if using linear or binary search is faster
    if len(list1)==0 or len(list2)==0:
        return []
    len1,len2=len(list1),len(list2)
    if len2*math.log(len1,2)<len1:
        return intersect_binary(list1,list2,len1)
    else:
        answer=[]
        for item in list1:
            if item in list2 and item not in answer:
                answer.append(item)
        return answer

def intersect_binary(list1,list2,len1):
    """
    Helper function for binary search
    """
    answer=[]
    for item in list2:
        if iter_binary_search(list1,0, len1, item):
            answer.append(item)
    return answer

def iter_binary_search(ordered_list, lower, upper, item):
    """
    Iterative version of binary search
    Test whether item is in ordered_list[lower:upper]
    """
    
    while lower + 1 < upper:
        mid = (lower + upper) / 2        
        if item < ordered_list[mid]:
            upper = mid
        else:
            lower = mid            
    return item == ordered_list[lower]

#own version
def intersect2(list1, list2):
    """
    Compute the intersection of two sorted lists.
    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    This function can be iterative.
    """
    screened = []
    for item in list1:
        if item not in screened and item in list2:
            screened.append(item)
    return screened


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.
    Returns a new sorted list containing those elements that are in
    either list1 or list2.
    This function can be iterative.
    """   
    l1 = list1[:]
    l2 = list2[:]
    
    merged = []
    
    while l1 and l2:
        if l1[0] < l2[0]:
            merged.append(l1.pop(0))
        elif l1[0] >= l2[0]:
            merged.append(l2.pop(0))
            
    if l1:
        merged += l1
    else:
        merged += l2
    
    return merged 
    
 
                
def merge_sort(list1):
    """
    Sort the elements of list1.
    Return a new sorted list with the same elements as list1.
    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    # finding midsection of the list
    half = len(list1) / 2
    return merge(merge_sort(list1[:half]), merge_sort(list1[half:])) 

# Function to generate all strings for the word wrangler game


def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.
    Returns a list of all strings that can be formed from the letters
    in word.
    This function should be recursive.
    """
    if word == "":
        return [""]
    else:
        rest_strings = gen_all_strings(word[1:])
        temp = rest_strings[:]
        for item in temp:
            for letter in range(len(item) + 1):
                rest_strings.append(item[:letter] + word[:1] + item[letter:])
        return rest_strings
    
# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.
    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    return [word[:-1] for word in netfile]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    