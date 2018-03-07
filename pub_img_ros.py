#!/usr/bin/env python

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import rospy
import cv2

if __name__ == '__main__':
    rospy.init_node('img_publisher')
    img = cv2.imread('qrcore.jpg')
    pub = rospy.Publisher('/img', Image, queue_size=1)
    bridge = CvBridge()
    img_msg = bridge.cv2_to_imgmsg(img, "bgr8")
    while not rospy.is_shutdown():
        pub.publish(img_msg)
        rospy.sleep(0.1)
