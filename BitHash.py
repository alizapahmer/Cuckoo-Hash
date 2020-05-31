
import random

# setup a list of random 64-bit values to be used by BitHash
__bits = [0] * (64*1024)
__rnd = random.Random()

# seed the generator to produce repeatable results
__rnd.seed("BitHash random numbers") 

# fill the list
for i in range(64*1024): 
    __bits[i] = __rnd.getrandbits(64)

# the parameter s is the string to hash.
# the parameter h is the starting "seed", usually defaults to 0
# See __main() below that shows how to re-hash a string s one or more times
def BitHash(s, h = 0):
    for c in s: 
        h  = (((h << 1) | (h >> 63)) ^ __bits[ord(c)]) 
        h &= 0xffffffffffffffff
    return h


def __main():
    while True:
        s = input("String to hash? ")
        
        # Show the result of hashing, and then re-hashing two more times
        ans = BitHash(s);       print("1st hash value for string %s: %016x" % (s, ans))
        ans = BitHash(s, ans);  print("2nd hash value for string %s: %016x" % (s, ans))   
        ans = BitHash(s, ans);  print("3rd hash value for string %s: %016x" % (s, ans))                
    
                        
if __name__ == '__main__':
    __main()       
                
                       

