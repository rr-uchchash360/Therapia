import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Function for forward kinematics
def forward_kinematics(theta1, theta2, theta3, l1, l2, l3):
    # Convert degrees to radians
    theta1 = np.deg2rad(theta1)
    theta2 = np.deg2rad(theta2)
    theta3 = np.deg2rad(theta3)

    # DH parameters for the 3-link arm
    dh_parameters = [
        [0, 0, l1, theta1],
        [l2, 0, 0, theta2],
        [l3, 0, 0, theta3]
    ]

    # Initialize transformation matrix
    T = np.eye(4)

    for dh in dh_parameters:
        a, alpha, d, theta = dh

        # Individual transformation matrices
        A_i = np.array([
            [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
            [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]
        ])

        # Update overall transformation matrix
        T = np.dot(T, A_i)

    # Extract end-effector position
    end_effector_pos = T[:3, 3]

    return end_effector_pos

# Function to update arm configuration for animation
def update(frame):
    # Joint angles (in degrees) - You can update these angles in real-time
    theta1 = frame * 2  # Example: Simple animation increasing theta1
    theta2 = frame * 1.5  # Example: Simple animation increasing theta2
    theta3 = frame * 1  # Example: Simple animation increasing theta3
    
    # Link lengths
    l1 = 2
    l2 = 3
    l3 = 2.5

    # Calculate end-effector position
    end_effector_position = forward_kinematics(theta1, theta2, theta3, l1, l2, l3)

    # Update arm segments with different colors for shoulder, elbow, and wrist
    shoulder_color = 'blue'
    elbow_color = 'red'
    wrist_color = 'green'

    shoulder_segment = np.array([[0, 0, 0], [l1, 0, 0]])
    elbow_segment = np.array([[l1, 0, 0], [l1 + l2 * np.cos(np.deg2rad(theta2)), l2 * np.sin(np.deg2rad(theta2)), 0]])
    wrist_segment = np.array([[l1 + l2 * np.cos(np.deg2rad(theta2)), l2 * np.sin(np.deg2rad(theta2)), 0], end_effector_position])

    # Clear previous plot and plot new arm configuration with different colors
    ax.clear()
    ax.plot(shoulder_segment[:, 0], shoulder_segment[:, 1], shoulder_segment[:, 2], marker='o', color=shoulder_color)
    ax.plot(elbow_segment[:, 0], elbow_segment[:, 1], elbow_segment[:, 2], marker='o', color=elbow_color)
    ax.plot(wrist_segment[:, 0], wrist_segment[:, 1], wrist_segment[:, 2], marker='o', color=wrist_color)

    # Setting plot attributes
    ax.set_xlim([-l1 - l2 - l3, l1 + l2 + l3])
    ax.set_ylim([-l1 - l2 - l3, l1 + l2 + l3])
    ax.set_zlim([-l1 - l2 - l3, l1 + l2 + l3])
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('3-Link 3D Arm Visualization using Denavit Hartenberg Forward Kinematics')

# Create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the number of frames for animation
num_frames = 100

# Create animation
ani = FuncAnimation(fig, update, frames=num_frames, interval=100)
plt.show()