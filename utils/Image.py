
import tkinter as tk
from tkinter.filedialog import askopenfilename
# from PIL.Image import open
# from PIL import ImageTk
from PIL import ImageTk
from PIL import Image
from utils.resize_image import resize_image


class CustomImage(Image.Image, ImageTk.PhotoImage):
    def __init__(self, app, label_original, label_edited, label_histogram):
        self.app = app
        self.filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        self.label_original = label_original
        self.label_edited = label_edited
        self.label_histogram = label_histogram
        self.image = self.upload_image()        
        self.original_size = self.image.size
        self.new_width = None
        self.new_height  = None
        self.contrast_value = 1.0
        self.threshold_value = None
        self.histogram_data = None  
        self.blur_value = None
        self.image_edited = None


        self.image_original,self.image_original_tk = self.display_image_in_label(self.image, self.label_original)
        self.show_image(self.app, self.label_original, self.image_original_tk)
        
        #Create and show the edited Image based in the original PIL Image
        self.image_edited = self.image
        self.image_edited,self.image_edited_tk = self.display_image_in_label(self.image_edited, self.label_edited)
        self.show_image(self.app, self.label_edited, self.image_edited_tk)

    

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


        # # Clear any existing canvas and create a new one
        if label == self.label_original:
            if hasattr(app, "original_canvas"):
                app.original_canvas.destroy()
                # Destroy the previous canvas
        else:
            if hasattr(app, "edited_canvas"):
                app.edited_canvas.destroy()
                # Destroy the previous canvas


        # # Calculate the coordinates to center the image in the canvas
        x_center = (self.new_width - image.width()) / 2
        y_center = (self.new_height - image.height()) / 2
        
        app.original_canvas = tk.Canvas(label)
        app.original_canvas.config(borderwidth=0)
        app.original_canvas.pack()
        app.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
        app.original_canvas.create_image(x_center, y_center, anchor=tk.NW, image=image)

    def transform_in_tkimage(self, image):
        image = image.copy()
        image_tk = ImageTk.PhotoImage(image)

        return image_tk
