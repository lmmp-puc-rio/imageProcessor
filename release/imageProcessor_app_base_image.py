import tkinter as tk
import webbrowser
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageEnhance

class FullScreenApp(tk.Tk):
    def __init__(self):
        super().__init__()

        #Colors used in the app

        self.background_header_color = '#767272'
        self.background_header_button_color = 'white'
        self.background_header_button_font_color = 'black'

        # Set the app title in the title bar
        self.title('Image Processor')

        # Set the window attributes to keep the title bar visible
        self.attributes('-alpha')
        self.overrideredirect(False)

        # Set the window state to maximized
        self.wm_state('zoomed')

        # Create a frame for the header
        self.header_frame = tk.Frame(self, bg=self.background_header_color, height=50)
        self.header_frame.pack(side='top', fill='x')

        # Add a logo to the header with hyperlink to google homepage
        self.logo_image = tk.PhotoImage(file='logo.png')
        self.logo_label = tk.Label(self.header_frame, image=self.logo_image, bg=self.background_header_color)
        self.logo_label.pack(side='left', padx=10, pady=5)
        self.logo_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.google.com"))

        # # Add minimize and close buttons to the window
        # self.minimize_button = tk.Button(self.header_frame, text='-', font=('Arial', 16), bg=self.background_header_color, fg='white', command=self.minimize_window)
        # self.minimize_button.pack(side='right', padx=5, pady=5)

        # self.close_button = tk.Button(self.header_frame, text='x', font=('Arial', 16), bg=self.background_header_color, fg='white', command=self.close_window)
        # self.close_button.pack(side='right', padx=5, pady=5)

        # Add a button to the header with hyperlink to LMMP homepage
        self.google_button = tk.Button(self.header_frame, text='Homepage', font=('Arial', 12), bg=self.background_header_button_color, fg=self.background_header_button_font_color, command=self.open_homepage)
        self.google_button.pack(side='right', padx=10, pady=5)

        # Add a button to the header with hyperlink to Help homepage
        self.google_button = tk.Button(self.header_frame, text='Help', font=('Arial', 12), bg=self.background_header_button_color, fg=self.background_header_button_font_color, command=self.open_helpPage)
        self.google_button.pack(side='right', padx=10, pady=5)

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.header_frame, bg=self.background_header_color)
        self.button_frame.pack(side='right', padx=10, pady=5)

        # Add an upload button to the button frame
        self.upload_button = tk.Button(self.button_frame, text='Upload Image', font=('Arial', 12), bg=self.background_header_button_color, fg=self.background_header_button_font_color, command=self.upload_image)
        self.upload_button.pack(side='left', padx=5, pady=5)

        # Create a frame for the content
        self.content_frame = tk.Frame(self, bg='white')
        self.content_frame.pack(side='top', fill='both', expand=True)

        # Create the espace for the loaded image
        self.image_canvas = tk.Canvas(self, width=500, height=500)
        # self.image_canvas.grid(row=0, column=1, rowspan=4, padx=10, pady=10)

    def minimize_window(self):
        self.iconify()

    def close_window(self):
        self.destroy()

    def open_helpPage(self):
        webbrowser.open_new("https://drive.google.com/file/d/1-MgFsss6qrnetYDDEAJwozX1AoTjc367/view?usp=share_link")
    
    def open_homepage(self):
        webbrowser.open_new("http://lmmp.mec.puc-rio.br/lmmp/")

    def upload_image(self):
        # Open a file dialog and get the path of the selected file
        filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=filetypes)
        
        # Check if a file was selected
        if file_path:

            # Create a PhotoImage object from the selected file
            self.file_path = file_path
            self.original_image = Image.open(self.file_path)
            self.image = self.original_image.copy()
            # Resize image to fit canvas and convert to PhotoImage
            self.image = self.image.resize((500, 500), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(self.image)

            # Create a canvas widget to display the image
            canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
            canvas.place(relx=0, rely=0.5, anchor=tk.W, y=10)
            canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

            # initialize the filters parameters
            self.contrast_value = 1.0
            self.threshold_value = None
            self.histogram_data = None                              

if __name__ == '__main__':
    app = FullScreenApp()
    app.mainloop()
