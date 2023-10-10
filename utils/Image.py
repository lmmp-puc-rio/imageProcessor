import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL.Image import open as PIL_Image
from PIL import ImageTk

from utils.resize_image import resize_image


class Image(PIL_Image):
    def __init__(self, app, label):
        self.app = app
        self.filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        self.label = label
        self.image = self.upload_image()        
        self.original_size = self.image.size   
        self.contrast_value = 1.0
        self.threshold_value = None
        self.histogram_data = None  
        self.blur_value = None
        
        
        self.display_image(self.app)
    
    def upload_image(self):
        
        self.file_path = askopenfilename(title="Select Image File", filetypes=self.filetypes)

        if self.file_path:
            self.file_path = self.file_path
            image = open(self.file_path)
            self.image = image

        return self.image
    
    def display_image(self,app):
        
        new_width = self.label.winfo_width()  
        new_height = self.label.winfo_height()     

        self.image_original = resize_image(self.image, ((new_width), (new_height)))    
     
        self.image_original_tk = self.image.copy()
        print(self.image_original_tk)
        self.image_original_tk = ImageTk.PhotoImage(self.image)

        # Clear any existing canvas and create a new one
        if hasattr(app, "original_canvas"):
            self.original_canvas.destroy()
            # Destroy the previous canvas

   
        # Calculate the coordinates to center the image in the canvas
        self.x_center = (new_width - self.image_original_tk.width()) / 2
        self.y_center = (new_height - self.image_original_tk.height()) / 2
        
        app.original_canvas = tk.Canvas(self.label)
        app.original_canvas.config(borderwidth=0)
        app.original_canvas.pack()
        app.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
        app.original_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=self.image_original_tk)
        #self.original_canvas.create_image(image=self.image_original_tk)
    