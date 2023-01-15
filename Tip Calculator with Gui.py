import numpy as np
import tkinter as tk
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


def calculate_tip():
    # Get the input values from the Entry widgets
    food_input = food_entry.get()
    service_input = service_entry.get()

    try:
        # Convert the input values to floats
        food_value = float(food_input)
        service_value = float(service_input)
    except ValueError:
        # Display an error message if the input is invalid
        tip_label.config(text='Error: Invalid input')
        return
        
          # Set the input values in the simulation
    tipping.input['food'] = food_value
    tipping.input['service'] = service_value

    # Calculate the output

    tipping.compute()

    # Update the label with the tip value
    tip_label.config(text=f'Tip: {tipping.output["tip"]:.2f}')


# Create the main window
window = tk.Tk()
window.title('Tip Calculator')
window.geometry("250x150")

# Create the input widgets
food_label = tk.Label(text='Food Quality (0-10):')
food_entry = tk.Entry()

service_label = tk.Label(text='Service Quality (0-10):')
service_entry = tk.Entry()

# Create the output widget
tip_label = tk.Label(text='Tip:')

# Create the button widget
calculate_button = tk.Button(text='Calculate Tip', command=calculate_tip)

# Add the widgets to the main window
food_label.pack()
food_entry.pack()

service_label.pack()
service_entry.pack()

tip_label.pack()
calculate_button.pack()

# Start the event loop
window.mainloop()