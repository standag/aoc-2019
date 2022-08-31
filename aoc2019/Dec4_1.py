
def has_two_same_number(number):
    numbers = [int(x) for x in str(number)]
    # part one
    # for i in range(len(numbers)-1):
    #     if numbers[i] == numbers[i+1]: return True
    for i in range(10):
        if numbers.count(i)==2: return True
    return False

def is_only_increasing(number):
    numbers = [int(x) for x in str(number)]
    for i in range(len(numbers)-1):
        if numbers[i] > numbers[i+1]: return False
    return True

passwords = []
for i in range(273025, 767253):
    if has_two_same_number(i) and is_only_increasing(i):
        passwords.append(i)

print(len(passwords))