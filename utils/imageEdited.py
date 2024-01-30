from utils.imageOriginal import ImageOriginal
from utils.resize_image import resize_image
from PIL import Image
import tkinter as tk

#plot histogram
import matplotlib.pyplot as plt

#to change the edited Image
import numpy as np
import cv2
from PIL import ImageEnhance

class ImageEdited(ImageOriginal):

    def __init__(self, app, label, image):
        super().__init__(app, label)
        self.contrast_value = None
        self.threshold_value = None
        self.blur_value = None
        self.image = image
        self.image_edited = None
        self.photo_binary = None


    def upload_show_image(self):
        #calls the sequence of methods to upload and display the image on the screen
        self.display_image_in_label(self.label)
        self.show_image_in_label()
    
    def display_image_in_label(self, label):
        
        #Remove existing canvas in the screen
        if hasattr(self.app, "edited_canvas"):
            # Destroy the previous canvas
            self.app.edited_canvas.destroy()

        self.new_width = label.winfo_width()  
        self.new_height = label.winfo_height()   

        
    def show_image_in_label(self):
        #Show the image in the referenced label
        try:
            image = resize_image(self.image_edited, ((self.new_width), (self.new_height)))
            self.image_tk = self.transform_in_tkimage(image)
    
        except Exception as e:
            print(f"Edited Image does not resize correcly: \n{e}")

        #Receives the tk PhotoImage and destroy to plot the new image in the correct canvas
        self.image_w = self.image_tk.width()
        self.image_h = self.image_tk.height()
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
            self.app.edited_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=self.image_tk)

    def update_contrast(self, contrast_value):
        """!
        @brief Modify the image based on the contrast contrast_value.

        @param The function uses attributes: `contrast_value = string`.

        @note In this method, the edited image is modified with each interaction with the contrast slider.
          So, the method takes the contrast contrast_value as a parameter and applies the edit to the image.
           After that, both the image and the histogram are updated.

        @return: None
        """

        image_copy = self.image.copy()
        image_copy = resize_image(self.image, ((self.new_width), (self.new_height)))
        enhancer = ImageEnhance.Contrast(image_copy)
        self.image_edited = enhancer.enhance(float(contrast_value))
        self.image_tk = enhancer.enhance(float(contrast_value))
        
        #retun the edited_image_tk to Tk format the edited_image stays in PIL.Image format
        #self.image_tk = self.transform_in_tkimage(image_tk)

        # the image without the blur. that way the program not will put blur on blur in the edited img.
        self.image_without_blur = image_copy

        # Update image displayed and histogram
        self.show_image_in_label()
    
    def get_image(self):
        return self.image_edited
    
    def set_image_edited(self, image):
        self.image_edited = image

    def apply_blur(self, blur_value):

        """!
        @brief Apply the blur to the edited image.

        @param The function uses attributes: `blur_value = Int`.

        @note In this method, the blur is applied to a temporary variable, 'self.image_without_blur',
          which is created during image upload and updated during the contrast update. 
          This image is used to avoid applying blur on top of blur. At the end of the method, 'image_edited' is assigned this blurred image
        
        @return: None
        """        
        self.blur_value = blur_value
        # Convert the PIL image to a NUMPY array
        image_array = np.array(self.image_without_blur)   
        image_array = image_array.astype(np.uint8)


        # Apply Gaussian blur using OpenCV
        blurred_image = cv2.GaussianBlur(image_array, (0, 0), self.blur_value)

        # Convert the NUMPY array back to a PIL image
        blurred_image = Image.fromarray(blurred_image)

        #change the edited image and show the tk one
        self.image_edited = blurred_image
        self.image_edited_tk = self.transform_in_tkimage(blurred_image)
        self.show_image_in_label()
        #self.create_histogram(self.image_edited, self.canvas_histogram ,self.label_histogram)