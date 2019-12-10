# Your puzzle input is 197487-673251.

def match(password):
    passlist = [int(stringnumber) for stringnumber in str(password)]
    test = False
    for v, w in zip(passlist[:-1], passlist[1:]):
        if v == w:
            test = True
        if w < v:
            return False
    return test

def match2(password):
    passlist = [int(stringnumber) for stringnumber in str(password)]
    test = False
    for v, w in zip(passlist[:-1], passlist[1:]):
        if w < v:
            return False
    for index, number in enumerate(passlist):
        if index == 5:
            break
        if number == passlist[index + 1]:
            if index == 0:
                if passlist[index + 2] != number:
                    test = True
            elif index == 4:
                if passlist[index - 1] != number:
                    test = True
            elif (passlist[index -1] != number) & (passlist[index + 2] != number):
                test = True
    return test


a = 0
for i in range(197487, 673252):
    if match(i):
        a+=1
print(a)
b = 0
for i in range(197487, 673252):
    if match2(i):
        b+=1
print(b)