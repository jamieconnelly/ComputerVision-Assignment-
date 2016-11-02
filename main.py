from Tkinter import *
from compare import Compare
from tkFileDialog import askopenfilename, askdirectory
import numpy as np
#import image_slicer

root = Tk()
root.minsize(width=400, height=400)
image_path = None

# Define widget callbacks
def start_btn_cb(val):
    tiles = int(val.get())
    # Slice image int n number of tiles
    #tiles = image_slicer.slice(image_path, tiles)
    # Print first tile as matrix
    # print (np.asarray(tiles[0].image.convert('L')))
    # Show first tile as image
    x = Compare(image_path, (100, 100), 10, src_dir)
    #print x.compare_histograms('Correlation')


def open_img_btn_cb():
    global image_path
    image_path = askopenfilename()
def open_dir():
	global src_dir
	src_dir=askdirectory()


# Define widgets
tile_no_lbl = Label(root, text="Number of tiles")
tile_no_val = Entry(root, bd=1)
open_img_btn = Button(root, text ="Load Image", command=open_img_btn_cb)
source_dir=Button(root, text ="Choose Source Dir", command=open_dir)
start_btn = Button(root, text ="Start", command=lambda v=tile_no_val: start_btn_cb(v))


# Pack widgets
start_btn.pack(side=BOTTOM, fill=X)
open_img_btn.pack(side=BOTTOM, fill=X)
source_dir.pack(side=TOP,fill=X)
tile_no_lbl.pack(side=LEFT)
tile_no_val.pack(side=RIGHT)

root.mainloop()
