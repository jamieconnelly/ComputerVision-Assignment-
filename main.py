from Tkinter import *
from compare import Compare
from tkFileDialog import askopenfilename, askdirectory
import numpy as np

root = Tk()
root.minsize(width=400, height=400)
root.resizable(width=False, height=False)
image_path = None
src_dir = None
tile_size = StringVar(root)
tile_size.set("5")
hist_var= StringVar(root)
hist_var.set("Correlation")



# Define widget callbacks
def start_btn_cb(val):
    tiles = int(val.get())
    tile_val=int(tile_size.get())
    filename_out=filename_text.get() + ".jpg"
    x = Compare(image_path, (1680, 1120), 8000, src_dir)
    x.create_mosaic()


def open_img_btn_cb():
    global image_path
    image_path = askopenfilename()


def open_dir():
    global src_dir
    src_dir = askdirectory()

def exit_btn():
	exit()
	
# Define widgets
tile_no_lbl = Label(root, text="Number of tiles")
filename_lbl = Label(root, text="Choose Output name")
filename_text = Entry(root)
tile_no_val = Entry(root, bd=1)
open_img_btn = Button(root, text ="Load Image", command=open_img_btn_cb)
source_dir=Button(root, text ="Choose Source Dir", command=open_dir)
start_btn = Button(root, text ="Start", command=lambda v=tile_no_val: start_btn_cb(v))
exit_btn = Button(root, text="Exit", command=exit_btn)

size_picker_lbl = Label(root, text="Pick Tile Size")
size_picker = OptionMenu(root, tile_size, "5","10","20","30")

hist_comp_lbl = Label(root, text="Pick Histogram Comparison")
hist_comp = OptionMenu(root, hist_var, "Correlation","Chi-Squared","Intersection","Hellinger")


# Pack widgets
exit_btn.pack(side=BOTTOM,fill=X)
start_btn.pack(side=BOTTOM, fill=X)
open_img_btn.pack(side=BOTTOM, fill=X)
source_dir.pack(side=TOP,fill=X)



#~ tile_no_lbl.place(x=0,y=220)
#~ tile_no_val.place(x=235, y=220)

size_picker.place( x=235, y=160)
size_picker_lbl.place(x=0, y=160)

filename_lbl.place(x=0, y=100)
filename_text.place(x=235, y=100)

hist_comp_lbl.place(x=0, y=125)
hist_comp.place(x=235, y=125,w=120)




root.mainloop()
