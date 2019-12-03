from numpy import random
import numpy as np
import pandas as pd
from numpy.random import choice

#import matplotlib.pyplot

DATA = pd.DataFrame(columns = ['Results'])



'''class: A blueprint created by a programmer for an object. 
This defines a set of attributes that will characterize any object that is instantiated from this class'''

#define function for employees  
class Employee: #Creating a prototype, which has certain function related to it 
    def __init__(self, gender): #_init_ is known as a constructor in object oriented concepts: An object is created from the class and it allow the class to initialize the attributes of a class.
        self.gender = gender #self represents the instance of the class. By using the "self" keyword we can access the attributes and methods of the class in python
        self.rating = 10.0
        self.employee_position = "employee"


class Result:
    """Result has two attributes, men and women. Each are an array of length levels where each element is the count of gender at the indexed level"""
    def __init__(self,men,women):
        self.men = men
        self.women = women
        

class Simulation:
#attrition: the ones who quit
#num_simulation: 10
#iterations_per_simulation: 2
#promotion_bias: our gender bias --> 0.00004
#num_positions_at_level: number of employees per level (a list)
#bias_favors_this_gender: males
    def __init__(self, num_simulations, attrition, iterations_per_simulation, promotion_bias_FF, promotion_bias_FM, promotion_bias_MM, promotion_bias_MF,  
        num_positions_at_level):
        self.num_simulations = num_simulations
        self.attrition = attrition
        self.iterations_per_simulation = iterations_per_simulation
        self.promotion_bias_FF = promotion_bias_FF
        self.promotion_bias_FM = promotion_bias_FM
        self.promotion_bias_MM = promotion_bias_MM
        self.promotion_bias_MF = promotion_bias_MF
        self.num_positions_at_level = num_positions_at_level
        #self.bias_favors_this_gender = bias_favors_this_gender
        self.num_employee_levels = len(num_positions_at_level)

        self.init_employees()
        self.hire() 

    def init_employees(self):
        """Build up mapping of levels with an empty array, which will
        eventually be populated with Employees"""

        self.levels_to_employees = {}# number of levels 
        for i in range(0, self.num_employee_levels): #from 0 to 8
            self.levels_to_employees[i] = [] #i varies from 0 to 8, makes a list 

    def hire(self):
        """Populates levels_to_employees with 50% male/50% female employees"""
        gender = ['men', 'women'] #create a list
        #Randomly assign gender to first employee
        next_gender = random.choice(gender)
        level = 0 #start at level 0
        k = 1
        CV_bias_F = 0.30
        CV_bias_M = 0.70
        for positions in self.num_positions_at_level: #iterate over number of positions at the current level, e.g. [20,16,12,8,4] 
            employee_list_at_level = self.levels_to_employees.get(level) #start at level 0, will then build up to level 8
            append = employee_list_at_level.append #append to employee list 
            if self.num_positions_at_level[1] == len(self.levels_to_employees.get(k)):
                if employee_list_at_level is not None: 
                    while len(employee_list_at_level) < positions: #while the number of employees is lower than the max number of posiitions at the level continue appending 
                        weights = [CV_bias_M, CV_bias_F]
                        gender_hired = choice(gender, p=weights)
                        append(Employee(gender_hired))
            elif self.num_positions_at_level[1] != len(self.levels_to_employees.get(k)):
                if employee_list_at_level is not None: 
                    while len(employee_list_at_level) < positions: #while the number of employees is lower than the max number of posiitions at the level continue appending 
                        append(Employee(next_gender))
                        if next_gender == "women": #shift between men and women 
                            next_gender = "men"
                        else: 
                            next_gender = "women"
            level += 1 #go one level up
                

    def run(self):
        """Run simulation"""
        for _ in range(0, self.iterations_per_simulation):
            self.attrit() 
            self.talent_review()
            self.promote() 
            self.hire()

    def talent_review(self):
        """Defining the confidence expressions for gender combinations"""
        conf_FF = 0.9796
        conf_MF = 1.0340
        conf_FM = 0.9297
        conf_MM = 1.0567
        
        """Looks at each employee object in dictionary, checks gender and gives
        random performance rating"""
        for level in range(self.num_employee_levels): #loop through the levels
            employee_list = self.levels_to_employees.get(level) #get the employees at a given level - save to employ list
            if level in (6, 7):           
                for employee in employee_list: #for i in employee list --> so two loops in one 
                    new_rating = random.normal(10, 1)#draw randoms samples from a normal distribution, mean and sd is defined
                    bias_FF = (self.promotion_bias_FF/100.0) + 1 #take value from promotion bias variable 
                    bias_FM = (self.promotion_bias_FM/100.0) + 1 #take value from promotion bias variable 
                    bias_MM = (self.promotion_bias_MM/100.0) + 1 #take value from promotion bias variable 
                    bias_MF = (self.promotion_bias_MF/100.0) + 1 #take value from promotion bias variable 
                    
                    ###Making a comitee
                    level_8 = 7 #Define the top level
                    men_in_comitee = 0 #Make value to count from
                    women_in_comitee = 0 #Make value to count from

                    employees_at_level_8 = self.levels_to_employees.get(level_8) #saving employees at level 7 in a list

                    #Finding manager (best performing at level)
                    n = 0
                    comitee_list = []
                    for employee in employees_at_level_8:
                        if n == 0: 
                            manager = employee
                            n = n + 1
