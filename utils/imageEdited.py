from utils.imageOriginal import ImageOriginal
from utils import resize_image
from PIL import Image

#to change the edited Image
from PIL import ImageEnhance

class ImageEdited(ImageOriginal):

    def __init__(self, app, label):
        super().__init__(app, label)
        #self.app = app
        #self.label_edited = label
        self.contrast_value = None
        self.threshold_value = None
        self.blur_value = None
        self.image_edited = None

    def update_contrast(self, value):
        """!
        @brief Modify the image based on the contrast value.

        @param The function uses attributes: `value = string`.

        @note In this method, the edited image is modified with each interaction with the contrast slider.
          So, the method takes the contrast value as a parameter and applies the edit to the image.
           After that, both the image and the histogram are updated.

        @return: None
        """
        # Apply the constrast value in the edited image
        # This method needs to create a copy of the original image and resize it once again.
        # If this doesn't happen, the image will be resized to its original size 
        
        image_copy = self.image.copy()
        image_copy = resize_image(image_copy, ((self.new_width), (self.new_height)))
        enhancer = ImageEnhance.Contrast(image_copy)
        self.image_edited = enhancer.enhance(float(value))
        self.image_edited_tk = enhancer.enhance(float(value))
  
        #retun the edited_image_tk to Tk format the edited_image stays in PIL.Image format
        self.image_edited_tk = self.transform_in_tkimage(self.image_edited_tk)

        # the image without the blur. that way the program not will put blur on blur in the edited img.
        self.image_without_blur = self.image_edited

        # Update image displayed and histogram
        self.show_image(self.app, self.label_edited, self.image_edited_tk)
        self.create_histogram(self.image_edited, self.canvas_histogram ,self.label_histogram)
