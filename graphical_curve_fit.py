import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.widgets import CheckButtons, SpanSelector


# Define various fitting functions
def linear_func(x, a, b):
    return a * x + b

def polynomial_func(x, a, b, c):
    return a * x**2 + b * x + c

def exponential_func(x, a, b, c):
    return a * np.exp(b * x) + c

def logarithmic_func(x, a, b):
    return a * np.log(x) + b

# Generate some synthetic data
x = np.linspace(1, 10, 100)
y = 3 * np.exp(-0.5 * x) + np.random.normal(size=x.size)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3)
ax.plot(x, y, 'o')
ax.set_title('Interactive Curve Fitting')
ax.set_xlabel('X data')
ax.set_ylabel('Y data')

fit_functions = {
    'Linear': (linear_func, 'y = {:.2f}x + {:.2f}'),
    'Polynomial': (polynomial_func, 'y = {:.2f}x² + {:.2f}x + {:.2f}'),
    'Exponential': (exponential_func, 'y = {:.2f}e^({:.2f}x) + {:.2f}'),
    'Logarithmic': (logarithmic_func, 'y = {:.2f}ln(x) + {:.2f}')
}

# Plotting the selected fit
def fit_data(label):
    fit_func, eq_template = fit_functions[label]
    thisx = x[selected_indices]
    thisy = y[selected_indices]
    if label == 'Logarithmic':
        valid_indices = thisx > 0
        thisx = thisx[valid_indices]
        thisy = thisy[valid_indices]
    if len(thisx) > 1:  # Check if there are enough points to fit
        popt, _ = curve_fit(fit_func, thisx, thisy, maxfev=10000)
        ax.cla()
        ax.plot(x, y, 'o', label='Data')
        ax.plot(thisx, fit_func(thisx, *popt), label=f'{label} fit')
        ax.legend()

        # Display equation
        equation = eq_template.format(*popt)
        print(equation)  # Print equation to console
        ax.text(0.05, 0.95, equation, transform=ax.transAxes, fontsize=12,
                verticalalignment='top')

        plt.draw()

rax = plt.axes([0.05, 0.5, 0.15, 0.15], facecolor='lightgoldenrodyellow')
radio = CheckButtons(rax, list(fit_functions.keys()), [False]*4)
radio.on_clicked(fit_data)

selected_indices = []

def onselect(xmin, xmax):
    global selected_indices
    selected_indices = (x > xmin) & (x < xmax)
    ax.plot(x[selected_indices], y[selected_indices], 'o', color='red')
    plt.draw()

span = SpanSelector(ax, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

plt.show()
