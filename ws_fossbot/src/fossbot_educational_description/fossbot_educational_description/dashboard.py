#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry

class Dashboard(Node):
    def __init__(self):
        super().__init__('dashboard')
        self.subscription_vel = self.create_subscription(Twist, 'cmd_vel', self.cmd_callback, 10)
        self.subscription_odom = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)

        self.vx = 0.0
        self.vy = 0.0
        self.omega = 0.0

        self.x = 0.0
        self.y = 0.0

    def cmd_callback(self, msg: Twist):
        self.vx = msg.linear.x
        self.vy = msg.linear.y
        self.omega = msg.angular.z

    def odom_callback(self, msg: Odometry):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        self.x = position.x
        self.y = position.y

    def plot_dashboard(self):    
        plt.ion()
        fig, axs = plt.subplots(2, 1, figsize=(8, 6))
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0)
            axs[0].cla()
            axs[1].cla()

            # Plot velocities
            axs[0].bar(['Vx', 'Vy', 'Omega'], [self.vx, self.vy, self.omega], color=['blue', 'orange', 'green'])
            axs[0].set_ylim(-2, 2)
            axs[0].set_title('Velocities')
            axs[0].set_ylabel('m/s or rad/s')

            # Plot position
            axs[1].scatter(self.x, self.y, color='red')
            axs[1].set_xlim(-2, 2)
            axs[1].set_ylim(-2, 2)
            axs[1].set_title('Position')
            axs[1].set_xlabel('X (m)')
            axs[1].set_ylabel('Y (m)')

            plt.pause(0.1)

def main(args=None):
    rclpy.init(args=args)
    dashboard_node = Dashboard()
    try:
        dashboard_node.plot_dashboard()
    except KeyboardInterrupt:
        pass
    finally:
        dashboard_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

