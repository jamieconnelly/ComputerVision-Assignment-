import Tkinter as tk
import time
from mosaic import Mosaic
from tkFileDialog import askopenfilename, askdirectory


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.image_path = None
        self.src_dir = None
        self.tile_size = tk.StringVar(parent)
        self.tile_size.set("5")
        self.hist_var = tk.StringVar(parent)
        self.hist_var.set("Correlation")
        self.img_w = tk.IntVar()
        self.img_h = tk.IntVar()
        self.img_w.set(800)
        self.img_h.set(600)
        self.modes = [("Part A", "A"), ("Part C", "C")]

        self.part_chooser = tk.StringVar()
        self.part_chooser.set("A")

        # Declare labels and inputs
        self.size_picker_lbl = tk.Label(parent, text="Pick Tile Size")
        self.size_picker = tk.OptionMenu(parent, self.tile_size,
                                         "5", "10", "20", "40")
        self.img_w_lbl = tk.Label(parent, text="Image Width")
        self.img_w_val = tk.Entry(parent, bd=1, text=self.img_w)
        self.img_h_lbl = tk.Label(parent, text="Image Height")
        self.img_h_val = tk.Entry(parent, bd=1, text=self.img_h)
        self.hist_comp_lbl = tk.Label(parent, text="Pick Histogram Comparison")
        self.hist_comp = tk.OptionMenu(parent, self.hist_var,
                                       "Correlation", "Chi-Squared",
                                       "Intersection", "Hellinger")

        # Declare buttons
        self.start_btn = tk.Button(parent, text="Start",
                                   command=self.start_btn_cb)
        self.open_img_btn = tk.Button(parent, text="Load Image",
                                      command=self.open_img_btn_cb)
        self.source_dir = tk.Button(parent, text="Choose Source Dir",
                                    command=self.open_dir)
        self.exit_btn = tk.Button(parent, text="Exit", command=self.exit_btn)

        # Pack widgets
        self.exit_btn.pack(side=tk.BOTTOM, fill=tk.X)
        self.start_btn.pack(side=tk.BOTTOM, fill=tk.X)
        self.open_img_btn.pack(side=tk.BOTTOM, fill=tk.X)
        #self.source_dir.pack(side=tk.TOP, fill=tk.X)
        self.source_dir.pack(side=tk.BOTTOM, fill=tk.X)
        self.img_w_lbl.pack()
        self.img_w_val.pack()
        self.img_h_lbl.pack()
        self.img_h_val.pack()
        self.hist_comp_lbl.pack()
        self.hist_comp.pack()
        for text, mode in self.modes:
            b = tk.Radiobutton(parent, text=text,
                            variable=self.part_chooser, value=mode)
            b.pack(anchor=tk.W)
        self.size_picker_lbl.pack()
        self.size_picker.pack()

    def start_btn_cb(self):
        if self.errors():
            exit()

        img_h = int(self.img_h.get())
        img_w = int(self.img_w.get())
        tile_val = int(self.tile_size.get())
        dis_metric = self.hist_var.get()
        filename = self.image_path[self.image_path.rfind("/") + 1:-4]
        filename_out = filename + time.strftime("%Y%m%d-%H-%M-%S") + "-" + dis_metric + "-" + str(tile_val) + "-" + str(img_w) + "x" + str(img_h)
        mos = Mosaic(self.image_path, (img_w, img_h), tile_val,
                     self.src_dir, dis_metric, filename_out)
        if self.part_chooser.get() == "A":
            mos.read_src_images()
            mos.create_mosaic()
        elif self.part_chooser.get() == "C":
            mos.compute_partB()
            mos.update_src_images()
            mos.read_src_images()
            mos.create_mosaic()

    def open_img_btn_cb(self):
        self.image_path = askopenfilename()

    def open_dir(self):
        self.src_dir = askdirectory()

    def errors(self):
        val = False
        if self.img_w == "" or self.img_h == "":
            print("Error in width or height parameters")
            val = True
        elif self.src_dir is None:
            print("Select source directory")
            val = True
        elif self.image_path is None:
            print("Select input Image")
            val = True
        return val

    def exit_btn(self):
        exit()


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
