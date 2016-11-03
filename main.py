import Tkinter as tk
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

        # Declare labels and inputs
        self.filename_lbl = tk.Label(parent, text="Choose Output name")
        self.filename_text = tk.Entry(parent)
        self.size_picker_lbl = tk.Label(parent, text="Pick Tile Size")
        self.size_picker = tk.OptionMenu(parent, self.tile_size,
                                         "5", "10", "20", "30")
        self.img_w_lbl = tk.Label(parent, text="Image Width")
        self.img_w_val = tk.Entry(parent, bd=1)
        self.img_h_lbl = tk.Label(parent, text="Image Height")
        self.img_h_val = tk.Entry(parent, bd=1)
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
        self.source_dir.pack(side=tk.TOP, fill=tk.X)
        self.source_dir.pack(side=tk.BOTTOM, fill=tk.X)
        self.img_w_lbl.pack()
        self.img_w_val.pack()
        self.img_h_lbl.pack()
        self.img_h_val.pack()
        self.filename_lbl.pack()
        self.filename_text.pack()
        self.hist_comp_lbl.pack()
        self.hist_comp.pack()
        self.size_picker_lbl.pack()
        self.size_picker.pack()

    def start_btn_cb(self):
        img_h = int(self.img_h_val.get())
        img_w = int(self.img_w_val.get())
        tile_val = int(self.tile_size.get())
        filename_out = "/" + self.filename_text.get() + ".jpg"
        dis_metric = self.hist_var.get()
        mos = Mosaic(self.image_path, (img_h, img_w), tile_val,
                     self.src_dir, dis_metric, filename_out)
        mos.create_mosaic()

    def open_img_btn_cb(self):
        self.image_path = askopenfilename()

    def open_dir(self):
        self.src_dir = askdirectory()

    def exit_btn(self):
        exit()


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
