
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline

# Read the CSV file into a DataFrame
df = pd.read_csv("xy_t.csv")  # Change the file name here

# Extract the x, y, and time values in millimeters
x_coords_mm = df['X'].values
y_coords_mm = df['Y'].values
time_values = df['t'].values

# Known radius value as an initial guess
initial_r_guess = 64.35/2  # Replace with your accurate radius measurement

# Use the original circle equation
def circle_equation(coords, h, k, r):
    x, y = coords
    return (x - h)**2 + (y - k)**2 - r**2

# Fit the circle equation to the data with an initial guess for the radius
initial_guess = [0, 0, initial_r_guess]  # Initial guesses for h, k, and r
params, _ = curve_fit(circle_equation, (x_coords_mm, y_coords_mm), np.zeros_like(x_coords_mm), p0=initial_guess)

# Extract the fitted parameters
fitted_h, fitted_k, fitted_r = params

# Generate x and y values for the fitted circle
theta = np.linspace(0, 2 * np.pi, 1000)
x_fit_mm = fitted_r * np.cos(theta) + fitted_h
y_fit_mm = fitted_r * np.sin(theta) + fitted_k

# Interpolate the fitted circle to create smooth functions for x and y
fitted_time = np.linspace(time_values[0], time_values[-1], 1000)
x_spline = UnivariateSpline(fitted_time, x_fit_mm, s=0, k=4)
y_spline = UnivariateSpline(fitted_time, y_fit_mm, s=0, k=4)

# Differentiate the splines to get velocity components
dx_dt_spline = x_spline.derivative()
dy_dt_spline = y_spline.derivative()

# Calculate the velocity magnitudes
instantaneous_velocities_norm = np.sqrt(dx_dt_spline(fitted_time)**2 + dy_dt_spline(fitted_time)**2)

# Calculate the average velocity
average_velocity_m_s = np.mean(instantaneous_velocities_norm) / 1000.0

# Convert velocities from mm/s to m/s
instantaneous_velocities_norm_m_s = instantaneous_velocities_norm / 1000.0

# Create the Matplotlib plot for displaying velocities in m/s
plt.figure(figsize=(8, 6))
plt.plot(fitted_time, instantaneous_velocities_norm_m_s, label='Instantaneous Velocity Norm (m/s)', color='b')
plt.axhline(average_velocity_m_s, linestyle='--', label='Average Velocity (m/s)', color='r')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Instantaneous and Average Velocities (Norm) Using Fitted Curve Derivative')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
