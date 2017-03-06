#permutations
#iterative
def perms(word):
    stack = list(word)
    results = [stack.pop()]
    while len(stack) != 0:
        c = stack.pop()
        new_results = []
        for w in results:
            for i in range(len(w)+1):
                new_results.append(w[:i] + c + w[i:])
        results = new_results
    return results

#recursive with generator
def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]


#print perms('abc')           
#for i in all_perms(['a','b','c']):
#    print i
    
    
#power set string recursive  
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
               
print gen_all_strings('aab')



#power set string recursive alternative
def gen_all_strings2(word):
    '''
    generate (function shall be recursive!) all strings that can be composed
    from the letters in word in any order;
    returns a list of all strings that can be formed from the letters in word
    '''
    # base case; no string
    if not word:
        return ['']
    
    possibilities = []
    # generate all appropriate strings for rest of the word
    for string in gen_all_strings2(word[1:]):
        for index in range(len(string) + 1):
            # inserting the initial character in all possible positions within the string
            possibilities.append(string[:index] + word[0] + string[index:])
            
    return gen_all_strings2(word[1:]) + possibilities



#power set list recursive
def power_set_recur(mylist):
    if mylist == []:
        return [[]]
    else:
        rest_strings = power_set_recur(mylist[1:])
        temp = rest_strings[:]
        for item in temp:
            for letter in range(len(item) + 1):
                rest_strings.append(item[:letter] + mylist[:1] + item[letter:])
        return rest_strings
               
#print power_set_recur([1,1]) 


#power set iterative
def list_powerset(lst):
    # the power set of the empty set has one element, the empty set
    result = [[]]
    for x in lst:
        # for every additional element in our set
        # the power set consists of the subsets that don't
        # contain this element (just take the previous power set)
        # plus the subsets that do contain the element (use list
        # comprehension to add [x] onto everything in the
        # previous power set)
        result.extend([subset + [x] for subset in result])
    return result
 
#power set iterative in one statement
def list_powerset2(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    