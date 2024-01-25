from utils.imageOriginal import ImageOriginal
from utils.resize_image import resize_image
from PIL import Image
import tkinter as tk

#plot histogram
import matplotlib.pyplot as plt

#to change the edited Image
from PIL import ImageEnhance

class ImageEdited(ImageOriginal):

    def __init__(self, app, label, image):
        super().__init__(app, label)
        self.contrast_value = None
        self.threshold_value = None
        self.blur_value = None
        self.image = image
        self.image_tk = None
        self.new_width = None
        self.new_height = None


    def upload_show_image(self):
        self.display_image_in_label(self.image, self.label)
        self.show_image_in_label(self.image_tk)
    
    def display_image_in_label(self, image, label):
        
        #Remove existing canvas in the screen
        if hasattr(self.app, "edited_canvas"):
            # Destroy the previous canvas
            self.app.edited_canvas.destroy()

        self.new_width = label.winfo_width()  
        self.new_height = label.winfo_height()   

        try:
            img = resize_image(image, ((self.new_width), (self.new_height)))
            self.image_tk = self.transform_in_tkimage(img)
    
        except Exception as e:
            print(f"Edited Image does not resize correcly: \n{e}")

    def show_image_in_label(self, image):

        #Receives the tk PhotoImage and destroy to plot the new image in the correct canvas
        self.image_w = image.width()
        self.image_h = image.height()
        #Calculate the coordinates to center the image in the canvas
        self.x_center = (self.new_width - self.image_w) / 2
        self.y_center = (self.new_height - self.image_h) / 2

        # Clear any existing canvas and create a new one
        if self.label :
            if hasattr(self.app, "edited_canvas"):
                # Destroy the previous canvas
                self.app.edited_canvas.destroy()
                
            self.app.edited_canvas = tk.Canvas(self.label)
            self.app.edited_canvas.config(borderwidth=0)
            self.app.edited_canvas.pack()
            self.app.edited_canvas.place(relwidth=1.0, relheight=1.0)  # Place edited_canvas inside the label
            self.app.edited_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)

    def update_contrast(self, contrast_value):
        """!
        @brief Modify the image based on the contrast contrast_value.

        @param The function uses attributes: `contrast_value = string`.

        @note In this method, the edited image is modified with each interaction with the contrast slider.
          So, the method takes the contrast contrast_value as a parameter and applies the edit to the image.
           After that, both the image and the histogram are updated.

        @return: None
        """

        image_copy = resize_image(self.image, ((self.new_width), (self.new_height)))
        enhancer = ImageEnhance.Contrast(image_copy)
        self.image = enhancer.enhance(float(contrast_value))
        image_tk = enhancer.enhance(float(contrast_value))
        
        #retun the edited_image_tk to Tk format the edited_image stays in PIL.Image format
        self.image_tk = self.transform_in_tkimage(image_tk)

        # the image without the blur. that way the program not will put blur on blur in the edited img.
        self.image_without_blur = image_copy

        # Update image displayed and histogram
        self.show_image_in_label(self.image_tk)
    
