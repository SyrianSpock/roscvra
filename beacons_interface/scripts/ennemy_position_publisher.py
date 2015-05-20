#!/usr/bin/env python3
import serial
import time
import rospy
from cvra_msgs.msg import EnnemyPosition

def ennemy_pos_publish(robot, x, y, var_x, var_y, cov_xy):
    ennemy = EnnemyPosition()

    now = rospy.Time.now()
    ennemy.header.stamp.secs = now.secs
    ennemy.header.stamp.nsecs = now.nsecs

    ennemy.robot_id = str(int(robot))
    ennemy.x = x
    ennemy.y = y
    ennemy.covariance = [ var_x, cov_xy,
                         cov_xy,  var_y]

    if robot == 1:
        pub_ennemy_1.publish(ennemy)
    elif robot == 2:
        pub_ennemy_2.publish(ennemy)
    else:
        raise ValueError('Robot ID unhandled (not 1 or 2)')

if __name__ == '__main__':
    # Setup serial interface
    port = rospy.get_param("/debra/beacons/port")
    baud = rospy.get_param("/debra/beacons/baud")
    serial = serial.Serial(port=port, baudrate=baud)
    stream = ""

    try:
        # Setup publisher
        pub_ennemy_1 = rospy.Publisher('ennemy_1', EnnemyPosition, queue_size=0)
        pub_ennemy_2 = rospy.Publisher('ennemy_2', EnnemyPosition, queue_size=0)
        rospy.init_node('ennemy_position', anonymous=True)
        rate = rospy.Rate(10) # Run at 10 Hz

        while not rospy.is_shutdown():
            # Get serial data
            stream += serial.readline().decode("ascii")
            data = stream.split("\n")

            for line in data:
                if len(line.split(" ")) == 6:
                    try:
                        robot, x, y, var_x, var_y, cov_xy = tuple(map(float, line.split()))
                        ennemy_pos_publish(robot, x, y, var_x, var_y, cov_xy) # Publish
                    except:
                        pass
                rate.sleep()
    except rospy.ROSInterruptException:
        pass