#                            print("first manager", manager.gender)
                        elif employee.rating > manager.rating: 
                            comitee_list.append(manager)
                            manager = employee
#                            print("new manager", manager.gender)
                        else: 
                            comitee_list.append(employee)
#                            print("comitee list", len(comitee_list))

#                        print("manager rating", manager.rating)

                    comitee_size = 6
                    comitee = random.choice(comitee_list, comitee_size)

                    if manager.gender == "men": 
                        manager_bias_F = 0.77 
                        manager_bias_M = 1
                        #print("male manager")
                    else: 
                        manager_bias_F = 0.78 
                        manager_bias_M = 1
                        #print("woman manager")

                    for i in comitee: #Making loop to count number of different gender at level 7
                        if i.gender == "men":
                            men_in_comitee = float(men_in_comitee + 1)
                        else:
                            women_in_comitee = float(women_in_comitee + 1)

                     ###Biasing the promotion decision
                    #Calculating bias, which affects the promoting decision
                    bias_against_women = (bias_FF+bias_MF)/2 #bias againt women as follower #0.99
                    bias_against_men = (bias_FM+bias_MM)/2 #bias against men as follower #1.02

                    #Weighing the bias for FF, MM, FM, MF by gender bias at top level and percentage of gender at the level
                    weighted_bias_FF = float(bias_against_women)*float(bias_FF)*(float(women_in_comitee)/float(comitee_size))
                    weighted_bias_FM = float(bias_against_women)*float(bias_FM)*(float(women_in_comitee)/float(comitee_size))
                    weighted_bias_MM = float(bias_against_men)*float(bias_MM)*(float(men_in_comitee)/float(comitee_size))
                    weighted_bias_MF = float(bias_against_men)*float(bias_MF)*(float(men_in_comitee)/float(comitee_size))
                    
                    #Calculating current bias aginst men and women as a product of weighted  
                    current_comitee_bias_F = weighted_bias_FF + weighted_bias_MF
                    current_comitee_bias_M = weighted_bias_FM + weighted_bias_MM
                    
#                    print("manager bias F", manager_bias_F, "manager bias M",manager_bias_M)
#                    print("high level,  comitee bias F", current_comitee_bias_F)
#                    print("high level,  comitee bias M", current_comitee_bias_M)
#                    
                    #Weighting the current comitee bias with the manager bias_FF
                    current_bias_F = current_comitee_bias_F *0.8 + manager_bias_F*0.2*bias_against_women
                    current_bias_M = current_comitee_bias_M *0.8 + manager_bias_M*0.2*bias_against_men
                    
