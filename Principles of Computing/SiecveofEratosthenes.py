n = 100
numbers = range(2,n)
result = []

while numbers != []:
    result.append(numbers[0])
    numbers = [n for n in numbers if n % numbers[0] != 0]
    
print result
print len(result)

