from Tkinter import *
from compare import Compare
from tkFileDialog import askopenfilename

root = Tk()
root.minsize(width=400, height=400)
image_path = None

# Define widget callbacks
def start_btn_cb(val):
    tiles = int(val.get())
    x = Compare(image_path, (800, 600), 8000)
    x.create_mosaic()


def open_img_btn_cb():
    global image_path
    image_path = askopenfilename()


# Define widgets
tile_no_lbl = Label(root, text="Number of tiles")
tile_no_val = Entry(root, bd=1)
open_img_btn = Button(root, text ="Load Image", command=open_img_btn_cb)
start_btn = Button(root, text ="Start", command=lambda v=tile_no_val: start_btn_cb(v))


# Pack widgets
start_btn.pack(side=BOTTOM, fill=X)
open_img_btn.pack(side=BOTTOM, fill=X)
tile_no_lbl.pack(side=LEFT)
tile_no_val.pack(side=RIGHT)

root.mainloop()