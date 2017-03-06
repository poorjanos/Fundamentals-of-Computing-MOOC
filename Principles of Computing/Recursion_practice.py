def triangular_sum(n):
    """
    Example of a recursive function that computes
    a triangular sum
    """
    if n == 0:
        return 0
    else:
        return n + triangular_sum(n-1)
    
    
#print triangular_sum(3)


def number_of_threes(n, count):
    """
    Takes a non-negative integer num and compute the 
    number of threes in its decimal form
    Returns an integer
    """
    str_n = str(n)
    if len(str_n) == 1 and str_n == "3":
        count += 1
        return count
    elif len(str_n) == 1 and str_n != "3":
        return count
    elif str_n[0] == "3":
        return number_of_threes(str_n[1:], count + 1)
    elif str_n[0] != "3":
        return number_of_threes(str_n[1:], count)
    
#print number_of_threes(34545633334, 0)

def number_of_threes1(string):
    for char in string:
        res = n3(string[1:])
        if char == "3":
            res += 1
        return res
    return 0


def number_of_threes2(num):
    """
    Takes a non-negative integer num and computes the 
    number of threes in its decimal form
    Returns an integer
    """
    if num == 0:
        return 0
    else:
        unit_digit = num % 10
        threes_in_rest = number_of_threes2(num // 10)
        if unit_digit == 3:
            return threes_in_rest + 1
        else:
            return threes_in_rest
    
#print number_of_threes(323)




def is_member(mylist, elem):
    """
    Take list my_list and determines whether elem is in my_list
    Returns True or False
    """
    if mylist == []:
        return False
    else:
        if mylist[0] == elem:
            return True
        else:
            return is_member(mylist[1:], elem)
        
#print is_member(['c', 'b', 't'], 'a')



def remove_x(my_string):
    """
    Takes a string my_string and removes all instances of
    the character 'x' from the string
    Returns a string
    """
    if my_string == "":
        return ""
    else:
        first_chr = my_string[0]
        rest_removed = remove_x(my_string[1:])
        if first_chr != 'x':
            return first_chr + rest_removed
        else:
            return rest_removed 
    
#print remove_x("catxxdogx")



def insert_x(my_string):
    """
    Takes a string my_string and add the character 'x'
    between all pairs of adjacent characters in my_string
    Returns a string
    """
    if my_string == "":
        return ""
    else:
        if len(my_string) == 1:
            first_chr = my_string[0]
        else:
            first_chr = my_string[0] + 'x'
        rest = insert_x(my_string[1:])
        return first_chr + rest
            
#print insert_x("cato")



def insert_x2(my_string):
    """
    Takes a string my_string and add the character 'x'
    between all pairs of adjacent characters in my_string
    Returns a string
    """
    if len(my_string) <= 1:
        return my_string
    else:
        first_character = my_string[0]
        rest_inserted = insert_x(my_string[1 :])
        return first_character + 'x' + rest_inserted

#print insert_x("cato")



def list_reverse(my_list):
    """
    Takes a list my_list and returns new list
    whose elements are in reverse order
    Returns a list
    """
    if my_list == []:
        return []
    else:
        elem = my_list[0]
        rest = list_reverse(my_list[1:])
        return rest + [elem]
              
#print list_reverse([1,2,3,5,4])



def gcd(num1, num2):
    """
    Euclid's Algorithm: handling of num1 = 0 or num2 = 0 is the key
    Takes non-negative integers num1 and num2 and
    returns the greatest common divisor of these numbers
    """
    if num2 > num1:
        return gcd(num2, num1)
    else:
        if num2 == 0:
            return num1
        else:
            return gcd(num1 - num2, num2)
        
#print gcd(3, 0)



def slice(my_list, first, last):
    if my_list == []:
        return []
    else:
        elem_idx = len(my_list) - 1
        elem = my_list.pop()
        rest = slice(my_list, first, last)
        if first <= elem_idx <= last:
            return rest + [elem]
        else:
            return rest
        
        
#print slice(['a', 'b', 'c'], 0, 1)




def slice2(my_list, first, last):
    """
    Takes a list my_list and non-negative integer indices
    satisfying 0 <= first <= last <= len(my_list)
    Returns the slice my_list[first : last]
    """
    if my_list == []:
        return []
    else:
        first_elem = my_list.pop(0)
        if first > 0:  
            rest_sliced = slice(my_list, first - 1, last - 1)
            return rest_sliced
        elif last > 0:
            rest_sliced = slice(my_list, 0, last - 1)
            return [first_elem] + rest_sliced
        else:
            return []
        
print slice2([1, 2, 3], 1, 2)




