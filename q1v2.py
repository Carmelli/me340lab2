# This is the better coded version btw

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad 

#Define constants
friction_values  = [0.05, 0.10, 0.15, 0.20]
von_mises_factor = 2/math.sqrt(3)
roll_radius = 32.5


#Define functions
def n_and_k(T):
    """
    Calculate the values of k and n based on temperature T.
    The equations are given as:
    k = -0.5058*T + 210.4
    n = -0.0004*T + 0.2185
    """
    k = -0.5058*T + 210.4
    n = -0.0004*T + 0.2185
    return k, n

#Function for mean flow stress
    def mean_flow_stress(k, n, epsilon_final):
        integral, _ = quad(lambda x: k * x**n, 0, epsilon_final)
        return integral / epsilon_final

def mean_flow_stress(k, n, epsilon_final):
    integral, _ = quad(lambda x: k * x**n, 0, epsilon_final)[0]

def rolling_force_solver(): 

    #Calculating mean flow stress, thickness also represents h 
   
    change_in_thickness = 0.1654 
    original_thickness = 1.654 
    epsilon = change_in_thickness / original_thickness
    mean_flow_stress = k * epsilon**n

    #Calculating friction factor (using average length and average height, also literally just took avg for sample 1, also using experimental measured values for h_after)
    h_naught = 1.654   
    h_after = 1.502 
    h_bar  = (h_naught + h_after )/2  
    length = math.sqrt(roll_radius*(h_naught - h_after)) 
    width = 24.615 
    area = width * length
    
    #Creating an array to store rolling forces
    rolling_forces = [] 
    
    #Loop through friction, calculating rolling force for each one
    for friction_value in friction_values:
        Q = (friction_value*length)/h_bar 
        friction_factor = 1/Q*(math.e**(Q)-1)

        #Calculating pressure
        pressure = von_mises_factor * mean_flow_stress * friction_factor

        #Calculating rolling force 
        rolling_force = pressure * area
        rolling_forces.append(rolling_force)
    return rolling_forces

# Call the function
friction_values = [0.05, 0.10, 0.15, 0.20]
rolling_forces = rolling_force_solver()

        #Graph
plt.figure(figsize=(8,5))
plt.plot(friction_values, rolling_forces, marker='o', linestyle='-', color='b', label='Rolling Force')
plt.xlabel("Friction Value")
plt.ylabel("Rolling Force N)")
plt.title("Rolling Force vs Friction Value")
plt.grid(True)
plt.legend() 

#Show plot
plt.show()

#Calling function
results = rolling_force_solver()
print("Rolling Forces: ", results)
    

    

def rolling_torque_solver(pressure, area): 
     #Calculating rolling torque and power
        """
     rolling_force = Self.rolling_force_solver(pressure, area)

     rolling_torque = rolling_force * length/2
     power = (2*math.pi*rolling_force*length* N) / 60000

     return rolling_torque, power"
        """ 
    