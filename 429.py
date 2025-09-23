i = 90
j = 3
check_str = "123"
k = 1
limit = 678910
n = 13
p = int(str(2**90)[:n])
p196 = int(str(2**196)[:n])
p289 = int(str(2**289)[:n])
p485 = int(str(2**485)[:n])


while k < limit:
    if str(p*p196)[:j] == check_str:
        i = i + 196
        p = int(str(p*p196)[:n])
       
    elif str(p*p289)[:j] == check_str:
        i = i + 289
        p = int(str(p*p289)[:n])
        
    elif str(p*p485)[:j] == check_str:
        i = i + 485
        p = int(str(p*p485)[:n])
        
    k = k + 1
