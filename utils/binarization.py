#to change the edited Image
import numpy as np
from skimage.filters import threshold_otsu,threshold_triangle

class Binarization():
    def __init__(self):
        self.model_value = None

    def set_model_value(self, value):
        self.model_value = value

    def get_model_value(self):
        return self.model_value
    
    def otsu(self,image):
        """!
        @brief Apply the Otsu Treashold model.

        @param The function uses attributes: `manual_value = Int`.

        @note This function take the PIL image, transform in a numpy array and pass to the threshold_otsu of the Skimage filters.
        Show an edited image in a gray scale of the treshold model, take the value of the model and plot a red line in the histogram.

        @return: None
        """  
        manual_value = self.model_value

        #Convert image to grayscale and get pixel values
        image_gray = image.convert("L")
        pixels = np.array(image_gray.getdata()) #gray#
        pixels = pixels.astype(np.uint8)

        #Check if the manual value was used and set it
        # to the model's value if it wasn't used. The automatic value will be used otherwise.
        if manual_value != None:
            self.model_value = manual_value
        else:
            self.model_value = threshold_otsu(pixels)

        #apply the model
        photo_binary = image_gray.point(lambda x: 0 if x < self.model_value else 255)

        #change the edited image and show the tk one
        return photo_binary

    def triangle(self):
        pass

