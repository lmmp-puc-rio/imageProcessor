import tkinter as tk
import webbrowser
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from skimage.filters import threshold_otsu
from tkinter.messagebox import askyesno
import matplotlib.ticker as mtick
import os

class FullScreenApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize variables
        self.filename = None
        self.original_image = None
        self.image = None
        self.image_gray = None
        self.image_binary = None
        self.contrast_value = 1.0
        self.threshold_value = None
        self.histogram_data = None
        self.hist = None
        self.size = (500, 500)

        #Colors used in the app
        self.background_header_color = '#5376D6'#'#767272'
        self.background_header_button_color = 'white'
        self.background_header_button_font_color = 'black'
        self.background_important_button_color = 'red'

        #Fonts used in app
        self.fz_mn = 8
        self.fz_md = 10
        self.fz_xmd = 12
        self.fz_lg = 14
        self.fz_xlg = 16

        # Set the app title in the title bar
        self.title('Image Processor')

        # Set the window attributes to keep the title bar visible
        # self.attributes('-alpha')
        self.attributes("-fullscreen", True)
        self.overrideredirect(False)

        # Set the window state to maximized
        #self.wm_state('zoomed')

        # Create a frame for the header
        self.header_frame = tk.Frame(self, bg=self.background_header_color, height=50)
        self.header_frame.pack(side='top', fill='x')

        # Add a logo to the header with hyperlink to google homepage
        self.logo_image = tk.PhotoImage(file=r'src/images/logo_grey.png')
        self.logo_label = tk.Label(self.header_frame, image=self.logo_image, bg=self.background_header_color)
        self.logo_label.pack(side='left', padx=16, pady=10) 
        self.logo_label.bind("<Button-1>", lambda e: webbrowser.open_new("http://lmmp.mec.puc-rio.br/lmmp/"))

        # # Add minimize and close buttons to the window

        self.close_button = tk.Button(self.header_frame, text='x', font=('Arial', self.fz_md), bg=self.background_header_color, fg='white', command=self.close_window, height= 1, width=2)
        self.close_button.pack(side='right', padx=(0,5), pady=5)

        self.minimize_button = tk.Button(self.header_frame, text='-', font=('Arial', self.fz_md), bg=self.background_header_color, fg='white', command=self.minimize_window, height= 1, width=2)
        self.minimize_button.pack(side='right', padx=(5,0), pady=5)

        # Add a button to the header with hyperlink to LMMP homepage
        self.google_button = tk.Button(self.header_frame, text='Homepage', font=('Arial', self.fz_xmd), bg=self.background_header_button_color, fg=self.background_header_button_font_color, command=self.open_homepage)
        self.google_button.pack(side='right', padx=10, pady=5)

        # Add a button to the header with hyperlink to Help homepage
        self.google_button = tk.Button(self.header_frame, text='Help', font=('Arial', self.fz_xmd), bg=self.background_header_button_color, fg=self.background_header_button_font_color, command=self.open_helpPage)
        self.google_button.pack(side='right', padx=10, pady=5)

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.header_frame, bg=self.background_header_color)
        self.button_frame.pack(side='right', padx=10, pady=5)

        # Add an upload button to the button frame
        self.upload_button = tk.Button(self.button_frame, text='Upload Image', font=('Arial', self.fz_xmd), bg=self.background_header_button_color, fg=self.background_header_button_font_color, command=self.upload_image)
        self.upload_button.pack(side='left', padx=5, pady=5)

        # # Create a frame for the content
        self.content_frame = tk.Frame(self, bg='white', height=500)
        # self.content_frame.pack(side='top', fill='both', expand=True)

        # Create the espace for the loaded image
        self.image_canvas = tk.Canvas(self.content_frame, width=250, height=250)
        
        # self.image_canvas = tk.Label(self.master)
        # self.image_canvas.pack(side="left", padx=10, pady=10)
        # self.image_canvas.grid(row=0, column=1, rowspan=4, padx=10, pady=10)
        self.f_hist = plt.Figure(figsize=(5, 4))
        self.histogram_canvas = FigureCanvasTkAgg(self.f_hist, master=self)
        # self.histogram_canvas.get_tk_widget().pack(side=tk.RIGHT)#, anchor='s')
        self.histogram_canvas.get_tk_widget().pack(padx=200, pady=100)
        


        # Create a frame for the header
        self.bottom_frame = tk.Frame(self, bg=self.background_header_color, height=50)
        self.bottom_frame.pack(side='bottom', fill='x')

        # Create a Scale widget to adjust the contrast
        self.contrast_scale = tk.Scale(self.bottom_frame, from_=0.1, to=5.0, resolution=0.1, bg=self.background_header_button_color, label="Contrast", orient=tk.HORIZONTAL, command=self.update_contrast, font=('Arial', self.fz_xmd), width=15)
        self.contrast_scale.pack(anchor = "s", side='left', padx=100, pady=15)#( side = "bottom")#(anchor = "sw")#

        # Create a button to apply Otsu's threshold to the image
        self.otsu_button = tk.Button(self.bottom_frame, bg=self.background_header_button_color, text="Otsu Threshold", font=('Arial', self.fz_xmd), width=20, command=self.otsu_threshold)
        self.otsu_button.pack(anchor = "s", side='left', padx=50, pady=25)#( side = "bottom")#(anchor = "s")#

        # Create a button to save the image
        self.save_button = tk.Button(self.bottom_frame,fg=self.background_important_button_color, bg=self.background_header_button_color, text="Save Image", font=('Arial', self.fz_xmd), width=20, command=self.save_image)
        self.save_button.pack(anchor = "s", side='left', padx=50, pady=25)#( side = "bottom")#(anchor = "s")#

        # Create a button to save the history process
        self.history_button = tk.Button(self.bottom_frame,fg=self.background_important_button_color, bg=self.background_header_button_color, text="Save History", font=('Arial', self.fz_xmd), width=20, command=self.save_history)
        self.history_button.pack(anchor = "s", side='left', padx=50, pady=25)#( side = "bottom")#(anchor = "s")#
        
        # Create a button to save the histogram process
        self.histogram_button = tk.Button(self.bottom_frame,fg=self.background_important_button_color, bg=self.background_header_button_color, text="Save Histogram", font=('Arial', self.fz_xmd), width=20, command=self.save_histogram)
        self.histogram_button.pack(anchor = "s", side='left', padx=50, pady=25)#( side = "bottom")#(anchor = "s")#

    def minimize_window(self):
        self.iconify()

    def close_window(self):
        # self.destroy()
        proceed = askyesno('Quit', 'Quit?')
        proceed = bool(proceed) # So it is a bool

        if proceed:
            self.quit()
        else:
            # You don't really need to do this
            pass

    def open_helpPage(self):
        webbrowser.open_new("https://drive.google.com/file/d/1-MgFsss6qrnetYDDEAJwozX1AoTjc367/view?usp=share_link")
    
    def open_homepage(self):
        webbrowser.open_new("http://lmmp.mec.puc-rio.br/lmmp/")

    def upload_image(self):
        # Open a file dialog and get the path of the selected file
        filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp, *.tif, *.jtif")]
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=filetypes)
        
        # Check if a file was selected
        if file_path:

            # Create a PhotoImage object from the selected file
            self.file_path = file_path
            self.original_image = Image.open(self.file_path)
            self.original_size = self.original_image.size
            self.original_image.thumbnail(self.size)
            self.image = self.original_image.copy()

            # Resize image to fit canvas and convert to PhotoImage
            # self.image = self.image.resize(self.size , Image.LANCZOS)
            
            # print(f'tamanho display desejado {self.size}') 
            self.photo_image = ImageTk.PhotoImage(self.image)

            # Create a canvas widget to display the image
            canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
            canvas.place(relx=0, rely=0.5, anchor=tk.W, y=10)
            canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            print('passei aqui e exibi?')
            # self.update_image()
            
            # initialize the filters parameters
            self.contrast_value = 1.0
            self.threshold_value = None
            self.histogram_data = None  
            # print(f'tamanho original {self.original_size}')
            plt.clf()
            plt.hist(self.image.histogram(), weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))
            self.histogram_canvas.figure.clear()
            self.histogram_data, _ = np.histogram(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))       
            self.hist = self.f_hist.gca()
            self.hist.hist(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))#(self.image.histogram(), bins=256, range=(0, 256))
            self.hist.set_xlabel('Pixel Value', fontsize = 12)
            self.hist.set_title('Pixel Histogram', fontsize = 12)
            
            self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
            # p.yaxis.set_label('Percentual')
            # self.histogram_canvas.figure.add_subplot(111).hist(self.image.histogram(), bins=256, range=(0, 256))
            self.histogram_canvas.draw()
    
    def update_image(self):
        # Resize image to fit canvas and convert to PhotoImage
        # self.image = self.image.resize(self.size , Image.LANCZOS)
        self.image.thumbnail(self.size)
        self.photo_image_update = ImageTk.PhotoImage(self.image)

        # Update canvas image and keep reference to prevent garbage collection
        self.image_canvas.delete("all")
        self.image_canvas.create_image(0, 0, anchor="nw", image=self.photo_image_update)
        self.image_canvas.image = self.photo_image_update


        plt.clf()
        plt.hist(self.image.histogram(), bins=256, range=(0, 256))
        self.histogram_canvas.figure.clear()

        self.hist = self.f_hist.gca()
        self.histogram_data, _ = np.histogram(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))
        self.hist.hist(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))#(self.image.histogram(), bins=256, range=(0, 256))
        self.hist.set_xlabel('Pixel Value', fontsize = 12)
        self.hist.set_title('Pixel Histogram', fontsize = 12)
            
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        # self.histogram_canvas.figure.add_subplot(111).hist(self.image.histogram(), bins=256, range=(0, 256))
        self.histogram_canvas.draw()
        # print('passei aqui 1')

    def update_contrast(self, value):
        # Update the contrast of the image based on the current scale value
        enhancer = ImageEnhance.Contrast(self.original_image)
        # contrasted_img = enhancer.enhance(float(value))
        self.image = enhancer.enhance(float(value))
        # Resize image to fit canvas and convert to PhotoImage
        # self.image = self.image.resize(self.size , Image.LANCZOS)
        self.image.thumbnail(self.size)

        # Update the label with the new image
        self.photo_image = ImageTk.PhotoImage(self.image)
        # self.image_canvas.configure(image=self.photo_image)

        canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        canvas.place(relx=0, rely=0.5, anchor=tk.W, y=10)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        # Store a reference to the modified image
        self.modified_img = self.image.copy() 
        
        # Resize image to fit canvas and convert to PhotoImage
        # self.modified_img = self.modified_img.resize(self.original_size , Image.LANCZOS)
        plt.clf()
        plt.hist(self.image.histogram(), bins=256, range=(0, 256))

        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))        
        self.hist = self.f_hist.gca()
        self.hist.hist(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))#(self.image.histogram(), bins=256, range=(0, 256))
        self.hist.set_xlabel('Pixel Value', fontsize = 12)
        self.hist.set_title('Pixel Histogram', fontsize = 12)
            
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        # self.histogram_canvas.figure.add_subplot(111).hist(self.image.histogram(), bins=256, range=(0, 256))
        self.histogram_canvas.draw()

    def save_image(self):
        files = [("Image Files (png)", "*.png "),
                 ("Image Files (jpg)","*.jpg *"),
                 ("Image Files (tif)","*.tif *"),
                 ("Image Files (jtif)","*.jtif *")]
        # Prompt the user to choose a file name to save the modified image
        file_name = tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files)

        # If the user cancels the dialog, do nothing
        if not file_name:
            return
        # Save the modified image to the chosen file name
        self.modified_img.save(file_name)


    def otsu_threshold(self):
        # print('cheuei nesse ponto')
        # Convert image to grayscale and get pixel values
        self.image_gray = self.image.convert("L")
        pixels = np.array(self.image_gray.getdata())

        # Compute Otsu threshold and binary transform
        self.threshold_value = threshold_otsu(pixels)
        # print(self.threshold_value)
        # print(type(self.threshold_value))
        self.image_binary = self.image_gray.point(lambda x: 0 if x < self.threshold_value else 255)

        # # Compute histogram data and plot histogram
        # self.histogram_data, _ = np.histogram(pixels, bins=256, range=(0, 256))
        # self.hist_plot.clear()
        # self.hist_plot.plot(self.histogram_data)
        # self.hist_plot.axvline(x=self.threshold_value, color="r")
        # self.hist_canvas.draw()

        # Update image display
        self.photo_image = ImageTk.PhotoImage(self.image_binary)
        canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        canvas.place(relx=0, rely=0.5, anchor=tk.W, y=10)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        plt.clf()
        plt.hist(self.image.histogram(), bins=256, range=(0, 256))

        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))       
        self.hist = self.f_hist.gca()
        self.hist.hist(self.image.histogram(), bins=20, weights=np.ones(len(self.image.histogram()))/len(self.image.histogram()), range=(0, 256))#(self.image.histogram(), bins=256, range=(0, 256))
        self.hist.axvline(self.threshold_value, color='r', ls='--')
        self.hist.set_xlabel('Pixel Value', fontsize = 12)
        self.hist.set_title('Pixel Histogram', fontsize = 12)
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        # self.histogram_canvas.figure.add_subplot(111).hist(self.image.histogram(), bins=256, range=(0, 256))

        self.histogram_canvas.draw()
        self.modified_img = self.image_binary.copy()
    
    def save_histogram(self):
        files = [("Image Files (png)", "*.png "),
                 ("Image Files (jpg)","*.jpg *"),
                 ("Image Files (tiff)","*.tiff *")]
        # Prompt the user to choose a file name to save the modified image
        file_name = tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files)

        # If the user cancels the dialog, do nothing
        if not file_name:
            return
        # Save the modified image to the chosen file name
        self.hist.figure.savefig(file_name)# self.histogram_canvas.save(file_name)
    
    
    def save_history(self):
        # Prompt user for file name and directory
        filename = simpledialog.askstring("Save History", "Enter a file name:", initialvalue="history.txt")
        directory = filedialog.askdirectory(title="Select Directory to Save History")

        if filename and directory:
            # Create string with processing history data
            history_data = f"Image file path: {self.file_path}\nContrast value: {self.contrast_value}\n"

            if self.threshold_value is not None:
                history_data += f"Otsu threshold value: {self.threshold_value}\n"

            if self.histogram_data is not None:
                history_data += "Histogram data:\n"
                for i, value in enumerate(self.histogram_data):
                    history_data += f"{i}: {value}\n"

            # Write string to text file
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as f:
                f.write(history_data)

if __name__ == '__main__':
    app = FullScreenApp()
    app.mainloop()