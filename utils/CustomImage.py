#for create widget in app
import tkinter as tk
from tkinter.filedialog import askopenfilename

#for histogram
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
import cv2

#for create and edited the images
from PIL import ImageTk
from PIL import Image
from utils.resize_image import resize_image

#for change the edited Image
from PIL import ImageEnhance

#for treshold models
from skimage.filters import threshold_otsu,threshold_triangle

#for save files
import os

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
        self.image_without_blur = None
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

        # # Clear any existing canvas and create a new one
        if label == self.label_original:
            if hasattr(app, "original_canvas"):
                # Destroy the previous canvas
                app.original_canvas.destroy()
                
            app.original_canvas = tk.Canvas(label)
            app.original_canvas.config(borderwidth=0)
            app.original_canvas.pack()
            app.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place original_canvas inside the label
            app.original_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)
                
        else:
            if hasattr(app, "edited_canvas"):
                # Destroy the previous canvas
                app.edited_canvas.destroy()
        
            app.edited_canvas = tk.Canvas(label)
            app.edited_canvas.config(borderwidth=0)
            app.edited_canvas.pack()
            app.edited_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
            app.edited_canvas.create_image(self.x_center, self.y_center, anchor=tk.NW, image=image)
            
            # Create the image without the blur. that way the program not will put blur on blur in the edited img.
            self.image_without_blur = self.image_edited

    def transform_in_tkimage(self, image):
        image = image.copy()
        image_tk = ImageTk.PhotoImage(image)

        return image_tk

    def create_histogram(self, image, canvas, container):
        self.canvas = canvas
        rcParams['font.weight'] = 'bold'       
        plt.clf()
        plt.hist(image.histogram(), weights=np.ones(len(image.histogram()))/len(image.histogram()), range=(0, 256))
        self.canvas.figure.clear()
        self.histogram_data, _ = np.histogram(image.histogram(), bins=self.num_of_bins, weights=np.ones(len(image.histogram()))/len(image.histogram()), range=(0, 256))       
        self.hist = container.gca()
        self.hist.hist(image.histogram(), bins=self.num_of_bins, weights=np.ones(len(image.histogram()))/len(image.histogram()), range=(0, 256))
        self.hist.set_xlabel('Pixel Value', fontdict=dict(weight='bold',fontsize = 12))
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        self.canvas.draw()

    def update_contrast(self, value):

        #Apply the constrast value in the edited image
        enhancer = ImageEnhance.Contrast(self.image)
        self.image_edited = enhancer.enhance(float(value))
        self.image_edited_tk = enhancer.enhance(float(value))
  
        #retun the edited_image_tk to Tk format the edited_image stays in PIL.Image format
        self.image_edited_tk = self.transform_in_tkimage(self.image_edited_tk)

        # the image without the blur. that way the program not will put blur on blur in the edited img.
        self.image_without_blur = self.image_edited

        # Update image displayed and histogram
        self.show_image(self.app, self.label_edited, self.image_edited_tk)
        self.create_histogram(self.image_edited, self.canvas_histogram ,self.label_histogram)

    def apply_blur(self, blur_value):        
        #Convert the PIL image to a NUMPY array
        self.blur_value = blur_value
        # Convert the PIL image to a NUMPY array
        image_array = np.array(self.image_without_blur)   
        image_array = image_array.astype(np.uint8)


        # Apply Gaussian blur using OpenCV
        blurred_image = cv2.GaussianBlur(image_array, (0, 0), blur_value)

        # Convert the NUMPY array back to a PIL image
        blurred_image = Image.fromarray(blurred_image)

        #change the edited image and show the tk one
        self.image_edited = blurred_image
        self.image_edited_tk = self.transform_in_tkimage(blurred_image)
        self.show_image(self.app, self.label_edited, self.image_edited_tk)
        self.create_histogram(self.image_edited, self.canvas_histogram ,self.label_histogram)
        
    def apply_model_otsu_treashold(self, manual_value = None):
        manual_value = manual_value

        #Convert image to grayscale and get pixel values
        image_gray = self.image_edited.convert("L")
        pixels = np.array(image_gray.getdata()) #gray#
        pixels = pixels.astype(np.uint8)
        
        #Check if the manual value was used and set it
        # to the model's value if it wasn't used. The automatic value will be used otherwise.
        if manual_value != None:
            self.threshold_value = int(manual_value)
        else:
            self.threshold_value = threshold_otsu(pixels)

        #apply the model
        photo_binary = image_gray.point(lambda x: 0 if x < self.threshold_value else 255)
        
        #change the edited image and show the tk one
        self.image_edited = photo_binary
        self.image_edited_tk = self.transform_in_tkimage(self.image_edited)
        self.show_image(self.app, self.label_edited, self.image_edited_tk)
        self.draw_red_line_in_histogram()

    def apply_model_triangle_treashold(self, manual_value = None):
        manual_value = manual_value

        #Convert image to grayscale and get pixel values
        image_gray = self.image_edited.convert("L")
        pixels = np.array(image_gray.getdata()) #gray#
        pixels = pixels.astype(np.uint8)
        
        #Check if the manual value was used and set it
        # to the model's value if it wasn't used. The automatic value will be used otherwise.
        if manual_value != None:
            self.threshold_value  = int(manual_value)

        else:
           self.threshold_value = threshold_triangle(pixels)

        #apply the model
        photo_binary = image_gray.point(lambda x: 0 if x < self.threshold_value  else 255)
        
        #change the edited image and show the tk one
        self.image_edited = photo_binary
        self.image_edited_tk = self.transform_in_tkimage(self.image_edited)
        self.show_image(self.app, self.label_edited, self.image_edited_tk)
        self.draw_red_line_in_histogram()

    def draw_red_line_in_histogram(self):
        rcParams['font.weight'] = 'bold' 
        #apply the red line in the histogram
        
        self.hist.axvline(self.threshold_value, color='r', ls='--')
        self.canvas.draw()

    def reset_project(self):

        #reseting the edited image for the original
        self.image_edited = self.image
        self.image_edited = resize_image(self.image, ((self.original_size[0]),(self.original_size[1])))
        self.image_edited_tk = self.transform_in_tkimage(self.image_edited)
        self.show_image(self.app, self.label_edited, self.image_edited_tk)

        #reset contrast
        self.contrast_value = 0

        #reset Blur
        self.blur_value = 0

        #reset histogram
        self.create_histogram(self.image_edited, self.canvas_histogram, self.label_histogram)

    def save_image_edited(self, folder):
        self.binary_photo_for_save = self.image_edited.resize(self.original_size)

        self.image_original_for_save = self.image_original.resize(self.original_size)

        # Ensure the folder exists; create it if it doesn't
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        # Save the image with a new name in the folder
        output_path = os.path.join(folder, 'image_edited')
        self.binary_photo_for_save.save(output_path, 'PNG')
        output_path_original = os.path.join(folder, 'image_original')
        self.image_original_for_save.save(output_path_original, 'PNG')
    
    def save_histogram(self, folder):
        
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        output_path = os.path.join(folder, 'histogram')
        self.hist.figure.savefig(output_path)

    def save_history(self, folder):    
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Create string with processing history data
        history_data = f"Image file path: {self.file_path}\nContrast value: {self.contrast_value}\n"

        if self.threshold_value is not None:
            history_data += f"Otsu threshold value: {self.threshold_value}\n"

        if self.blur_value is not None:
            history_data += f"Blur value: {self.blur_value}\n"

        if self.histogram_data is not None:
            history_data += "Histogram data:\n"
            for i, value in enumerate(self.histogram_data):
                history_data += f"{i}: {value}\n"

        # Write string to text file
        filepath = os.path.join(folder, 'contrast history')
        with open(filepath, "w") as f:
            f.write(history_data)