import pytest 
from CuckooHash import CuckooHash  
import time 

# *************PYTEST*************************
# ********************************************

# successfully insert 100 unique words from a file
def test__SuccessfulFind():               
    c = CuckooHash(400)
    file = open("wordlist.txt")
    word = file.readline()
    for i in range(100):
        c.insert(word, i)
        word = file.readline()
    file.close()  
    file = open("wordlist.txt")
    word = file.readline()
    for i in range(100):
        assert c.find(word) != None       # Successfully find all the words. If a word returns none then it didn't find it
        assert c.find(word) == i          # returns the proper data for the key 
        word = file.readline()     
    file.close()

# Don't allow inserting a word that is already in the table   
def test__insertDouble():      
    c = CuckooHash(100)
    c.insert("DoubleWord", 234)
    c.insert("word1", 1)
    c.insert("word2", 2)
    c.insert("word3", 3)
    assert c.insert("DoubleWord",234) == False 

# Forces the table to grow by inserting many words from a file    
def test__insertMany():                    
    c = CuckooHash(300)
    file = open("wordlist.txt")
    word = file.readline()
    for i in range(580):
        c.insert(word, 2)
        word = file.readline()
    file.close()      
    file = open("wordlist.txt")          # asserts that all the data was successfully inserted and the table was properly grown  
    word = file.readline()
    for i in range(400):
        assert c.find(word) != None 
        word = file.readline() 
    file.close()

# No word was inserted, empty CuckooHash should fail to find anything  
def test__findFail():
    c = CuckooHash(100)
    assert c.find("Cuckoo") == None    

# insert a key and then delete it. Should not be able to find it in the table anymore 
def test__delete():
    c = CuckooHash(100)
    c.insert("toDelete", 44)
    c.delete("toDelete")
    assert c.find("toDelete") == None  

# No error occurs when deleting a key that isn't there 
def test__deleteFalseKey():
    c = CuckooHash(20)
    assert c.delete("Delete") == None

# insert keys then delete one. Try reinserting the key and if it was properly deleted,
# the insertion should be successful 
def test__deleteFromTable():               
    c = CuckooHash(400)
    c.insert("a",1)
    c.insert("b",2)
    c.insert("c",3)
    c.insert("d",4)
    c.insert("e",5)
    c.insert("f",6)
    c.insert("g",7)
    c.insert("h",8)
    c.insert("i",9)
    c.delete("e") 
    assert c.insert("e",5) != False  
    assert c.find("e") == 5 
    
# Check if the find time is around the same regardless of how many records in the tables
def test__Findtime():
    
    # Calculate how long it takes to find 100 records in an hash table that only has 100 records in it 
    h = CuckooHash(1000)
    file = open("wordlist.txt")
    word = file.readline()
    
    # insert 100 words from a file
    for i in range(100):
        h.insert(word, 2)
        word = file.readline()
    file.close() 
    file = open("wordlist.txt")
    word = file.readline()
    
    # time how long it takes to find those 100 words
    tm = time.time()
    for i in range(100):
        h.find(word)    
    tm = time.time() - tm   
    file.close()
    # ----------------------------------------
    # calculate how long it takes to find 100 records in a hashTable with 300 records 
    c = CuckooHash(1000)
    file = open("wordlist.txt")
    word = file.readline()
    
    # insert 300 records from a file
    for i in range(300):
        c.insert(word, 2)
        word = file.readline()
    file.close() 
    
    # Want it to find a different 100 words than the first time, 
    # So read some words first
    file = open("wordlist.txt")
    word = file.readline()
    for i in range(150):
        word = file.readline()
    
    # time how long it takes to find 100 words
    t = time.time()
    for i in range(100):
        c.find(word)
        word = file.readline()
    t = time.time() - t
    file.close()
    # -------------------------------------------------
    # calculate how long it takes to find 100 records in a hashTable with 800 records 
    ck = CuckooHash(1000)
    file = open("wordlist.txt")
    word = file.readline()
    
    # insert 800 words from a file 
    for i in range (800):
        ck.insert(word, 2)
        word = file.readline()
    file.close() 
    
    # Want it to find a different 100 words than the other time
    # So read in some words first 
    file = open("wordlist.txt")
    word = file.readline()
    for i in range(300):
        word = file.readline()    
    
    # time how long it takes to find 100 words 
    s = time.time()
    for i in range(100):
        ck.find(word)
        word = file.readline()
    s = time.time() - s
    file.close()
    
    
    # Check if the times for find on the different tables sizes are the same or  
    # within a 20 percent acceptable difference 
    assert abs(t-s) <= t* 0.2 
    assert abs(s-tm) <= s* 0.2
    assert abs(t-tm) <= t* 0.2

pytest.main(["-v"])

