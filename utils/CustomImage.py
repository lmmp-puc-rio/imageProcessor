#for create widget in app
import tkinter as tk
from tkinter.filedialog import askopenfilename

#for histogram
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams

#for create and edited the images
from PIL import ImageTk
from PIL import Image
from utils.resize_image import resize_image

#for change the edited Image
from PIL import ImageEnhance


class CustomImage(Image.Image, ImageTk.PhotoImage):
    def __init__(self, app, label_original, label_edited, canvas_histogram ,label_histogram):
        self.app = app
        self.filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        self.label_original = label_original
        self.label_edited = label_edited
        self.image = self.upload_image()        
        self.original_size = self.image.size
        self.new_width = None
        self.new_height  = None
        self.contrast_value = 1.0
        self.threshold_value = None
        self.histogram_data = None  
        self.blur_value = None
        self.image_edited = None
        self.image_without_blur = self.image_edited
        self.label_histogram = label_histogram
        self.canvas_histogram = canvas_histogram
        self.num_of_bins = int(256/2)


        self.image_original,self.image_original_tk = self.display_image_in_label(self.image, self.label_original)
        self.show_image(self.app, self.label_original, self.image_original_tk)
        
        #Create and show the edited Image based in the original PIL Image
        self.image_edited = self.image
        self.image_edited,self.image_edited_tk = self.display_image_in_label(self.image_edited, self.label_edited)
        self.show_image(self.app, self.label_edited, self.image_edited_tk)

        #create and show the histogram based in the edited Image
        self.create_histogram(self.image_edited, self.canvas_histogram ,self.label_histogram)

    

    def upload_image(self):
        
        self.file_path = askopenfilename(title="Select Image File", filetypes=self.filetypes)

        if self.file_path:
            self.file_path = self.file_path
            image = Image.open(self.file_path)
            self.image = image
            
        
        return self.image
    
    def display_image_in_label(self, image, label):
        
        self.new_width = label.winfo_width()  
        self.new_height = label.winfo_height()   

        image = resize_image(image, ((self.new_width), (self.new_height)))    
        image_tk = self.transform_in_tkimage(image)

        return  image, image_tk
        #self.show_image(app, label, self.image_original_tk)

    def show_image(self, app, label, image):
        #Receives the tk PhotoImage and destroy to plot the new image in the correct canvas
        self.image_w = image.width()
        self.image_h = image.height()
        #Calculate the coordinates to center the image in the canvas
        self.x_center = (self.new_width- self.image_w) / 2
        self.y_center = (self.new_height - self.image_h) / 2
        print(f"\n\n\nESSE É A WID{self.image_w}\nÉSSA É A {self.image_h}")
        print(f"\n\n\nESSE É A WID{int(self.image_w)}\nÉSSA É A {type(self.image_h)}")

        # # Clear any existing canvas and create a new one
        if label == self.label_original:
            if hasattr(app, "original_canvas"):
                # Destroy the previous canvas
                app.original_canvas.destroy()
            else:
                app.original_canvas = tk.Canvas(label)
                app.original_canvas.config(borderwidth=0)
                app.original_canvas.pack()
                app.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place original_canvas inside the label
                print("passei pelo OG")
                app.original_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)
                
        else:
            if hasattr(app, "edited_canvas"):
                # Destroy the previous canvas
                app.edited_canvas.destroy()
            else:
                app.edited_canvas = tk.Canvas(label)
                app.edited_canvas.config(borderwidth=0)
                app.edited_canvas.pack()
                app.edited_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
                app.edited_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)
                print("passei pelo ED")

        # app.canvas = tk.Canvas(label)
        # app.canvas.config(borderwidth=0)
        # app.canvas.pack()
        # app.canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
        # app.canvas.create_image(x_center, y_center, anchor=tk.NW, image=image)

    def transform_in_tkimage(self, image):
        image = image.copy()
        image_tk = ImageTk.PhotoImage(image)

        return image_tk

    def create_histogram(self, image, canvas, container):
    
        rcParams['font.weight'] = 'bold'       
        plt.clf()
        plt.hist(image.histogram(), weights=np.ones(len(image.histogram()))/len(image.histogram()), range=(0, 256))
        canvas.figure.clear()
        self.histogram_data, _ = np.histogram(image.histogram(), bins=self.num_of_bins, weights=np.ones(len(image.histogram()))/len(image.histogram()), range=(0, 256))       
        self.hist = container.gca()
        self.hist.hist(image.histogram(), bins=self.num_of_bins, weights=np.ones(len(image.histogram()))/len(image.histogram()), range=(0, 256))
        self.hist.set_xlabel('Pixel Value', fontdict=dict(weight='bold',fontsize = 12))
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        canvas.draw()

    def update_image(self, image):
        if hasattr(self.app, "edited_canvas"):
            self.app.edited_canvas.destroy()
            # Destroy the previous canvas

        label = self.app.edited_canvas
        self.show_image(self.app, label, image)
    
    def reset_images_and_histogram(self):

        #reseting the edited image for the original
        self.image_edited = self.image
        self.image_edited = resize_image(self.image, ((self.original_size[0]),(self.original_size[1])))
        self.update_image(self.image_edited)

        #reset contrast
        self.bar_contrast.set(1.0)
        self.contrast_value = 0
        #self.update_contrast(self.image_edited, self.contrast_value)
        

        #reset Blur
        self.blur_value_textbox.delete("1.0","2.0")
        self.blur_value = 0

        #reset MODEL
        #self.show_histogram(self.image_edited)
        self.text_box_treshold.delete("1.0", "end")
        self.radio_selected.set('automatic')
        self.text_box_treshold.config(state='disable')

        #reset histogram
        self.show_histogram(self.image_edited)

    def update_contrast(self, value):

        #Apply the constrast value in the edited image
        enhancer = ImageEnhance.Contrast(self.image)
        photo_contrast = enhancer.enhance(float(value))
        self.image_edited_tk = enhancer.enhance(float(value))
        
        # Update image displaed and histogram
        self.update_image(photo_contrast)
        self.create_histogram(self.image_edited, self.canvas_histogram ,self.label_histogram)