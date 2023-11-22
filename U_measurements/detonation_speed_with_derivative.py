import pandas as pd
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

def fit_circle(params, x, y):
    """ Function to calculate the residuals for circle fitting. """
    h, k, r = params
    return (x - h)**2 + (y - k)**2 - r**2

def circle_equations(t, h, k, r, omega, phi):
    """ Function to compute x(t), y(t), x'(t), and y'(t). """
    x = h + r * np.cos(omega * t + phi)
    y = k + r * np.sin(omega * t + phi)
    x_prime = -r * omega * np.sin(omega * t + phi)  # Derivative of x with respect to t
    y_prime = r * omega * np.cos(omega * t + phi)  # Derivative of y with respect to t
    return x, y, x_prime, y_prime

def calculate_instantaneous_velocity(x, y, t):
    """ Calculate instantaneous velocity norms from x, y, t data. """
    dx = np.diff(x)
    dy = np.diff(y)
    dt = np.diff(t)
    velocities = np.sqrt((dx/dt)**2 + (dy/dt)**2) / 1000  # Convert to m/s
    return velocities

def main():
    # Load the data
    file_path = 'xy_t.csv'  # Replace with your file path
    data = pd.read_csv(file_path)

    # Extract x, y coordinates, and time
    x = data['X'].values
    y = data['Y'].values
    t = data['t'].values

    # Initial guess for the parameters (h, k, r)
    initial_guess = [0, 0, 1]

    # Perform the least squares fit to find the circle center
    result = least_squares(fit_circle, initial_guess, args=(x, y))
    h_fit, k_fit, r_fit = result.x

    # Estimate angular velocity omega
    theta_unwrapped = np.unwrap(np.arctan2(y - k_fit, x - h_fit))
    omega_estimated = np.mean(np.diff(theta_unwrapped) / np.diff(t))

    # Calculate instantaneous velocity norms
    inst_velocity_norms = calculate_instantaneous_velocity(x, y, t)
    avg_velocity_norm = np.mean(inst_velocity_norms)

    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot the original data points and the fitted circle
    plt.subplot(1, 2, 1)
    plt.scatter(x, y, label='Data Points')
    # Plot the fitted circle
    t_circle = np.linspace(0, 2 * np.pi, 500)
    x_circle, y_circle, _, _ = circle_equations(t_circle, h_fit, k_fit, np.abs(r_fit), 1, 0)
    plt.plot(x_circle, y_circle, color='red', label='Fitted Circle')
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.title('Circle Fitting to Data Points')
    plt.legend()
    plt.axis('equal')

    # Plot the instantaneous velocity norm and average velocity norm
    plt.subplot(1, 2, 2)
    plt.plot(t[1:], inst_velocity_norms, label='Instantaneous Velocity Norm (m/s)')
    plt.axhline(y=avg_velocity_norm, color='r', linestyle='--', label=f'Average Velocity Norm = {avg_velocity_norm:.3f} m/s')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity Norm (m/s)')
    plt.title('Velocity Norm over Time')
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
