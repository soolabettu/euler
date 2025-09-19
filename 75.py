

from collections import defaultdict

def solve(limit):
    my_dict = defaultdict(int)
    my_set = set()
    for i in range(1, limit):
        for j in range(i+1, limit+1):
            a = j ** 2 - i ** 2
            b = 2 * i * j
            c = i ** 2 + j ** 2
            my_set.add((a, b, c))
            
    for i in my_set:
        my_dict[i[0] + i[1] + i[2]] += 1
        
    count = sum(1 for v in my_dict.values() if v == 1)
    print(count)  # Outputs: 2
    
    
from mytimeit import MyTimer

with MyTimer() as t:
    solve(1_500_000)
            
    
            