#                    print("high level,  summed bias F", current_bias_F)
#                    print("high level,  summed bias M", current_bias_M)
                    
                    #Weighing the confidence in relation to gender proportion in hiring comitee
                    weighted_conf_FF = float(conf_FF)*(float(women_in_comitee)/float(comitee_size))
                    weighted_conf_MF = float(conf_MF)*(float(women_in_comitee)/float(comitee_size))
                    weighted_conf_MM = float(conf_MM)*(float(men_in_comitee)/float(comitee_size))
                    weighted_conf_FM = float(conf_FM)*(float(men_in_comitee)/float(comitee_size))
                    
                    #Calculating current bias aginst men and women as a product of weighted  
                    current_conf_F = weighted_conf_FF + weighted_conf_FM
                    current_conf_M = weighted_conf_MM + weighted_conf_MF
                    
                    if employee.gender == "men": #if own gender equals the gender which is favored, do this
                        previous_rating = employee.rating/2
                        # Saves updated rating to Employee object
                        employee.rating = (previous_rating + new_rating)
                        employee.rating = employee.rating* current_conf_M
                        employee.rating = employee.rating * current_bias_M 
                    else:
                        previous_rating = employee.rating/2
                        # Saves updated rating to Employee object
                        employee.rating = (previous_rating + new_rating)
                        employee.rating = employee.rating * current_conf_F
                        employee.rating = employee.rating * current_bias_F 
                        #print("high level employee rating female after bias", employee.rating)
            
            if level in (0, 1, 2, 3, 4, 5):    
                for employee in employee_list: #for i in employee list --> so two loops in one 
                    new_rating = random.normal(10, 1)#draw randoms samples from a normal distribution, mean and sd is defined
                    bias_FF = (self.promotion_bias_FF/100.0) + 1 #take value from promotion bias variable 
                    bias_FM = (self.promotion_bias_FM/100.0) + 1 #take value from promotion bias variable 
                    bias_MM = (self.promotion_bias_MM/100.0) + 1 #take value from promotion bias variable 
                    bias_MF = (self.promotion_bias_MF/100.0) + 1 #take value from promotion bias variable 
                    
                    ###Making a comitee
                    comitee_lower_level = int(level + 1) #Define the top level
                    comitee_higher_level = int(level + 2) #Define the top level
                    
                    men_in_comitee = 0 #Make value to count from
                    women_in_comitee = 0 #Make value to count from
                    
                    employees_lower_level_comitee = self.levels_to_employees.get(comitee_lower_level) #saving employees at level 7 in a list
                    employees_higher_level_comitee = self.levels_to_employees.get(comitee_higher_level) #saving employees at level 7 in a list

                    #Finding manager on the highest level(best performing at level)
                    n = 0
                    higher_level_comitee_list = []
                    for employee in employees_higher_level_comitee:
                        if n == 0: 
                            manager = employee
                            n = n + 1
#                            print("first manager", manager.gender)
                        elif employee.rating > manager.rating: 
                            higher_level_comitee_list.append(manager)
                            manager = employee
#                            print("new manager", manager.gender)
                        else: 
                            higher_level_comitee_list.append(employee)
#                            print("comitee list", len(comitee_list))

