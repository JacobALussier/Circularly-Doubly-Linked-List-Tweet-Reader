''' Assignment 2
Making a tweet reader using a linked list as backing data structure
11/26/19
Author: Jacob Lussier'''

import re
import sys

class CDLLNode:
    def __init__(self, time="", tweet="", next_node=None, prev_node=None):
        self.time: str = time
        self.tweet: str = tweet
        self.next_node: CDLLNode = next_node
        self.prev_node: CDLLNode = prev_node

class CDLL:
    def __init__(self):
        self.head: CDLLNode = None
        self.current: CDLLNode = None
        self.numnodes: int = 0
    
    # makes an insertion based on the 'current' node
    def insert(self,time: str, tweet: str):
        newNode = CDLLNode(time,tweet) # Initialize the new node being inserted
        saveTime = time 
         
        if self.head == None: # If the list is empty
            self.head = newNode
            self.current = self.head
            self.numnodes += 1
            newNode.next_node = self.head
            newNode.prev_node = self.head
        elif self.numnodes == 1: # If one node is already in the list
            
            if saveTime > self.current.time: # If time is greater than time of the single node in the list
                newNode.next_node = self.head
                newNode.prev_node = self.head
                self.head.next_node = newNode
                self.head.prev_node = newNode
                self.numnodes +=1
                
                
                
            else: # If time is less than time of the single node in the list
                newNode.next_node = self.head
                newNode.prev_node = self.head
                self.head.prev_node = newNode
                self.head.next_node = newNode
                self.head = newNode
                self.numnodes +=1
                self.current = self.head
        else: # If more than one node is in the list
            self.go_first()
            
            if self.current.time >= saveTime: # Check if time is less than head
                self.go_last()
                self.current.next_node = newNode
                newNode.prev_node = self.current
                self.head.prev_node = newNode
                newNode.next_node = self.head
            
                self.head = newNode
                self.numnodes +=1
                self.current = self.head
            else: # If time is not less than head
                while saveTime > self.current.time and self.current.next_node != self.head: # Loop through the list looking for a  node time greater than new time
                    self.go_next()
                    
                if saveTime > self.current.time and self.current.next_node == self.head: # Check if node should be inserted at end of list
                    self.current.next_node = newNode
                    self.head.prev_node = newNode
                    newNode.next_node = self.head
                    newNode.prev_node = self.current
                    self.numnodes += 1

                else: # Basic insertion between two nodes

                    newNode.next_node = self.current
                    newNode.prev_node = self.current.prev_node
                    self.current.prev_node.next_node = newNode
                    self.current.prev_node = newNode
                    self.numnodes += 1
        self.current = self.head
                    
        return
        

    # moves 'current' pointer to the next node (circularly)
    def go_next(self):
        if self.head == None:
            return
        else:
            self.current = self.current.next_node
        
        return 


    # moves 'current' pointer to the previous node (circularly)
    def go_prev(self):
        if self.head == None:
            return
        elif self.current == self.head:
            while self.current.next_node != self.head and self.current.next_node != None:
                self.go_next()
            
        else:
            self.current = self.current.prev_node
        
        return
        

    # moves 'current' pointer to the head (the first node)
    def go_first(self):
        if self.head == None:
            return
        else:
            self.current = self.head

    # moves 'current' pointer to the last node
    def go_last(self):
        if self.head == None:
            return
        else:
           self.current = self.head.prev_node
        return

    # moves 'current' pointer n elements ahead (circularly)
    def skip(self,n:int):
        if n >= self.numnodes:
            n = n % self.numnodes # mod to keep the number in range of numnodes
        for i in range(n):
            self.go_next()

    # prints the contents of the 'current' node
    # prints the time, then the tweet (each with a newline following)
    def print_current(self):
        if self.head == None:
            return
        else:
            print(self.current.time)
            print(self.current.tweet)


def main():
    
    tList = CDLL() #Create a new doubly linked list called "tweet list" or tList
    filename = sys.argv[1] # take the file as command line input
    openFile = open(filename,"r",encoding="utf8")
    for line in openFile:
        line = line.strip()
        tweetId,time,tweet = line.split("|") # separate the line into three variables
        saveTime = time[11:19] # get the military time 
        tList.insert(saveTime,tweet) # insert the tweet with the military time and tweet as parameters 
    
    tList.go_first()
    tList.print_current() # print the head                           
    openFile.close()

  
    userCommand = ""
    over = False
    while over != True : # loop to get user input and perform appropriate tasks
        userCommand = input()
        if userCommand == "n":
            tList.go_next()
            tList.print_current()
        elif userCommand == "f":
            tList.go_first()
            tList.print_current()
        elif userCommand == "l":
            tList.go_last()
            tList.print_current()
        elif userCommand == "p":
            tList.go_prev()
            tList.print_current()
        elif userCommand == "num":
            print(tList.numnodes)
        elif userCommand.isdigit() == True: # is digit checks if the user enters a number
            tList.skip(int(userCommand))
            tList.print_current()
        elif bool(re.match("s \w",userCommand)): # utilize the re class to check if user's input match specified pattern
            
            realWord = userCommand.strip("s ").lower() # strip the s and space of the word so we can search for it

            for i in range(tList.numnodes):
                if realWord in (tList.current.tweet).lower(): # if found print it 
                    tList.print_current()
                    return
                else:
                    tList.go_next()
            return
        
        elif userCommand == "q": # quit if q is entered
            over = True
        else:
            print("Command not found (Options: n,f,l,p,<num>,s <word>, q)") # if wrong command entered tell the user
        
        
            
        
            
            


if __name__ == "__main__":
    main()
