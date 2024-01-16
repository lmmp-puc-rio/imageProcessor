from utils import ImageOriginal

class ImageEdited(ImageOriginal):
    def __init__(self, label_edited):
        self.label_edited = label_edited
        self.contrast_value = None
        self.threshold_value = None
        self.blur_value = None
        self.image_edited = None