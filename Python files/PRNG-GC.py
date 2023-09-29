import random

# Redefine the rand() and srand() functions using a linear congruential generator
RAND_LOCAL_MAX = 2147483647


#2063485727
def rand():
    global next
    next = (next * 1103515245 + 12345) % RAND_LOCAL_MAX
    return next
channel=[7,4,6,1,5,3,2,0,6,5]
# Usage exa


for i in range(2**30,2**32):
    found=[]
    next = i
    for j in range(len(channel)):
        if ((rand() % 8) != channel[j]):
            break
        else:
            found.append(channel[j])
            print(next)
    if len(found) ==len(channel):
        print("Got it")
        break




