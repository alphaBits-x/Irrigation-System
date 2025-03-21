import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import skfuzzy.control as ctrl

# Defining the ranges for the fuzzy sets
soil_moisture = np.arange(0, 101, 1)
rainfall_range = np.arange(0, 101, 1)
water_amount_range = np.arange(0, 101, 1)

# Defining fuzzy membership functions for Soil Moisture
soil_moisture_low = fuzz.trimf(soil_moisture, [0, 0, 30])
soil_moisture_medium = fuzz.trimf(soil_moisture, [20, 50, 80])
soil_moisture_high = fuzz.trimf(soil_moisture, [60, 100, 100])

# Defining fuzzy membership functions for Rainfall
low_rain = fuzz.trimf(rainfall_range, [0, 0, 30])
medium_rain = fuzz.trimf(rainfall_range, [20, 50, 80])
high_rain = fuzz.trimf(rainfall_range, [60, 100, 100])

# Defining fuzzy membership functions for Water Amount
low_water = fuzz.trimf(water_amount_range, [0, 0, 30])
medium_water = fuzz.trimf(water_amount_range, [20, 50, 80])
high_water = fuzz.trimf(water_amount_range, [60, 100, 100])

# Plotting the membership functions
plt.figure(figsize=(10, 5))

# Soil Moisture Plot
plt.subplot(1, 2, 1)
plt.plot(soil_moisture, soil_moisture_low, label='Low Soil Moisture')
plt.plot(soil_moisture, soil_moisture_medium, label='Medium Soil Moisture')
plt.plot(soil_moisture, soil_moisture_high, label='High Soil Moisture')
plt.title('Soil Moisture Membership Functions')
plt.xlabel('Soil Moisture (%)')
plt.ylabel('Membership Degree')
plt.legend()

# Rainfall Plot
plt.subplot(1, 2, 2)
plt.plot(rainfall_range, low_rain, label='Low Rainfall')
plt.plot(rainfall_range, medium_rain, label='Medium Rainfall')
plt.plot(rainfall_range, high_rain, label='High Rainfall')
plt.title('Rainfall Membership Functions')
plt.xlabel('Rainfall (%)')
plt.ylabel('Membership Degree')
plt.legend()

plt.tight_layout()
plt.show()

# Defining fuzzy variables
soil_moisture_input = ctrl.Antecedent(soil_moisture, 'soil_moisture')
rainfall_input = ctrl.Antecedent(rainfall_range, 'rainfall')
water_output = ctrl.Consequent(water_amount_range, 'water_amount')

# Automating the membership function assignments
soil_moisture_input['low'] = soil_moisture_low
soil_moisture_input['medium'] = soil_moisture_medium
soil_moisture_input['high'] = soil_moisture_high

rainfall_input['low'] = low_rain
rainfall_input['medium'] = medium_rain
rainfall_input['high'] = high_rain

water_output['low'] = low_water
water_output['medium'] = medium_water
water_output['high'] = high_water

# Defining fuzzy rules
rule1 = ctrl.Rule(soil_moisture_input['low'] & rainfall_input['low'], water_output['low'])
rule2 = ctrl.Rule(soil_moisture_input['low'] & rainfall_input['medium'], water_output['medium'])
rule3 = ctrl.Rule(soil_moisture_input['low'] & rainfall_input['high'], water_output['high'])
rule4 = ctrl.Rule(soil_moisture_input['medium'] & rainfall_input['low'], water_output['medium'])
rule5 = ctrl.Rule(soil_moisture_input['medium'] & rainfall_input['medium'], water_output['medium'])
rule6 = ctrl.Rule(soil_moisture_input['medium'] & rainfall_input['high'], water_output['high'])
rule7 = ctrl.Rule(soil_moisture_input['high'] & rainfall_input['low'], water_output['low'])
rule8 = ctrl.Rule(soil_moisture_input['high'] & rainfall_input['medium'], water_output['medium'])
rule9 = ctrl.Rule(soil_moisture_input['high'] & rainfall_input['high'], water_output['high'])

# Creating the control system and simulation
water_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
irrigation_sim = ctrl.ControlSystemSimulation(water_ctrl)

# Input values for soil moisture and rainfall (for example purposes)
soil_moisture_value = int(input("Soil Moisture %: "))  # Example: 40% soil moisture
rainfall_value = int(input("Rainfall %: "))       # Example: 50% rainfall

# Passing inputs to the simulation
irrigation_sim.input['soil_moisture'] = soil_moisture_value
irrigation_sim.input['rainfall'] = rainfall_value

# Crunching the numbers
irrigation_sim.compute()

# Output the water amount
print(f"Recommended water amount: {irrigation_sim.output['water_amount']}%")
water_output.view(sim=irrigation_sim)