#                        print("manager rating", manager.rating)

                    num_employees_higher_level_comitee = len(higher_level_comitee_list)
                    num_employees_lower_level_comitee = len(employees_lower_level_comitee)
                    
                    comitee_size = 6
                    comitee_from_lower_level_size = int(comitee_size/2)
                    comitee_from_higher_level_size = int(comitee_size/2)
                    
                    comitee_employees = [] #Make empty list to append kept employees to 
                    
                    comitee_lower_level = random.choice(range(num_employees_lower_level_comitee), comitee_from_lower_level_size) #Choose random individuls to keep
                    for n in comitee_lower_level:  #Loop through list of kept employees
                        comitee_employees.append(employees_lower_level_comitee[n]) #append indices to retain to list of employees at the given level
                    
                    comitee_higher_level = random.choice(range(num_employees_higher_level_comitee), comitee_from_higher_level_size) #Choose random individuls to keep
                    for t in comitee_higher_level:  #Loop through list of kept employees
                        comitee_employees.append(higher_level_comitee_list[t]) #append indices to retain to list of employees at the given level
                                        
                    
                    ###Biasing the promotion decision
                    if manager.gender == "men": 
                        manager_bias_F = 0.77 
                        manager_bias_M = 1
                        #print("male manager")
                    else: 
                        manager_bias_F = 0.78 
                        manager_bias_M = 1
                        #print("woman manager")

                    for i in comitee_employees: #Making loop to count number of different gender at lvel 7
                        if i.gender == "men":
                            men_in_comitee = float(men_in_comitee + 1)
                        else:
                            women_in_comitee = float(women_in_comitee + 1)
                    
                    #Calculating bias, which affects the promoting decision
                    bias_against_women = (bias_FF+bias_MF)/2 #bias againt women as follower #0.99
                    bias_against_men = (bias_FM+bias_MM)/2 #bias against men as follower #1.02

                    #Weighing the bias for FF, MM, FM, MF by gender bias at top level and percentage of gender at the level
                    weighted_bias_FF = float(bias_against_women)*float(bias_FF)*(float(women_in_comitee)/float(comitee_size))
                    weighted_bias_FM = float(bias_against_women)*float(bias_FM)*(float(women_in_comitee)/float(comitee_size))
                    weighted_bias_MM = float(bias_against_men)*float(bias_MM)*(float(men_in_comitee)/float(comitee_size))
                    weighted_bias_MF = float(bias_against_men)*float(bias_MF)*(float(men_in_comitee)/float(comitee_size))

                    #Calculating current bias aginst men and women as a product of weighted  
                    current_comitee_bias_F = weighted_bias_FF + weighted_bias_MF
                    current_comitee_bias_M = weighted_bias_FM + weighted_bias_MM
                    
                    #Weighting the current comitee bias with the manager bias_FF
                    current_bias_F = current_comitee_bias_F *0.8 + manager_bias_F*0.2*bias_against_women
                    current_bias_M = current_comitee_bias_M *0.8 + manager_bias_M*0.2*bias_against_men

                    #Weighing the confidence in relation to gender proportion in hiring comitee
                    weighted_conf_FF = float(conf_FF)*(float(women_in_comitee)/float(comitee_size))
                    weighted_conf_MF = float(conf_MF)*(float(women_in_comitee)/float(comitee_size))
                    weighted_conf_MM = float(conf_MM)*(float(men_in_comitee)/float(comitee_size))
                    weighted_conf_FM = float(conf_FM)*(float(men_in_comitee)/float(comitee_size))
                    
                    #Calculating current bias aginst men and women as a product of weighted  
                    current_conf_F = weighted_conf_FF + weighted_conf_FM
                    current_conf_M = weighted_conf_MM + weighted_conf_MF

                    if employee.gender == "men": #if own gender equals the gender which is favored, do this
                        previous_rating = employee.rating/2
                        # Saves updated rating to Employee object
                        employee.rating = (previous_rating + new_rating) * current_conf_M
                        employee.rating = employee.rating * current_bias_M 
                    else:
                        previous_rating = employee.rating/2
                        # Saves updated rating to Employee object
                        employee.rating = (previous_rating + new_rating) * current_conf_F
                        employee.rating = employee.rating * current_bias_F 
                    
    def attrit(self):
        """Looks at each employee in dictionary and randomly retains employees
        based on global attrition rate""" #its random who stays and who does not 

        for level in range(self.num_employee_levels): #Loop through each level
            employee_list_at_level = self.levels_to_employees.get(level) #save employees at a given level in a list
            num_employees_at_level = len(employee_list_at_level) #Save number of individuals at given level 
            num_employees_to_retain = int(num_employees_at_level * ((100 - self.attrition)/100.0)) #Find number of employees to keep
            indices_to_retain = random.choice(range(num_employees_at_level), num_employees_to_retain) #Choose random individuls to keep
            retained_employees = [] #Make empty list to append kept employees to 
            for i in indices_to_retain:  #Loop through list of kept employees
                retained_employees.append(employee_list_at_level[i]) #append indices to retain to list of employees at the given level

            self.levels_to_employees[level] = retained_employees #Save the indices at the given level

    def promote(self):
        """Starts at highest level and checks for open positions, then removes the top
        employees from the level below to fill the open positions. Continues this process through 
        each lower level. Only the entry level will have open positions at the end of this method."""
        for i in range(self.num_employee_levels - 1, 0, -1):
            promote_to_level = i
            promote_from_level = i - 1

            promote_from_employees = self.levels_to_employees.get(promote_from_level) #save list of employees to promote from

            promote_to_employees = self.levels_to_employees.get(promote_to_level) #save list of employees at the level we wish to promote to

            promote_from_employees.sort(key=lambda x: x.rating, reverse=True) #Sorting the list of employees to promote from in descending order by their rating

            num_candidates = len(promote_from_employees) #Saving the number of candidates, which we are to promote from
            total_positions = self.num_positions_at_level[promote_to_level] #Saving the total number of positions at a given level
            filled_positions = len(promote_to_employees) #Saving the number of employees already at the level
            open_positions = total_positions - filled_positions #Finding the number of open positions
            num_promotions = min(num_candidates, open_positions) #finding number of promotions from the lower level - Is this done in case that there is not enough employees at the lower level? 
            candidates_to_promote = promote_from_employees[:num_promotions] #choose the top number of candidates in the number of promotions
            # Saves revised data back to the dictionary
            self.levels_to_employees[promote_from_level] = promote_from_employees[num_promotions:] #save the individuals not promoted in the level where to promote from
            self.levels_to_employees[promote_to_level] = promote_to_employees + candidates_to_promote #add the promoted individuals the the level above

    def get_result(self):
        """Counts number of men and women at each level and saves totals to
        the corresponding list."""
        total_men_at_level = [0] * self.num_employee_levels #make a list of number of employee levels
        total_women_at_level = [0] * self.num_employee_levels

        for level in range(self.num_employee_levels): #loop through the levels
            employee_list = self.levels_to_employees.get(level) #get the employees at a given level - save to employ list

            for employee in employee_list: #for each individual in the employee list
                if employee.gender == "men":  # if the gender is male
                    total_men_at_level[level] += 1 #add 1 to total men list
                else:
                    total_women_at_level[level] += 1 #else add 1 t0 total number of females
        return Result(total_men_at_level, total_women_at_level) #give output i.e. total number males and total number of females

