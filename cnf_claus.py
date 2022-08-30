#Author: Elias Rosenberg
#Date: October 29th, 2021
#Purpose: Create a claus object that holds a list of cnf_variable objects. Has methods that loop through the variable
#vals held within the claus list and returns whether the claus is true or not. We can then hold a list of clauses when
#running the SAT code to check and see if they're all True.

class Claus:
    def __init__(self):
        self.var_list = [] #list of all variables within this claus
        self.assignment = None
        self.var_names = []

    def add_variable(self, new_variable):
        self.var_list.append(new_variable) #add the new variable to the list
        self.var_names.append(new_variable.name)

    def set_assignment(self): #sets this objects boolean value depending on the values of its variables
        for var in self.var_list:
            if var.assignment == True:
                self.assignment = True
        self.assignment = False

        return self.assignment


    def most_truth_values(self): #need some clever way to see the best variable to switch variables to --> step 'P' in algorithm
        pass

    def __str__(self):
        print(self.var_names)
