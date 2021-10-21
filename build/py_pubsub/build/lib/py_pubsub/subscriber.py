import rclpy
import numpy as np
import tkinter as tk
import threading
import time
from rclpy.node import Node
from PIL import ImageTk, Image  

from std_msgs.msg import Float64MultiArray

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

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Float64MultiArray,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        global array
        self.get_logger().info('I heard: "%s"' % msg.data)
        array=np.reshape(msg.data,(100,100))

def map():
    rectangles = []
    cv.pack()
    cv.bind('<Button-1>', onclick)
    for x in range(100):
       for y in range(100):
          cv.create_rectangle(10+x*10, 10+y*10, 20+x*10, 20+y*10, tags=('rect'))
    x=0
    y=0
    for x in range(100):
       for y in range(100):
          if(((array)[x][y])==1.0):
             cv.create_rectangle(10+x*10,10+y*10,10+x*10+10,10+y*10+10, tags=('rect'),fill='black')

    image1 = Image.open("index.png")
    image1 = image1.resize((30, 30), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image=test)
    label1.image = test
    label1.place(x=50, y=100)
    root.mainloop()
   
def listening(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin_once(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

def main(args=None):
    listening()
    mapa=threading.Thread(target=map())
    mapa.start()

if __name__ == '__main__':
     main()
