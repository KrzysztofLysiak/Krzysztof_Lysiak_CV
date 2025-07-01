import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Algorithm parameters
f_threshold = 0.0001  # Accuracy
num_steps = 10000  # Maximum number of iterations

def f(x):
    return 10*x**4 + 3*x**3 - 30*x**2 + 10*x

def df(x):
    return 40*x**3 + 9*x**2 - 60*x + 10

def g(x1, x2):
    return (x1 - 2)**4 + (x2 + 3)**4 + 2 * (x1 - 2)**2 * (x2 + 3)**2

def grad_g(x1, x2):
    d1 = 4*(x1-2)**3 + 4*(x1-2)*(x2+3)**2
    d2 = 4*(x2+3)**3 + 4*(x2+3)*(x1-2)**2
    return np.array([d1, d2])

def gradient_descent(f_grad, x_init, learning_rate=0.01, threshold=f_threshold, max_steps=num_steps):
    x = np.array(x_init, dtype=float)
    
    for _ in range(max_steps):
        grad = f_grad(*x)
        x_new = x - learning_rate * grad
        
        if np.linalg.norm(x_new - x) < threshold:
            break
        
        x = x_new
    
    return x 

# Plot function f(x)
x = np.linspace(-3, 3, 400)
y = f(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y, label='$f(x)$', color='b')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend()
plt.title('Plot of function f(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()

# Plot function g(x1, x2)
x1 = np.linspace(-5, 5, 100)
x2 = np.linspace(-5, 5, 100)
X1, X2 = np.meshgrid(x1, x2)
Z = g(X1, X2)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none')
ax.set_title('Plot of function g(x1, x2)')
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('g(x1, x2)')
plt.show()

# Gradient for f(x)
x_min = gradient_descent(lambda x: np.array([df(x)]), x_init=[0], learning_rate=0.001)
print(f"Minimum of function f(x): x = {x_min[0]}")

# Gradient for g(x1, x2)
x_min_g  = gradient_descent(grad_g, x_init=[0, 0], learning_rate=0.01)
print(f"Minimum of function g(x1, x2): x1 = {x_min_g[0]}, x2 = {x_min_g[1]}")

# Experiment with different learning rates
learning_rates = [0.001, 0.01, 0.02]
initial_points = [[-1], [1], [0]]

for lr in learning_rates:
    for init in initial_points:
        x_min = gradient_descent(lambda x: np.array([df(x)]), x_init=init, learning_rate=lr)
        print(f"Start: {init}, learning rate: {lr}, minimum: {x_min[0]}")
