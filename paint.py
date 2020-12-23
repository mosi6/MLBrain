from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import ImageGrab
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from machineLearn3 import *



class Paint(object):

    DEFAULT_PEN_SIZE = 30
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.xscreen = self.root.winfo_screenwidth()//2-150
        self.yscreen = self.root.winfo_screenheight()//2-172
        self.root.geometry(f"300x344+{self.xscreen}+{self.yscreen}")

        self.pen_button = Button(self.root, text='clear', command=self.erase_all)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='save', command=self.save)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=50, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)
        self.choose_size_button.set(30)
        self.c = Canvas(self.root, bg='white', width=300, height=300)
        self.c.grid(row=1, columnspan=5)
        self.setup()
        self.root.mainloop()


    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 30
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.brush_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.parameters=ReadDict(name="NNt")


    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            ImageGrab.grab((300,300,300,300))
        self.old_x = event.x
        self.old_y = event.y

    def erase_all(self):
        paint_color = 'white'
        self.c.create_line(0, 0, 300, 300,
                               width=1000, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
    def save(self):
        self.root.geometry(f'+{self.xscreen}+{self.yscreen}')
        self.root.update()
        filename = 'image.png'
        img=ImageGrab.grab((self.xscreen+10, self.yscreen+75, self.xscreen+308, self.yscreen+373))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        #img = cv2.resize(img, (20, 20), interpolation=cv2.INTER_AREA)
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)


        img = 255 - img
        plt.imshow(img, cmap = plt.cm.gray_r, interpolation = 'nearest')

        #print(img)
        img = np.array([img.flatten()])
        apply_on_example(img,self.parameters)
        plt.show()
    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()
