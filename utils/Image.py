import tkinter as tk
from tkinter.filedialog import askopenfilename
# from PIL.Image import open
# from PIL import ImageTk
from PIL import ImageTk
from PIL import Image
from utils.resize_image import resize_image


class CustomImage(Image.Image, ImageTk.PhotoImage):
    def __init__(self, app, label):
        self.app = app
        self.filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        self.label = label
        self.image = self.upload_image()        
        self.original_size = self.image.size
        self.new_width = None
        self.new_height  = None
        self.contrast_value = 1.0
        self.threshold_value = None
        self.histogram_data = None  
        self.blur_value = None
        self.display_image(self.app)
    
    def upload_image(self):
        
        self.file_path = askopenfilename(title="Select Image File", filetypes=self.filetypes)

        if self.file_path:
            self.file_path = self.file_path
            image = Image.open(self.file_path)
            self.image = image
        
        print(self.image)

        return self.image
    
    def display_image(self, app):
        
        self.new_width = self.label.winfo_width()  
        self.new_height = self.label.winfo_height()   

        self.image_original = resize_image(self.image, ((self.new_width), (self.new_height)))    
        self.image_original_tk = self.transform_in_tkimage(self.image_original)
        
        self.show_image(self.app, self.image_original_tk)

        

    def show_image(self, app, image):

        #Receives the tk PhotoImage and destroy to plot the new image in the correct canvas

        # Clear any existing canvas and create a new one
        if hasattr(app, "original_canvas"):
            app.original_canvas.destroy()
            app.edited_canvas.destroy()
            # Destroy the previous canvas

        # Calculate the coordinates to center the image in the canvas
        self.x_center = (self.new_width - image.width()) / 2
        self.y_center = (self.new_height - image.height()) / 2
        
        app.original_canvas = tk.Canvas(self.label)
        app.original_canvas.config(borderwidth=0)
        app.original_canvas.pack()
        app.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
        app.original_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)

    def transform_in_tkimage(self, image):
        self.image_original_tk = image.copy()
        self.image_original_tk = ImageTk.PhotoImage(self.image)

        return self.image_original_tk

    def create_edited_image(self, image):
        pass
