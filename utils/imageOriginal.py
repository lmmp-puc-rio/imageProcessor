#to create widget in app
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk

from utils.resize_image import resize_image

#from PIL import ImageTk
from PIL import Image

class ImageOriginal ():
    def __init__(self, app, label):
        self.app = app
        self.filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        self.image = None
        self.image_tk = None
        self.original_size = None
        self.histogram_data = None
        self.new_width = None
        self.new_height = None
        self.label = label
        self.image_without_blur = None
        self.blur_value = None
        self.file_path = None
    
    def upload_show_image(self):
        self.upload_image()
        self.display_image_in_label(self.image, self.label)
        self.show_image_in_label(self.image_tk)

    def upload_image(self):

        if not self.file_path:
            self.file_path = askopenfilename(title="Select Image File", filetypes=self.filetypes)

        try:
            image = Image.open(self.file_path)
            self.image = image   
            self.original_size = image.size
            
        except Exception as e:
            print(f"Error loading the original image: \n{e}")

    def display_image_in_label(self, image, label):

        #Remove existing canvas in the screen
        if hasattr(self.app, "original_canvas"):
            # Destroy the previous canvas
            self.app.original_canvas.destroy()

        self.new_width = label.winfo_width()  
        self.new_height = label.winfo_height()   
        try:
            img = resize_image(image, ((self.new_width), (self.new_height)))
            self.image_tk = self.transform_in_tkimage(img)
    
        except Exception as e:
            print(f"Image does not resize correcly: \n{e}")

    def show_image_in_label(self, image):

        #Receives the tk PhotoImage and destroy to plot the new image in the correct canvas
        self.image_w = image.width()
        self.image_h = image.height()
        #Calculate the coordinates to center the image in the canvas
        self.x_center = (self.new_width- self.image_w) / 2
        self.y_center = (self.new_height - self.image_h) / 2

        # Clear any existing canvas and create a new one
        if self.label:
            if hasattr(self.app, "original_canvas"):
                # Destroy the previous canvas
                self.app.original_canvas.destroy()
                
            self.app.original_canvas = tk.Canvas(self.label)
            self.app.original_canvas.config(borderwidth=0)
            self.app.original_canvas.pack()
            self.app.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place original_canvas inside the label
            self.app.original_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)
    
    def get_image(self):
        return self.image
    
    def transform_in_tkimage(self, image):
        """!
        @brief This method converts the image from PIL.Image to Tk.Image

        @param The function uses attributes: `image = PIL.Image`.

        @note This method converts the image from PIL.Image to Tk.Image to have the image in a format that is accepted by the tk.Canvas.

        @return: image_tk
        """
        image = image.copy()
        image_tk = ImageTk.PhotoImage(image)

        return image_tk
