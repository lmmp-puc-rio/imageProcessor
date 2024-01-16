from abc import ABC, abstractmethod

class ImageAbstract(ABC):
    def __init__(self, app, filetypes, image, original_size, histogram_data, new_width, new_heigth):
        self.app = app
        self.filetypes = filetypes
        self.image = image
        self.original_size = original_size
        self.histogram_data = histogram_data
        self.new_width = new_width
        self.new_heigth = new_heigth
    
    @abstractmethod
    def upload_image(self):
        """!
        @brief Open a window to pick the image file for editing.

        @note This method simply selects the desired file and creates the image in the 'PIL.Image'
          format to start editing. This method is used to create the 'CustomImage' class in the Main.

        @return: self.image
        """

    @abstractmethod
    def display_image_in_label(self, image, label):

        """!
        @brief Display the image passed as a parameter in the label.

        @param The function uses attributes: `image = PIL.Image`, `label = Tkinter.Widget.Label`.

        @note This method is used to create the original and edited image for each 'label'
          First, there's a resizing of the image to fit into each selected label. After that, there's a transformation of the original image,
            in the 'PIL.Image' format, into another image in the 'tk.Image' format, returning both images.

        @return: image, image_tk
        """

    @abstractmethod
    def show_image(self, app, label, image):
        """!
        @brief In this method, we create a "Canvas widget" to display the image on the screen..

        @param The function uses attributes: `app = tk.Tk`, `label = Tkinter.Widget.Label`, `image = Tk.Image`.

        @note First, we need to define the center of the image and the canvas to position the image in the center.
          After that, we check if there is an existing canvas, if there is,
              we destroy the canvas and create a new one in its place, replacing the image in editing
        
        @return: None
        """