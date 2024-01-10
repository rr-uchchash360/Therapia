import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

def forward_kinematics(shoulder_angle, elbow_angle, wrist_abduction_angle, arm_length):
    # Define DH parameters
    d_shoulder_elbow, a_shoulder_elbow, alpha_shoulder_elbow = 0, 1, 0
    d_elbow_wrist, a_elbow_wrist, alpha_elbow_wrist = 0, 1, 0
    d_wrist_hand, a_wrist_hand, alpha_wrist_hand = 0, 1, 0

    # Homogeneous transformations
    T_shoulder_elbow = np.array([[np.cos(shoulder_angle), -np.sin(shoulder_angle), 0, a_shoulder_elbow],
                                  [np.sin(shoulder_angle), np.cos(shoulder_angle), 0, 0],
                                  [0, 0, 1, d_shoulder_elbow],
                                  [0, 0, 0, 1]])

    T_elbow_wrist = np.array([[np.cos(elbow_angle), -np.sin(elbow_angle), 0, a_elbow_wrist],
                              [np.sin(elbow_angle), np.cos(elbow_angle), 0, 0],
                              [0, 0, 1, d_elbow_wrist],
                              [0, 0, 0, 1]])

    T_wrist_hand = np.array([[np.cos(wrist_abduction_angle), -np.sin(wrist_abduction_angle), 0, a_wrist_hand],
                             [np.sin(wrist_abduction_angle), np.cos(wrist_abduction_angle), 0, 0],
                             [0, 0, 1, d_wrist_hand],
                             [0, 0, 0, 1]])

    T_shoulder_hand = np.dot(np.dot(T_shoulder_elbow, T_elbow_wrist), T_wrist_hand)

    # Extract end-effector position
    end_effector = T_shoulder_hand[:3, 3]

    # Scale the end-effector position to maintain constant arm length
    end_effector_scaled = (arm_length / np.linalg.norm(end_effector)) * end_effector

    return end_effector_scaled

# Create a 3D plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Set axis labels
ax.set_xlabel('X-axis')
ax.set_ylabel('Z-axis')  # Swap y-axis and z-axis
ax.set_zlabel('Y-axis')  # Swap y-axis and z-axis

# Set plot limits
arm_length = 1.5
ax.set_xlim([-arm_length, arm_length])
ax.set_ylim([-arm_length, arm_length])
ax.set_zlim([0, 2 * arm_length])

# Set aspect ratio
ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.5)  # Add a grid

# Initialize line objects for the arm and neck
arm_line, = ax.plot([], [], [], linewidth=2, label='Arm', color='blue')
shoulder_point, = ax.plot([], [], [], marker='o', markersize=8, color='red', label='Shoulder')
elbow_point, = ax.plot([], [], [], marker='o', markersize=8, color='orange', label='Elbow')
wrist_point, = ax.plot([], [], [], marker='o', markersize=8, color='green', label='Wrist')
neck_line, = ax.plot([], [], [], linewidth=2, label='Neck', color='purple')
hand_point, = ax.plot([], [], [], marker='o', markersize=8, color='brown', label='Hand')

# Add a legend
ax.legend()

# Update function for animation
def update(frame):
    shoulder_angle = np.radians(45)  # Fix the shoulder angle
    elbow_angle = np.radians(frame)
    wrist_abduction_angle = np.radians(frame)
    
    # Calculate the wrist position
    wrist_position = forward_kinematics(shoulder_angle, elbow_angle, wrist_abduction_angle, arm_length)

    # Update arm line
    arm_line.set_xdata([0, wrist_position[0]])
    arm_line.set_ydata([0, wrist_position[2]])  # Swap y and z
    arm_line.set_3d_properties([0, wrist_position[1]])  # Swap y and z

    # Update shoulder, elbow, and wrist points
    shoulder_point.set_data([0], [0])
    shoulder_point.set_3d_properties([0])

    elbow_point.set_data([wrist_position[0]], [wrist_position[2]])  # Swap y and z
    elbow_point.set_3d_properties([wrist_position[1]])  # Swap y and z

    wrist_point.set_data([wrist_position[0]], [wrist_position[2]])  # Swap y and z
    wrist_point.set_3d_properties([wrist_position[1]])  # Swap y and z

    # Update neck line
    neck_line.set_xdata([0, 0])
    neck_line.set_ydata([0, 0])
    neck_line.set_3d_properties([0, arm_length])  # You can adjust the length of the neck as needed

    # Update hand point
    hand_point.set_data([wrist_position[0]], [wrist_position[2]])  # Swap y and z
    hand_point.set_3d_properties([wrist_position[1]])  # Swap y and z

    return arm_line, shoulder_point, elbow_point, wrist_point, neck_line, hand_point

# Create an animation
animation = FuncAnimation(fig, update, frames=np.arange(0, 360, 20), blit=True)

# Show the plot
plt.show()
