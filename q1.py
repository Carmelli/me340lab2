import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad 


def rolling_force_solver(): 
    
    #Define constants
    friction_values  = [0.05, 0.10, 0.15, 0.20]
    change_in_thickness = 0.1654 
    original_thickness = 1.654 
    epsilon_final = change_in_thickness / original_thickness
    von_mises_factor = 2/math.sqrt(3)
    roll_radius = 32.5
    

    #Calculating mean flow stress, thickness also represents h 
    T = 20
    k = -0.5058*T + 210.4
    n =-0.0004*T + 0.2185

    
    #Calculating mean flow stress
    integral, _ = quad(lambda x: k * x**n, 0, epsilon_final)
    mean_flow_stress = integral / epsilon_final
        
    
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


import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad 

# Define constants
von_mises_factor = 2/math.sqrt(3)
roll_radius = 32.5
T = 20
k = -0.5058*T + 210.4
n = -0.0004*T + 0.2185

# Sample data (3 samples)
samples = [
    {'h_naught': 1.654, 'h_after': 1.502, 'width': 24.615, 'reductions': [0.1654, 0.2481, 0.3308]},
    {'h_naught': 1.598, 'h_after': 1.314, 'width': 24.408, 'reductions': [0.1598, 0.2397, 0.3196]},
    {'h_naught': 1.314, 'h_after': 1.280, 'width': 25.057, 'reductions': [0.1724, 0.2516, 0.3308]}
]

# Friction values to test
friction_values = [0.05, 0.10, 0.15, 0.20]

# Define functions (same as before)
def mean_flow_stress(k, n, epsilon_final):
    integral, _ = quad(lambda x: k * x**n, 0, epsilon_final)
    return integral / epsilon_final

def geometry_values(h_naught, h_after, width):
    h_bar = (h_naught + h_after) / 2  
    length = math.sqrt(roll_radius * (h_naught - h_after)) 
    area = width * length
    return length, area

def friction_factor(friction_value, length, h_bar):
    Q = (friction_value * length) / h_bar 
    return 1 / Q * (math.e**(Q) - 1)

def pressure(von_mises_factor, mean_flow_stress, friction_factor):
    return von_mises_factor * mean_flow_stress * friction_factor

def rolling_force(pressure, area):
    return pressure * area

# Main calculation loop
for sample_idx, sample in enumerate(samples, 1):
    print(f"\nProcessing Sample {sample_idx}:")
    print(f"Initial thickness: {sample['h_naught']} mm")
    print(f"Final thickness: {sample['h_after']} mm")
    print(f"Width: {sample['width']} mm")
    
    # Calculate geometry values for this sample
    length, area = geometry_values(sample['h_naught'], sample['h_after'], sample['width'])
    h_bar = (sample['h_naught'] + sample['h_after']) / 2
    
    for reduction in sample['reductions']:
        epsilon_final = reduction / sample['h_naught']
        mfs = mean_flow_stress(k, n, epsilon_final)
        
        print(f"\n  Reduction: {reduction:.4f} mm (ε = {epsilon_final:.4f})")
        
        for friction in friction_values:
            ff = friction_factor(friction, length, h_bar)
            p = pressure(von_mises_factor, mfs, ff)
            force = rolling_force(p, area)
            
            print(f"    Friction: {friction:.2f} -> Force: {force:.2f} N")
    
    # You could add plotting here for each sample if desired
    # plt.figure()
    # ... plotting code ...