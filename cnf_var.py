#Author: Elias Rosenberg
#Date: October 29th, 2021
#Purpose: Create a cnf variable object that holds the value/name of the variable and the boolean value. Has a helper
#method called 'flip' that changes the value of the boolean. Count int holds the number of flips.

from random import *

class Variable:
    def __init__(self, name, assignment):
        self.assignment = assignment #boolean that holds whether the variable is true or false
        self.name = name #whatever value this variable holds --> '111' , '112' etc in this case.
        self.flip_count = 0 #number of times this variable has been flipped
        self.tf = [True, False]



    def return_value(self):
        print(str(self.name) + "is currently assigned to: " + str(self.assignment))

    def flip(self): #switches the boolean value that is currently assigned to this variable
        if self.assignment == True:
            self.assignment = False
            self.flip_count += 1

        elif self.assignment == False:
            self.assignment = True
            self.flip_count += 1

    def __str__(self):
        print(self.name)