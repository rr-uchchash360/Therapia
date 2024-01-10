import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class ArmVisualization:
    def __init__(self, arm_length=1.5):
        self.arm_length = arm_length

        # Create a 3D plot
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Set axis labels
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Z-axis')  # Swap y-axis and z-axis
        self.ax.set_zlabel('Y-axis')  # Swap y-axis and z-axis

        # Set plot limits
        self.ax.set_xlim([-self.arm_length, self.arm_length])
        self.ax.set_ylim([-self.arm_length, self.arm_length])
        self.ax.set_zlim([0, 2 * self.arm_length])

        # Set aspect ratio
        self.ax.set_box_aspect([np.ptp(axis) for axis in [self.ax.get_xlim(), self.ax.get_ylim(), self.ax.get_zlim()]])
        self.ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.5)  # Add a grid

        # Initialize line objects for the arm and neck
        self.arm_line, = self.ax.plot([], [], [], linewidth=2, label='Arm', color='blue')
        self.shoulder_point, = self.ax.plot([], [], [], marker='o', markersize=8, color='red', label='Shoulder')
        self.elbow_point, = self.ax.plot([], [], [], marker='o', markersize=8, color='orange', label='Elbow')
        self.wrist_point, = self.ax.plot([], [], [], marker='o', markersize=8, color='green', label='Wrist')
        self.neck_line, = self.ax.plot([], [], [], linewidth=2, label='Neck', color='purple')
        self.hand_point, = self.ax.plot([], [], [], marker='o', markersize=8, color='brown', label='Hand')

        # Add a legend
        self.ax.legend()

        # Create an animation
        self.animation = FuncAnimation(self.fig, self.update, frames=np.arange(0, 360, 5), blit=True)

    def forward_kinematics(self, shoulder_angle, elbow_angle, wrist_abduction_angle):
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
        end_effector_scaled = (self.arm_length / np.linalg.norm(end_effector)) * end_effector

        return end_effector_scaled

    def update(self, frame):
        # Your sensor data processing code here...
        shoulder_angle, elbow_angle, wrist_abduction_angle = self.process_sensor_data(frame)

        # Calculate the wrist position
        wrist_position = self.forward_kinematics(shoulder_angle, elbow_angle, wrist_abduction_angle)

        # Update arm line
        self.arm_line.set_xdata([0, wrist_position[0]])
        self.arm_line.set_ydata([0, wrist_position[2]])  # Swap y and z
        self.arm_line.set_3d_properties([0, wrist_position[1]])  # Swap y and z

        # Update shoulder, elbow, and wrist points
        self.shoulder_point.set_data([0], [0])
        self.shoulder_point.set_3d_properties([0])

        self.elbow_point.set_data([wrist_position[0]], [wrist_position[2]])  # Swap y and z
        self.elbow_point.set_3d_properties([wrist_position[1]])  # Swap y and z

        self.wrist_point.set_data([wrist_position[0]], [wrist_position[2]])  # Swap y and z
        self.wrist_point.set_3d_properties([wrist_position[1]])  # Swap y and z

        # Update neck line
        self.neck_line.set_xdata([0, 0])
        self.neck_line.set_ydata([0, 0])
        self.neck_line.set_3d_properties([0, self.arm_length])  # You can adjust the length of the neck as needed

        # Update hand point
        self.hand_point.set_data([wrist_position[0]], [wrist_position[2]])  # Swap y and z
        self.hand_point.set_3d_properties([wrist_position[1]])  # Swap y and z

        return self.arm_line, self.shoulder_point, self.elbow_point, self.wrist_point, self.neck_line, self.hand_point

    def process_sensor_data(self, frame):
        # Your sensor data processing code here...
        # For demonstration purposes, using simple sine and cosine functions
        shoulder_angle = np.radians(45)  # Fix the shoulder angle
        elbow_angle = np.radians(frame)
        wrist_abduction_angle = np.radians(frame)

        return shoulder_angle, elbow_angle, wrist_abduction_angle

    def show_animation(self):
        plt.show()

# Example of using the ArmVisualization class
if __name__ == "__main__":
    arm_visualizer = ArmVisualization(arm_length=1.5)
    arm_visualizer.show_animation()
