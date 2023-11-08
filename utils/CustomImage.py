#to create widget in app
import tkinter as tk
from tkinter.filedialog import askopenfilename

#for histogram
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from matplotlib import rcParams
import cv2

#to create and edited the images
from PIL import ImageTk
from PIL import Image
from utils.resize_image import resize_image

#to change the edited Image
from PIL import ImageEnhance

#for treshold models
from skimage.filters import threshold_otsu,threshold_triangle

#to save files
import os

class CustomImage(Image.Image, ImageTk.PhotoImage):

    """
    This class works on creating two "widgets" in tkinter, one of them being an image in the format of Pil.Image 
    and the other in the format of tk.Image. The class also works on binarizing the editable image and displaying
    a histogram that represents the pixels of the image.  
    """

    def __init__(self, app, label_original, label_edited, canvas_histogram ,label_histogram):
        """!
        @brief It creates two images and edits one. This editing is for future analysis of capsules contained in the image.

        @param The Class uses attributes: `app = tk.Tk`, `label_original = Tkinter.Widget.Label`, `label_edited = Tkinter.Widget.Label`,
        `canvas_histogram = FigureCanvasTkAgg`, `canvas_histogram = plt.Figure`.

        @note This class is used to create two images, the original Image and the edited Image. 
            Both are created in two formats: one in the format of "PIL.Image" and the other in the format of "tk.Image".
            "image" is the original image that receives all the edits and methods of the class.
            "image_tk" is the image that receives the format transformation method and is displayed on the screen by the "Tk.Canvas" widget.

            In addition to image creation, the class has methods for editing, binarizing, and creating a histogram of the chosen image.

        @return: self.image_original, self.image_original, self.image_edited, self.image_edited_tk
        """
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
        """!
        @brief Open a window to pick the image file for editing.

        @note This method simply selects the desired file and creates the image in the 'PIL.Image'
          format to start editing. This method is used to create the 'CustomImage' class in the Main.

        @return: self.image
        """

        #Remove existing canvas in the screen
        if hasattr(self.app, "original_canvas") and (self.app, "edited_canvas"):
                # Destroy the previous canvas
                self.app.original_canvas.destroy()
                self.app.edited_canvas.destroy()
    
        self.file_path = askopenfilename(title="Select Image File", filetypes=self.filetypes)

        if self.file_path:
            self.file_path = self.file_path
            image = Image.open(self.file_path)
            self.image = image           
        
        return self.image
    
    def display_image_in_label(self, image, label):
        """!
        @brief Display the image passed as a parameter in the label.

        @param The function uses attributes: `image = PIL.Image`, `label = Tkinter.Widget.Label`.

        @note This method is used to create the original and edited image for each 'label'
          First, there's a resizing of the image to fit into each selected label. After that, there's a transformation of the original image,
            in the 'PIL.Image' format, into another image in the 'tk.Image' format, returning both images.

        @return: image, image_tk
        """
        
        self.new_width = label.winfo_width()  
        self.new_height = label.winfo_height()   

        image = resize_image(image, ((self.new_width), (self.new_height)))    
        image_tk = self.transform_in_tkimage(image)

        return  image, image_tk

    def show_image(self, app, label, image):
        """!
        @brief In this method, we create a "Canvas widget" to display the image on the screen..

        @param The function uses attributes: `app = tk.Tk`, `label = Tkinter.Widget.Label`, `image = Tk.Image`.

        @note First, we need to define the center of the image and the canvas to position the image in the center.
          After that, we check if there is an existing canvas, if there is,
              we destroy the canvas and create a new one in its place, replacing the image in editing
        
        @return: None
        """
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
            if self.image_without_blur == None:
                self.image_without_blur = self.image_edited
            else:
                pass

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

    def create_histogram(self, image, canvas, container):
        """!
        @brief Create a histogram based on the edited photo.

        @param The function uses attributes: `image = PIL.Image`, `canvas = Tk.Canvas`, `container = FigureCanvasTkAgg`.

        @note n this method, a histogram is created for the edited image and also serves to update the already plotted histogram.
          It refreshes the chart with each image edit.

        @return: None
        """
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
        self.hist.legend(['TESTE'], fontsize = 8, frameon=False)
        self.canvas.draw()

    def update_contrast(self, value):
        """!
        @brief Modify the image based on the contrast value.

        @param The function uses attributes: `value = string`.

        @note In this method, the edited image is modified with each interaction with the contrast slider.
          So, the method takes the contrast value as a parameter and applies the edit to the image.
           After that, both the image and the histogram are updated.

        @return: None
        """
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
        self.show_image(self.app, self.label_edited, self.image_edited_tk)
        self.create_histogram(self.image_edited, self.canvas_histogram ,self.label_histogram)
        
    def apply_model_otsu_treashold(self, manual_value = None):
        """!
        @brief Apply the Otsu Treashold model.

        @param The function uses attributes: `manual_value = Int`.

        @note This function take the PIL image, transform in a numpy array and pass to the threshold_otsu of the Skimage filters.
          Show an edited image in a gray scale of the treshold model, take the value of the model and plot a red line in the histogram.
        
        @return: None
        """  
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
        """!
        @brief Apply the Triangle Treashold model.

        @param The function uses attributes: `manual_value = Int`.

        @note This function take the PIL image, transform in a numpy array and pass to the threshold_triangle of the Skimage filters.
          Show an edited image in a gray scale of the treshold model, take the value of the model and plot a red line in the histogram.
        
        @return: None
        """  
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

    def get_model_value(self):
        """!
        @brief Return the model value for show in the screen

        @param The function uses attributes: None.

        @note This method returns the threshold model value to the main app for display on the screen.
        
        @return: model_value
        """  
        model_value =  self.threshold_value
        return model_value

    def draw_red_line_in_histogram(self):
        """!
        @brief Draw a red line in the histogram

        @param The function uses attributes: None.
        
        @note This method is used to draw a red line on the histogram representing the model's value
    
        @return: None
        """
        rcParams['font.weight'] = 'bold' 
        #apply the red line in the histogram
        
        self.hist.axvline(self.threshold_value, color='r', ls='--')
        self.canvas.draw()

    def reset_project(self):
        """!
        @brief Resets all variables, photos and histogram

        @param The function uses attributes: None.

        @note This function updates the edited image, the original image, the histogram and updates all variables relating to photo editing and the histogram.

        @return: None
        """

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
        """!
        @brief save the images

        @param The function uses attributes: `"folder" = mkdir`.

        @note this function resizes the original and the edited image to the original size and save this 2 images.

        @return: None
        """
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
        """!
        @brief save the histogram

        @param The function uses attributes: `"folder" = mkdir`.

        @note this function save the histogram in PNG format

        @return: None
        """
        
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        output_path = os.path.join(folder, 'histogram')
        self.hist.figure.savefig(output_path)

    def save_history(self, folder):
        """!
        @brief save the history and the bins o the histogram

        @param The function uses attributes: `"folder" = mkdir`.

        @note this function save some of the variables about the edited image and save the histogram data in a TXT file

        @return: None
        """     
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