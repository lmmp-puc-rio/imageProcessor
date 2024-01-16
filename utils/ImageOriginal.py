#to create widget in app
import tkinter as tk
from tkinter.filedialog import askopenfilename

from utils.resize_image import resize_image
#from PIL import ImageTk
from PIL import Image

class ImageOriginal ():
    def __init__(self, app, label_original):
        self.app = app
        self.filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        self.image = None
        self.original_size = None
        self.histogram_data = None
        self.new_width = None
        self.new_heigth = None
        self.label_original = label_original
        self.image_without_blur = None
        self.blur_value = None
    
    def upload_image(self, app, filetypes):

        #Remove existing canvas in the screen
        if hasattr(app, "original_canvas"):
            # Destroy the previous canvas
            app.original_canvas.destroy()
    
        self.file_path = askopenfilename(title="Select Image File", filetypes = filetypes)

        if self.file_path:
            self.file_path = self.file_path
            image = Image.open(self.file_path)
            self.image = image           
        
        return self.image
    
    def display_image_in_label(self, image, label_original):

        self.new_width = label_original.winfo_width()  
        self.new_height = label_original.winfo_height()   

        image = resize_image(image, ((self.new_width), (self.new_height)))    
        return  image

    def show_image(self, app, label, image):

        #Receives the tk PhotoImage and destroy to plot the new image in the correct canvas
        self.image_w = image.width()
        self.image_h = image.height()
        #Calculate the coordinates to center the image in the canvas
        self.x_center = (self.new_width- self.image_w) / 2
        self.y_center = (self.new_height - self.image_h) / 2

        # Clear any existing canvas and create a new one
        if label == self.label_original:
            if hasattr(app, "original_canvas"):
                # Destroy the previous canvas
                app.original_canvas.destroy()
                
            app.original_canvas = tk.Canvas(label)
            app.original_canvas.config(borderwidth=0)
            app.original_canvas.pack()
            app.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place original_canvas inside the label
            app.original_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)