class Control:
    """Runs bias simulations based on "Male-Female Differences: A Computer
    Simulation" from the Feb, 1996 issue of American Psychologist.
    http://www.ruf.rice.edu/~lane/papers/male_female.pdf"""

    def __init__(self, promotion_bias_FF, promotion_bias_FM, promotion_bias_MM, promotion_bias_MF):
        #self.bias_favors_this_gender = bias_favors_this_gender
        self.promotion_bias_FF = int(promotion_bias_FF)
        self.promotion_bias_FM = int(promotion_bias_FM)
        self.promotion_bias_MM = int(promotion_bias_MM)
        self.promotion_bias_MF = int(promotion_bias_MF)
        self.num_simulations = 100 #defining number of simulations, usually set to 1000
        self.attrition = 15 #15% turnover rate is applied
        self.iterations_per_simulation = 10 #20 performance-review cycles are generated 
        self.num_positions_at_level = [500, 350, 200, 150, 100, 75, 40, 10] #define hierarchy [500, 350, 200, 150, 100, 75, 40, 10]
        self.num_employee_levels = len(self.num_positions_at_level) #define number of employee levels

    def run_simulations(self):
        """Run NUM_SIMULATIONS simulations"""
        self.results = [] #creating empty list
        append = self.results.append
        for _ in range(self.num_simulations):#_ emphasize the value in the xrange is subordinate, it just needs to run the number of iterations in this case 30 times - as it is 30 simulations
            simulation = Simulation(self.num_simulations, self.attrition, self.iterations_per_simulation, 
                self.promotion_bias_FF, self.promotion_bias_FM, self.promotion_bias_MM, self.promotion_bias_MF, self.num_positions_at_level) #Adding information to the previously defined function
            
            simulation.run() #run the simulation
            append(simulation.get_result()) #use the results function previously defined to append the results to results list

    def fetch_results(self):
        """Creates two lists. Each contains the percent of that gender at each employee level """
        total_men_at_levels = [] #creating empty list
        total_women_at_levels = [] #creating empty list
        # Setting append constructs here, saves compute time in loop
        men_append = total_men_at_levels.append 
        women_append = total_women_at_levels.append

        for level in range(0, self.num_employee_levels): #loop through the levels
            total_num_men = 0.00
            total_num_women = 0.00
            for result in self.results: #loop through the results, add the number of wo/men at each level to the total number of wo/men 
                total_num_men += result.men[level] #+= means: . The list object implements it and uses it to iterate over an iterable object appending each element to itself in the same way that the list's extend method does.
                total_num_women += result.women[level]

            total_employees = total_num_men + total_num_women #Counting total number of employees
            men_percentage = 100 * total_num_men / total_employees #calculating the percentage of men
            women_percentage = 100 * total_num_women / total_employees #calculating the percentage of women
 
            men_append(men_percentage)
            women_append(women_percentage)
        return [total_men_at_levels, total_women_at_levels]


####OUTPUT SECTION
#Actual raesults from our experiment
#promotion_bias_FF, promotion_bias_FM, promotion_bias_MM, promotion_bias_MF
control = Control(-2, 2, -2, 2)

control.run_simulations()
results = control.fetch_results()


print(results)
#hist(results)


DATA = DATA.append({
    'Results': results}, ignore_index = True)

DATA.to_csv('simulation_1.csv')