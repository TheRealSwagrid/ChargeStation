#!/usr/bin/env python
import os
import socket

import numpy as np
import rospy
from AbstractVirtualCapability import VirtualCapabilityServer
import tf
from visualization_msgs.msg import Marker
from ChargeStation import ChargeStation

if __name__ == '__main__':
    rospy.init_node('rosnode', xmlrpc_port=int(os.environ["xmlrpc_port"]), tcpros_port=int(os.environ["tcpros_port"]))
    rate = rospy.Rate(25)
    server = VirtualCapabilityServer(int(rospy.get_param('~semantix_port')), socket.gethostbyname(socket.gethostname()))
    station = ChargeStation(server)
    station.uri = "ChargeStation"
    station.start()

    br = tf.TransformBroadcaster()
    pub = rospy.Publisher(f"/robot", Marker, queue_size=1)
    name = f"chargestation@{int(rospy.get_param('~semantix_port'))}"

    position = [10., 2., 0.]
    rotation = [0., 0., 0., 1.]
    scale = 1.

    station.functionality["get_pos"] = lambda: position

    while not rospy.is_shutdown():
        marker = Marker()
        marker.id = 105
        marker.header.frame_id = "world"
        marker.header.stamp = rospy.Time.now()
        marker.ns = f"chargestation@{int(rospy.get_param('~semantix_port'))}"
        marker.lifetime = rospy.Duration(0)
        marker.mesh_use_embedded_materials = True
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = position[2]
        marker.pose.orientation.x = rotation[0]
        marker.pose.orientation.y = rotation[1]
        marker.pose.orientation.z = rotation[2]
        marker.pose.orientation.w = rotation[3]
        # Scale down
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        marker.color.a = 1
        marker.type = Marker.MESH_RESOURCE
        marker.action = Marker.ADD
        marker.mesh_resource = r"package://chargestationhandler/meshes/charge_station.dae"
        pub.publish(marker)
        br.sendTransform(position, rotation, rospy.Time.now(), name, "world")

        rate.sleep()
