from Tkinter import *
from mosaic import Mosaic
from tkFileDialog import askopenfilename, askdirectory
import numpy as np
import time

root = Tk()
root.minsize(width=400, height=400)
root.resizable(width=False, height=False)
image_path = None
src_dir = None
tile_size = StringVar(root)
tile_size.set("5")
hist_var= StringVar(root)
hist_var.set("Correlation")

img_w = IntVar()
img_h = IntVar()
img_w.set(800)
img_h.set(600)


# Define widget callbacks
def start_btn_cb():
    if errors(img_w,img_h):
        exit()
        
    tile_val=int(tile_size.get())
    #filename_out= "/" + filename_text.get() + ".jpg"	
    filename=image_path[image_path.rfind("/") + 1:-4]
    filename_out=filename + time.strftime("%Y%m%d-%H-%M-%S") + "-" + hist_var.get() + "-" + tile_size.get() + "-" + str(img_w.get()) +"x" +str(img_h.get())
    print(filename_out)
    mos = Mosaic(image_path, (img_h.get(), img_w.get()), tile_val, src_dir, hist_var.get(), filename_out)
    mos.create_mosaic()

def open_img_btn_cb():
    global image_path
    image_path = askopenfilename()


def errors(w,h):
    global image_path,src_dir
    val=False
    if w.get()=="" or h.get()=="" :
        print("Error in width or height parameters")
        val=True
    elif src_dir is None:
        print("Select source directory")
        val=True
    elif image_path is None:
        print("Select input Image")
        val=True
    return val
		
	

def open_dir():
    global src_dir
    src_dir = askdirectory()

def exit_btn():
	exit()
	
# Define widgets
tile_no_lbl = Label(root, text="Number of tiles")
#filename_lbl = Label(root, text="Choose Output name")
#filename_text = Entry(root)
tile_no_val = Entry(root, bd=1)
open_img_btn = Button(root, text ="Load Image", command=open_img_btn_cb)
source_dir=Button(root, text ="Choose Source Dir", command=open_dir)

exit_btn = Button(root, text="Exit", command=exit_btn)

size_picker_lbl = Label(root, text="Pick Tile Size")
size_picker = OptionMenu(root, tile_size, "5","10","20","40")

hist_comp_lbl = Label(root, text="Pick Histogram Comparison")
hist_comp = OptionMenu(root, hist_var, "Correlation","Chi-Squared","Intersection","Hellinger")
img_w_lbl = Label(root, text="Image Width")
img_w_val = Entry(root, bd=1, text=img_w)
img_h_lbl = Label(root, text="Image Height")
img_h_val = Entry(root, bd=1, text=img_h)
start_btn = Button(root, text ="Start",command=start_btn_cb)

# Pack widgets
exit_btn.pack(side=BOTTOM,fill=X)
start_btn.pack(side=BOTTOM, fill=X)
open_img_btn.pack(side=BOTTOM, fill=X)
source_dir.pack(side=TOP,fill=X)



#~ tile_no_lbl.place(x=0,y=220)
#~ tile_no_val.place(x=235, y=220)

size_picker.place( x=235, y=185)
size_picker_lbl.place(x=0, y=185)

#filename_lbl.place(x=0, y=100)
#filename_text.place(x=235, y=100)

hist_comp_lbl.place(x=0, y=140)
hist_comp.place(x=235, y=140,w=120)

source_dir.pack(side=BOTTOM,fill=X)
img_w_lbl.pack()
img_w_val.pack()
img_h_lbl.pack()
img_h_val.pack()    
root.mainloop()
