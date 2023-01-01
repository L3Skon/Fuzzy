import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the input variables
food = ctrl.Antecedent(np.arange(0, 11, 1), 'food')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')

# Define the output variable
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# Define the membership functions for each variable

food['poor'] = fuzz.trimf(food.universe, [0, 0, 5])
food['average'] = fuzz.trimf(food.universe, [0, 5, 10])
food['good'] = fuzz.trimf(food.universe, [5, 10, 10])

service['poor'] = fuzz.trimf(service.universe, [0, 0, 5])
service['average'] = fuzz.trimf(service.universe, [0, 5, 10])
service['good'] = fuzz.trimf(service.universe, [5, 10, 10])

tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

# Define the fuzzy rules

rule1 = ctrl.Rule(food['poor'] | service['poor'], tip['low'])
rule2 = ctrl.Rule(service['average'], tip['medium'])
rule3 = ctrl.Rule(service['good'] | food['good'], tip['high'])

# Create the control system
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

# Create the simulation
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# Set the input values

food_input = float(input('Enter the value for food (0-10): '))
service_input = float(input('Enter the value for service (0-10): '))
tipping.input['food'] = food_input
tipping.input['service'] = service_input

# Calculate the output

tipping.compute()

# Print the output

print(f'The recommended tip is: {tipping.output["tip"]:.2f}')
