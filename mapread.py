import rclpy
import numpy as np
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

with open("map.csv", encoding='utf-8-sig') as file_name:
    array = np.loadtxt(file_name, delimiter=";")
a=array.ravel()
listed = list(a)



class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Float64MultiArray, 'topic', 10)
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Float64MultiArray()
        msg.data = listed
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data )
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
