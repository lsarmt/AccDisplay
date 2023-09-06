
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

file_path = filedialog.askopenfilename()

if file_path:
    print("You chose:", file_path)
else:
    print("No file selected.")
# file_name = input("Please enter a file name: ")
# directory_path = Path("path/to/directory")
# modified_path = directory_path / file_name  # Uses the / operator for path concatenation
# print("Modified path:", modified_path)
# Load data from Excel file
excel_file = file_path

df = pd.read_excel(excel_file)

# Extract data from DataFrame
acc_x = df['ACC_X'].values
acc_y = df['ACC_Y'].values
acc_z = df['ACC_Z'].values
gyro_x = df['GYRO_X'].values
gyro_y = df['GYRO_Y'].values
gyro_z = df['GYRO_Z'].values
time = df['TIME'].values
# Conversion factors
accel_scale = 9.81  # m/s^2
gyro_scale = 0.0175  # deg/s

# Initialize starting orientation
pitch = math.degrees(math.atan2(acc_x[0], math.sqrt(acc_y[0]**2 + acc_z[0]**2)))
roll = math.degrees(math.atan2(acc_y[0], math.sqrt(acc_x[0]**2 + acc_z[0]**2)))
yaw = 0

# Create lists to store orientation and position data
orientations = [(pitch, roll, yaw)]
positions = [(0, 0, 0)]

# Simulate movement over time
for i in range(1, len(time)):
    dt = time[i] - time[i - 1]
    
    # Update orientation using gyroscope data
    delta_pitch = gyro_x[i] * gyro_scale * dt
    delta_roll = gyro_y[i] * gyro_scale * dt
    delta_yaw = gyro_z[i] * gyro_scale * dt

    pitch += delta_pitch
    roll += delta_roll
    yaw += delta_yaw

    # Update position using accelerometer data
    delta_position = np.array([acc_x[i], acc_y[i], acc_z[i]]) * accel_scale * dt
    
    current_position = np.array(positions[-1]) + delta_position
    positions.append(tuple(current_position))

    orientations.append((pitch, roll, yaw))

# Extract data for plotting
xs, ys, zs = zip(*positions)
pitch_list, roll_list, yaw_list = zip(*orientations)

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the device movement
ax.plot(xs, ys, zs, label='Device Movement')
ax.scatter(xs[-1], ys[-1], zs[-1], color='red', label='Final Position')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Device Movement in 3D Space')
ax.legend()

plt.show()
