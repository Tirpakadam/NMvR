import tkinter as tk
import csv
import numpy as np


with open("map.csv", encoding='utf-8-sig') as file_name:
    array = np.loadtxt(file_name, delimiter=";")

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


rectangles = []

root = tk.Tk()
cv = tk.Canvas(root, height=1200, width=1200)
def processMouseEvent(event):
        mouse_coordinates= str(event.x) + ", " + str(event.y)
        cv.create_text(event.x, event.y, text = mouse_coordinates)
        print(mouse_coordinates)
cv.pack()
cv.bind('<Button-1>', onclick)



for x in range(100):
   for y in range(100):
     cv.create_rectangle(10+x*10, 10+y*10, 20+x*10, 20+y*10, tags=('rect'))
x=0
y=0
for x in range(100):
   for y in range(100):
     if((array[x][y])==1.0):
       cv.create_rectangle(10+x*10,10+y*10,10+x*10+10,10+y*10+10, tags=('rect'),fill='black')




root.mainloop()
