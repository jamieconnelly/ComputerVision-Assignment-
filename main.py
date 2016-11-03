from Tkinter import *
from compare import Mosaic
from tkFileDialog import askopenfilename, askdirectory
import numpy as np

root = Tk()
root.minsize(width=400, height=400)
image_path = None
src_dir = None


# Define widget callbacks
def start_btn_cb(img_h, img_w):
    img_h = int(img_h.get())
    img_w = int(img_w.get())
    mos = Mosaic(image_path, (img_h, img_w), 10, src_dir, 'Intersection', 'out')
    mos.create_mosaic()


def open_img_btn_cb():
    global image_path
    image_path = askopenfilename()


def open_dir():
    global src_dir
    src_dir = askdirectory()


# Define widgets
img_w_lbl = Label(root, text="Image Width")
img_w_val = Entry(root, bd=1)
img_h_lbl = Label(root, text="Image Height")
img_h_val = Entry(root, bd=1)
open_img_btn = Button(root, text ="Load Image", command=open_img_btn_cb)
source_dir = Button(root, text ="Choose Source Dir", command=open_dir)
start_btn = Button(root, text ="Start",
                   command=lambda w=img_w_val, h=img_h_val: start_btn_cb(w, h))


# Pack widgets
start_btn.pack(side=BOTTOM, fill=X)
open_img_btn.pack(side=BOTTOM, fill=X)
source_dir.pack(side=BOTTOM,fill=X)
img_w_lbl.pack()
img_w_val.pack()
img_h_lbl.pack()
img_h_val.pack()    
root.mainloop()
