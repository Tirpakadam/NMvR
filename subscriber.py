import rclpy
import numpy as np
import tkinter as tk
import threading
import time
from rclpy.node import Node
from PIL import ImageTk, Image
from math import sqrt, pow

from std_msgs.msg import Float64MultiArray
from std_msgs.msg import String

root = tk.Tk()
cv = tk.Canvas(root, height=1000, width=1000)
array=np.zeros((100,100))
   
def onclick(event):
    global rectangles
    item = cv.find_closest(event.x, event.y)
    if 'rect' in cv.gettags(item):
        current_color = cv.itemcget(item, 'fill')

        if current_color == 'black':
            cv.itemconfig(item, fill='white')
        else:
            cv.itemconfig(item, fill='black')
    mouse_x= (event.x)//10-1
    mouse_y=(event.y)//10-1
    if (array[mouse_x][mouse_y]==0) :
     array[mouse_x][mouse_y]=1
    elif (array[mouse_x][mouse_y]==1) :
     array[mouse_x][mouse_y]=0
    np.savetxt("map.csv",array, delimiter=";")




class Poloha_Publisher(Node):

    def __init__(self):
        super().__init__('publisher') # ako sa ma volat node
        self.publisher = self.create_publisher(String, 'poloha', 10)
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.rychlost = 0

    def timer_callback(self):
        print('in pub ', self.angular) 
        msg = String()
        msg.data = str(self.linear)
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)


class Poloha_Subscriber(Node):

    def __init__(self):
        super().__init__('subscriber')
        self.subscription = self.create_subscription(String, 'poloha', self.listener_callback, 10)
        self.robotx = 1
        self.roboty = 1
        self.rychlost=1
        self.uhol = 1
        self.cielx = 0
        self.ciely = 0

    def listener_callback(self, msg):
        self.linear = float(msg.data.split(",")[0])
        dcenter = self.linear
       #prevod stupne treba atd...
        self.robotx += round(rychlost * cos(self.uhol), 1)
        self.roboty += round(rychlost * sin(self.uhol), 1)

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')

        self.subscription = self.create_subscription(
            Float64MultiArray,
            'Map',
            self.listener_callback,
            10)

        self.subscription2 = self.create_subscription(
            String,
            'topic',
            self.listener_callback2,
            10)
        self.robotx = 1
        self.roboty = 1
        self.rychlost=1
        self.uhol = 0
        self.cielx = 0
        self.ciely = 0
        self.rectangles = []
        self.robot = Image.open("index.png")
        self.robot = self.robot.resize((10, 10), Image.ANTIALIAS)
        self.test = ImageTk.PhotoImage(self.robot)
        self.label1 = tk.Label(image=self.test)
        self.label1.image = self.test
        self.label1.place(x=self.robotx*10, y=self.roboty*10)

  
    def map(self,msg):

        
        cv.pack()
        cv.bind('<Button-1>', onclick)
        for x in range(100):
           for y in range(100):
              cv.create_rectangle(10+x*10, 10+y*10, 20+x*10, 20+y*10, tags=('rect'))
        x=0
        y=0
        for x in range(100):
           for y in range(100):
              if(((msg)[x][y])==1.0):
                 cv.create_rectangle(10+x*10,10+y*10,10+x*10+10,10+y*10+10, tags=('rect'),fill='black')
        
       
        

        root.update()

    def vzdialenost(self,robotx,roboty,cielx,ciely):
        return sqrt((pow(( self.cielx - self.robotx), 2) + pow((self.ciely - self.roboty), 2))) 

    def rychlost(self):
        self.rychlost = self.distance() * 2 

    def listener_callback(self, msg):
        array=np.reshape(msg.data,(100,100))
        self.map(array)
   
       
    def listener_callback2(self, msg):
        make,robot_x,robot_y, ciel_x,ciel_y = msg.data.split('.')
        if (make == "Move"):
            self.get_logger().info('send')
            self.label1.place_forget()

            self.cielx = int(ciel_x)
            self.ciely = int(ciel_y)

            

            cv.create_rectangle(self.cielx*10,self.ciely*10,self.cielx*10+10,self.ciely*10+10, tags=('rect'),fill='red')
            print(self.robotx,self.roboty,self.cielx,self.ciely)
            print(self.vzdialenost(self.robotx,self.roboty,self.cielx,self.ciely))

            if(self.robotx<self.cielx):
                self.robotx=self.robotx+self.rychlost
                 

            if(self.roboty<self.ciely):
                self.roboty=self.roboty+self.rychlost
            
            self.label1.place(x=self.robotx*10, y=self.roboty*10)




   
def listening(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

def main(args=None):
    listening()


if __name__ == '__main__':
     main()
