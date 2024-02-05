#for histogram
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from matplotlib import rcParams
from PIL import Image

class Histogram():
    def __init__(self, canvas, label):
        """!
        @brief Create a histogram based on the edited photo.

        @param The function uses attributes: `image = PIL.Image`, `canvas = Tk.Canvas`, `container = FigureCanvasTkAgg`.

        @note n this method, a histogram is created for the edited image and also serves to update the already plotted histogram.
        It refreshes the chart with each image edit.

        @return: None
        """
        self.image = None
        self.canvas = canvas 
        self.container = label
        rcParams['font.weight'] = 'bold'
        self.num_of_bins = int(256/2)

    def draw_histogram(self):
        plt.clf()
        try:
            plt.hist(self.image.histogram(), weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))
            self.canvas.figure.clear()
            self.histogram_data, _ = np.histogram(self.image.histogram(), bins=self.num_of_bins, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))       
            self.hist = self.container.gca()
            self.hist.hist(self.image.histogram(), bins=self.num_of_bins, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))
            self.hist.set_xlabel('Pixel Value', fontdict=dict(weight='bold',fontsize = 12))
            self.hist.set_yscale('log')  # Setting y-axis to log scale
            self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
            self.canvas.draw()
        except Exception as e:
            print(f"Histogram Error: \n{e}")
    

    def set_image(self, image):
        if not isinstance(image, Image.Image):
            # If it is not an instance of PIL's Image, perform the search on the other object
            print("Estou no if")
            self.image = image.get_image()
        else:
            self.image = image
            print("Estou no else")