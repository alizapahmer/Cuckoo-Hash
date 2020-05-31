import pytest
from BitHash import BitHash
import time 

#Create a Node class to hold each record's key and data 
class Node(object):
    def __init__(self, key,data):
        self.key = key
        self.data = data
        
        
class CuckooHash(object):
    def __init__(self, size):
        self.__numBuckets = size 
        self.__table1Count = 0             # keeps track of how many records are in each table 
        self.__table2Count = 0
        self.__hashArray1 = [None] * size
        self.__hashArray2 = [None] * size
        self.__prevReset = False           # Check if the bitHash has already been rehashed 
    
    
    # A function that generates two Hash Functions for each key. Gets a hashValue and
    # then mods the result to get a number within the size of the arrays 
    def __hash(self, key):
        Hash1 = BitHash(key,0) % self.__numBuckets
        Hash2 = BitHash(key, Hash1) % self.__numBuckets        
        return Hash1, Hash2 
    
    
    def insert(self,key, data, evictionCount = 0):   # evicitonCount keeps track of how many times a node has been kicked out of its spot
        
        # checks if the key is already there
        # if it's there, return False 
        if self.find(key):
            return False 
        
        # if either table gets too full, grow the size of the tables 
        # A table is considered too full when more than half of the table is filled 
        if self.__table1Count >= .5* self.__numBuckets or self.__table2Count >= .5* self.__numBuckets:
            self.growTable()
        
        # The function keeps track of how many times records have been kicked out of their spot 
        # if the cuckooHash gets stuck in a big loop of relocating data: 
        if evictionCount ==55:
            # if we have already reset the Hash Function due to an infinate loop, we grow the table and reset everything 
            if self.__prevReset == True:
                self.growTable()
                self.__prevReset == False            
            # if we have not yet tried reseting the Hash Fuction, reset it and try again 
            else: 
                self.resetHash()
            # set the loop tracker back to zero 
            evictionCount = 0
        
        # ACTUAL INSERT HAPPENS NOW: 
        
        # Create a node and get the hash values for the key
        node = Node(key,data)
        Hash1, Hash2 = self.__hash(key)
        
        # check the first hash value, if the spot is empty, insert it with no problem 
        # increment the table count for table one 
        if self.__hashArray1[Hash1] == None: 
            self.__hashArray1[Hash1] = node
            self.__table1Count +=1
            
        # if something was in the spot in table one:
        else:
            # save the node that was there and then insert the new data into that spot 
            oldNode = self.__hashArray1[Hash1]
            self.__hashArray1[Hash1] = node

            # try to insert the old key into the second hash table using the second hash function for that key
            # if the spot is empty, insert it and increment the record count for table 2  
            newHash1, newHash2 = self.__hash(oldNode.key)
            if self.__hashArray2[newHash2] == None:
                self.__hashArray2[newHash2] = oldNode
                self.__table2Count+=1
           
            # if something was occupying the spot on the second table 
            # save the node that was there and then insert the new data into that spot
            # recursively call the insert method on the old node until it can be successfully inserted 
            # keep track of this eviction loop to prevent a potential infinate loop 
            else:
                temp = self.__hashArray2[newHash2]
                self.__hashArray2[newHash2] = oldNode 
                self.insert(temp.key, temp.data, evictionCount+1) 
                
                
    # function to reset the BitHash to use a different Hash function
    def resetHash(self): 
        ResetBitHash()
        # store the old tables in temp values and reset the tables
        temp1 = self.__hashArray1 
        temp2 = self.__hashArray2 
        self.__hashArray1 = [None] * self.__numBuckets
        self.__hashArray2 = [None] * self.__numBuckets 
        # loop through the old tables and rehash and insert all the records using the new hash Function into the hashTables
        for i in range(len(temp1)):
            if temp1[i]:
                self.__insert(temp1[i].__key,temp1[i].data)
        for i in range(len(temp2)):
            if temp2[i]:
                self.__insert(temp2[i].__key, temp2[i].data)
        
        
    # function to double the size of the Hash tables 
    def growTable(self): 
        self.__numBuckets = self.__numBuckets * 2
        # store the old tables in temp values and reset the tables to the new size
        temp1 = self.__hashArray1 
        temp2 = self.__hashArray2 
        self.__hashArray1 = [None] * self.__numBuckets
        self.__hashArray2 = [None] * self.__numBuckets 
        # loop through the old tables and insert all the records into their new places in the hash table 
        for i in range(len(temp1)):
            if temp1[i]:
                self.insert(temp1[i].key,temp1[i].data)
        for i in range(len(temp2)):
            if temp2[i]:
                self.insert(temp2[i].key, temp2[i].data)  
            
            
    # check if a key has been inserted
    # hash the key and check only the relevant spot at each table for that key
    # if the key is there, returns the data 
    def find(self, key):
        Hash1, Hash2 = self.__hash(key)
        if self.__hashArray1[Hash1] and self.__hashArray1[Hash1].key == key:
            return self.__hashArray1[Hash1].data
        if self.__hashArray2[Hash2] and self.__hashArray2[Hash2].key == key:
            return self.__hashArray2[Hash2].data
        return None
    
    # hash the key and check the relevant spot at each table 
    # if the key is there, delete the node from the hash Table 
    def delete(self, key):
        Hash1, Hash2 = self.__hash(key)
        if self.__hashArray1[Hash1] and self.__hashArray1[Hash1].key == key:
            self.__hashArray1[Hash1] = None
        if self.__hashArray2[Hash2] and self.__hashArray2[Hash2].key == key:
            self.__hashArray2[Hash2] = None
            

