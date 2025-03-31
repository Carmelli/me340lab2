import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad 

 
#Define constants
von_mises_factor = 2/math.sqrt(3)
roll_radius = 32.5
T = 20
k = -0.5058*T + 210.4
n =-0.0004*T + 0.2185
colors = ['red', 'blue', 'green']

#Resetting global variables
plt.style.use('default')

# Sample data (3 samples)
samples = [
    {'h_naught': 1.654, 'h_after': 1.502, 'width': 24.615, 'reductions': [0.1654], 'label': 'Sample 1'},
    {'h_naught': 1.598, 'h_after': 1.314, 'width': 24.408, 'reductions': [0.2397], 'label': 'Sample 2'},
    {'h_naught': 1.584, 'h_after': 1.280, 'width': 25.057, 'reductions': [0.3168], 'label': 'Sample 3'}
]

#Different friction values
friction_values = [0.05, 0.10, 0.15, 0.20]

#Define functions
def mean_flow_stress(k, n, epsilon_final):
    integral, _ = quad(lambda x: k * x**n, 0, epsilon_final)
    return integral / epsilon_final

def geometry_values(h_naught, h_after, width):
    h_bar = (h_naught + h_after) / 2  
    length = math.sqrt(roll_radius * (h_naught - h_after)) 
    area = width * length
    return length, area, h_bar 

def friction_factor(friction_value, length, h_bar):
    Q = (friction_value * length) / h_bar 
    return 1 / Q * (math.e**(Q) - 1)

def pressure(von_mises_factor, mean_flow_stress, friction_factor):
    return von_mises_factor * mean_flow_stress * friction_factor

def rolling_force(pressure, area):
    return pressure * area

def rolling_torque(rolling_force):
    return rolling_force * length/2 



# Set up the plot
plt.figure(figsize=(10, 6))
plt.title('Rolling Force vs. Friction Factor for Different Samples and Reductions')
plt.xlabel('Friction Factor')
plt.ylabel('Rolling Force (N)')
plt.grid(True)

# Automatically generate distinct colors
num_lines = sum(len(sample['reductions']) for sample in samples)  # Total lines
colors = plt.cm.tab10(np.linspace(0, 1, num_lines))  # 10 distinct colors (or use 'viridis')

color_idx = 0
# Main calculation and plotting loop
for i, sample in enumerate(samples):
    # Calculate geometry values for this sample
    length, area, h_bar = geometry_values(sample['h_naught'], sample['h_after'], sample['width'])
    
    for reduction, color in zip(sample['reductions'], colors):
        epsilon_final = reduction / sample['h_naught']
        mfs = mean_flow_stress(k, n, epsilon_final)
        
        # Store results for plotting
        ff_values = []
        force_values = []
        torque_values = []
        
        for friction in friction_values:
            ff = friction_factor(friction, length, h_bar)
            p = pressure(von_mises_factor, mfs, ff)
            force = rolling_force(p, area)
            
            ff_values.append(ff)
            force_values.append(force)
            
        for friction in torque_values:
            rt = rolling_torque(rolling_force)
        
            torque_values.append(rt)
        
        # Plot for this reduction
        reduction_percent = (reduction/sample['h_naught'])*100
        plt.plot(ff_values, force_values, 'o-', color=colors[i], 
                label=f"{sample['label']}, {reduction_percent:.1f}% reduction")
        
        plt.plot(ff_values, torque_values, 'o-', color=colors[i], 
                label=f"{sample['label']}, {reduction_percent:.1f}% reduction")
   
                
        force_results = force_values
        torque_results = torque_values
        print("Rolling Forces: ", force_results)
        print("Rolling Torque: ", torque_results)
    

# Add legend and show plot
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


results = force_values, ff_values
print("Rolling Forces: ", results)
    
