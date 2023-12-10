from src.commander import Commander
import sys
import copy
import rospy
import moveit_commander
from math import tau
import numpy as np
from tf.transformations import quaternion_from_euler


class ROSCommander(Commander):

    step_size = 0.05
     
    def __init__(self):
        # Initialize the moveit_commander and rospy nodes
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('3d_printer', anonymous=True)

        # Instantiate a RobotCommander object. This object is an interface to the robot as a whole.
        self.robot = moveit_commander.RobotCommander()

        # Instantiate a PlanningSceneInterface object. This object is an interface to the world surrounding the robot.
        self.scene = moveit_commander.PlanningSceneInterface()

        # Load UR5e as the robot model
        self.group_name = 'manipulator'
        self.move_group = moveit_commander.MoveGroupCommander(self.group_name)

        # Create a DisplayTrajectory ROS publisher which is used to display trajectories in Rviz
        # display_trajectory_publisher = rospy.Publisher(
        #     "/move_group/display_planned_path",
        #     moveit_msgs.msg.DisplayTrajectory,
        #     queue_size=20,
        # )
         
    def orient_wrist(self):
        '''
        Orient the wrist to the given angle
        '''
        # Get the current joint values
        joint_goal = self.move_group.get_current_joint_values()

        # Set the wrist rotation to the given angle to be vertical
        # That is, it should be the sum of the shoulder, elbow, and wrist angles
        joint_goal[3] = -tau/4 - joint_goal[1] - joint_goal[2]
        joint_goal[4] = -tau/4 #Wrist Rotation

        # Move the robot to the given joint values
        self.move_group.go(joint_goal, wait=True)

        # Calling ``stop()`` ensures that there is no residual movement
        self.move_group.stop()

    def move_g0(self, x: float, y: float, z: float):
        '''
        Move the robot to the given position
        '''
        # Move the robot along the path
        print(f'Emitting G0 command: {x}, {y}, {z}')
        # self.orient_wrist()
        self.move_robot_along_path(np.array([[[x, y, z]]]))
     
    def move_g1(self, x: float, y: float, z: float, e: float, f: float):
        '''
        Move the robot to the given position and extrude
        '''
        # Move the robot along the path
        print(f'Emitting G1 command: {x}, {y}, {z}, {e}, {f}')
        # self.orient_wrist()
        self.move_robot_along_path(np.array([[[x, y, z]]]))
     
    def start_sequence(self):
        """Moves the robot to the start position"""

        # Set the robot back to the home position before starting the script
        self.move_group.set_named_target("home")
        plan_home = self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        # Get robot in "ready" position
        joint_goal = self.move_group.get_current_joint_values()
        joint_goal[0] = 0 #Slew
        joint_goal[1] = -tau / 4 #Shoulder
        joint_goal[2] = tau/4 #Elbow
        joint_goal[3] = -tau/4 #Wrist
        joint_goal[4] = -tau/4 #Wrist Rotation
        joint_goal[5] = tau / 6 #Gripper

        # The go command can be called with joint values, poses, or without any
        # parameters if you have already set the pose or joint target for the group
        self.move_group.go(joint_goal, wait=True)

        # Calling ``stop()`` ensures that there is no residual movement
        self.move_group.stop()

        # Print the current pose of the end-effector to the terminal
        current_pose = self.move_group.get_current_pose().pose
        print("Starting pose:", current_pose)
        
    def route_cartesian(self, waypoints: list):
        """Moves the robot along a path defined by the waypoints"""
        plan, fraction = self.move_group.compute_cartesian_path(
                            waypoints,  # waypoints to follow
                            self.step_size,  # eef_step
                            0.0,  # jump_threshold
                        )

        # Note: We are just planning, not asking move_group to actually move the robot yet
        print("Fraction:", fraction)
        print("Plan:", plan)

        # Move the robot
        self.move_group.execute(plan, wait=True)

    def gen_waypoints(self, points: np.ndarray) -> list:
        """Returns a list of waypoints for the robot to follow"""
        waypoints = []
        for point in points:
            # Copy the current pose of the end-effector
            waypoints.append(copy.deepcopy(self.move_group.get_current_pose().pose))

            # Move the end-effector to the next point
            waypoints[-1].position.x = point[0]
            waypoints[-1].position.y = point[1]
            waypoints[-1].position.z = point[2]

            # Set the end-effector's orientation

            # Quaternion for a vertical wrist
            oritentation = quaternion_from_euler(tau/2, 0, 0)
            waypoints[-1].orientation.x = oritentation[0]
            waypoints[-1].orientation.y = oritentation[1]
            waypoints[-1].orientation.z = oritentation[2]
            waypoints[-1].orientation.w = oritentation[3]

        return waypoints
    
    def move_robot_along_path(self, points: list):
        """Moves the robot along a path defined by the points"""
        # Create a list of waypoints marking out the letters
        print(f'Points: {points}')  
        waypoints_list = [self.gen_waypoints(points_i) for points_i in points]

        # Move the robot along the paths
        for waypoints in waypoints_list:

            # Move the robot along the path
            self.route_cartesian(waypoints)


def main():

    # Create a Commander object
    commander = ROSCommander()

    # Move the robot to the start position
    commander.start_sequence()

    # Define the points that the robot will move to
    points = np.array([[
        [0.5, 0.0, 0.1],
        [0.5, 0.0, 0.2],
        [0.5, 0.0, 0.3],
        [0.5, 0.0, 0.4],
        [0.5, 0.0, 0.5],
        [0.5, 0.0, 0.6],
        [0.5, 0.0, 0.7],
        [0.5, 0.0, 0.8],
        [0.5, 0.0, 0.9],
        [0.5, 0.0, 1.0],
    ]])

    # Move the robot along the path
    commander.move_robot_along_path(points)


if __name__ == '__main__':
    main()
