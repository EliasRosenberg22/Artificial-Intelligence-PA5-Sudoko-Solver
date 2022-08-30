#Author: Elias Rosenberg
#Date: October 29th, 2021
#Purpose: Create a SAT to give the proper variable values to a Sudoku puzzle. Takes in a .cnf file where each line is a
#discrete conjunctive normal form claus. These CNFs are 'or' clauses, meaning any one value in the line evaluating to
#true yields a true assignment. This program loops through the lines in the CNF file and assigns each value to an Variable
#object, and stores those variables within a Clause object. Holds GSAT and WalkSAT algos to find a correct solution.

from cnf_var import *
from cnf_claus import *
import random
import copy

class SAT:
    def __init__(self, filename): #takes a filename with the cnf lines from Sudoku.py --> should take a .cnf file
        self.filename = filename
        self.claus_list = []
        self.tf = [True, False]
        self.var_list = []


    def create_cnf_list(self): #parses the cnf doc to get a list of clauses. Each claus is a list that holds variables that
        #are initially assigned None, and then true or false randomly with randomly_generate_assignmnet()
        with open(self.filename) as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip('\n')
                line = line.split(" ") #each variable is split within the whole clause by a space
                claus = Claus() #I know it's spelled "clause." I didn't realize until just now :( I'm not perfect
                for var in line:
                    variable = Variable(var, None)
                    #print(var)
                    claus.add_variable(variable)
                    self.var_list.append(var)
                self.claus_list.append(claus)

        return self.claus_list

    def is_satisfied(self, model): #if all the clauses in the model are True, then the assignment is valid
        for claus in model:
            if claus.assignment == False:
                return False
        return True

    def randomly_generate_assignment(self, model): #randomly assigns True or False to every var or claus in a blank assignment
        for claus in model: #randomly assigning variables
            for var in claus.var_list:
                var.assignment = self.give_assignment(var)

        for claus in model: #figuring out the resulting claus assignments
            for var in claus.var_list:
                if var.assignment == True:
                    claus.assignment = True
                else:
                    claus.assignment = False
        return model


    def rebuild_claus_assignments(self, model): #workaround for shallow copy problems. Checks if any new clauses are true and reassigns them accordingly.
        for claus in model:
            for var in claus.var_list:
                if var.assignment == True:
                    claus.assignment = True
                else:
                    claus.assignment = False
        return model

    def give_assignment(self, variable): #helper for above function. Just assigns a variable True or False
        variable.assignment = random.choice(self.tf)
        return variable.assignment

    def count_valid_clauses(self, model): #Counts the number of valid clauses in a model to help with GSAT
        count = 0
        for claus in model:
            if claus.assignment == True:
                count +=1

        return count

    def change_var_in_model(self, model, variable): #helper to loop through a model and change one variable's assignment.
        altered_model = copy.deepcopy(model)
        for i, claus in enumerate(model):
            for j, var in enumerate(claus.var_list):
                if altered_model[i].var_list[j].name == variable.name:
                    altered_model[i].var_list[j].flip()

        return altered_model


    def GSAT(self, list_of_clauses, max_flips, max_tries): #Meat of the program. Like backtracking, but flips truth values
        #of the variables in the model and counts which ones get the entire model to be valid.
        for i in range(0, max_tries):
            T = self.randomly_generate_assignment(list_of_clauses)
            for j in range(0, max_flips):
                #print(self.is_satisfied(T))
                if self.is_satisfied(T):
                    return T
                else:
                    P = self.optimal_model(T)
                    T = P

        print("No solution found")
        return

    def flip_variables(self, model): #goes through all the variables in GSAT and makes a new model with that variable assignment flipped. Very costly. If I had time, I'd go back and change my implementation to a list of lists of 1s and 0s.
        successors = {}
        for i, claus in enumerate(model):
            for j, var in enumerate(claus.var_list):
                new_model = copy.deepcopy(model)  # make a copy of the original assignment
                #print("original vals:" + str(new_model[i].var_list[j].assignment))
                new_model[i].var_list[j].flip()
                #print("new_vals:" + str(new_model[i].var_list[j].assignment))
                successors[var] = new_model  # add new assignment to successors
                successors[var] = self.rebuild_claus_assignments(successors[var])

        return successors

    def optimal_model(self, model): #goes through the models given by the function above to see which one has the most true clauses.
        satisfied = self.count_valid_clauses(model)
        successor_dict = self.flip_variables(model)
        best_model = None
        for var in successor_dict.keys():
            x = self.count_valid_clauses(successor_dict[var])
            if x > satisfied:
                satisfied = x
                best_model = successor_dict[var]

        return best_model

#___________________________________________________________________________________________________________________
    def WalkSAT(self, list_of_clauses, max_tries, max_flips, probability):
        for i in range(0, max_tries):
            T = self.randomly_generate_assignment(list_of_clauses)
            for j in range(0, max_flips):
                if self.is_satisfied(T):
                    return T
                else:
                    claus = self.random_claus(T)  # choose a random unsatisfied clause
                    n = uniform(0, 1)  # get a number between 0 and 1
                    if n < probability:  # if that number is less than the given probability value
                        successors = self.flip_variables_WalkSAT(T, claus)  # get random successor models
                        rand = random.choice(claus.var_list)
                        T = successors[rand] #choose a random model to reassign to T
                    else:
                        T = self.optimal_variable_WalkSAT(T, claus) #just choose the best model

        print("No solution found")
        return

    def random_claus(self, model): #finds a random unassigned claus within the given model
        options = []
        for claus in model: #may need to rebuild claus assignments here. We'll see
            if claus.assignment == False:  # add all unsatisfied clauses to a list
                options.append(claus)
        shuffle(options)  # pick one at random and return it
        random_c = options[0]
        return random_c


    def flip_variables_WalkSAT(self, model, claus): #returns the new models of just the variables in the chosen clause
        successors = {}
        for var in claus.var_list:
            successors[var] = self.change_var_in_model(model, var)

        return successors

    def optimal_variable_WalkSAT(self, model, claus): #chooses the best model from the models returned above
        satisfied = self.count_valid_clauses(model)
        # print(satisfied)
        successor_dict = self.flip_variables_WalkSAT(model, claus)
        best_model = None
        for var in successor_dict.keys():
            x = self.count_valid_clauses(successor_dict[var])
            if x > satisfied:
                satisfied = x
                best_model = successor_dict[var]

        return best_model

    # takes a new file name and the final assignment
    def final_file(self, file_name, model):
        file = open(file_name, "w")
        for claus in model:
            s = ""  # string for each claus
            for var in claus.var_list:
                if var.assignment == False:
                    s += "-"
                else:
                    s += str(var.name) + " "  #add each variable val to the claus line
            s += "\n" #once a claus is completed, go to the next line
            file.write(s)
        file.close()


if __name__ == '__main__':
    sat = SAT('/Users/eliasrosenberg/PycharmProjects/PA5/provided-3/one_cell.cnf')
    l = sat.create_cnf_list()
    x = sat.GSAT(l, 100, 3)
   # y = sat.WalkSAT(l, 50, 3, .3)

    #file = sat.final_file("test_res1", x)
    for c in x:
        list = []
        for v in c.var_list:
            list.append(str(v.name) + " " + str(v.assignment))
        print(list)


