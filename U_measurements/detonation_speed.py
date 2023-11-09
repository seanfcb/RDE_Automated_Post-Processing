import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read the CSV file into a DataFrame
df = pd.read_csv("xy_t.csv")  # Change the file name here

# Extract the x, y, and time values in millimeters
x_coords_mm = df['X'].values
y_coords_mm = df['Y'].values
time_values = df['t'].values

# Define the equation of a circle
def circle_equation(coords, h, k, r):
    x, y = coords
    return (x - h)**2 + (y - k)**2 - r**2

# Fit the circle equation to the data using least-squares fitting
params, _ = curve_fit(circle_equation, (x_coords_mm, y_coords_mm), y_coords_mm)

# Extract the fitted parameters
fitted_h, fitted_k, fitted_r = params

# Generate x and y values for the fitted circle in millimeters
theta = np.linspace(0, 2 * np.pi, 100)
x_fit_mm = fitted_r * np.cos(theta) + fitted_h
y_fit_mm = fitted_r * np.sin(theta) + fitted_k

# Create the Matplotlib plot for the fitted circle
plt.figure(figsize=(8, 6))
plt.scatter(x_coords_mm, y_coords_mm, label='Data Points', color='b')
plt.plot(x_fit_mm, y_fit_mm, label='Fitted Circle', color='r')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.title('Fitted Circle to Data Points')
plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
plt.grid(True)

# Show the first plot
plt.show()

# Calculate the instantaneous velocities' norms at each time point (converted to m/s)
instantaneous_velocities_norm = []
for i in range(1, len(time_values)):
    x_t, y_t = x_coords_mm[i], y_coords_mm[i]
    x_t_minus_1, y_t_minus_1 = x_coords_mm[i - 1], y_coords_mm[i - 1]
    delta_x = x_t - x_t_minus_1
    delta_y = y_t - y_t_minus_1
    delta_t = time_values[i] - time_values[i - 1]
    velocity_norm = np.sqrt((delta_x / delta_t)**2 + (delta_y / delta_t)**2)
    instantaneous_velocities_norm.append(velocity_norm)

# Calculate the average velocity as the mean of instantaneous velocity norms
average_velocity = np.mean(instantaneous_velocities_norm)

# Convert velocities from mm/s to m/s
instantaneous_velocities_norm_m_s = [v / 1000.0 for v in instantaneous_velocities_norm]
average_velocity_m_s = average_velocity / 1000.0

# Create the Matplotlib plot for displaying velocities in m/s
plt.figure(figsize=(8, 6))
plt.plot(time_values[1:], instantaneous_velocities_norm_m_s, label='Instantaneous Velocity Norm (m/s)', color='b')
plt.axhline(average_velocity_m_s, linestyle='--', label='Average Velocity (m/s)', color='r')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Instantaneous and Average Velocities (Norm)')
plt.legend()
plt.grid(True)

# Show the second plot
plt.show()
