import tkinter as tk
import webbrowser
from tkinter import filedialog
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
        file_path = filedialog.askopenfilename()
        
        # Check if a file was selected
        if file_path:
            # Create a PhotoImage object from the selected file
            image = Image.open(file_path)
            photo_image = ImageTk.PhotoImage(image)
            
            # Display the image in a Label widget on the left side of the window
            image_label = tk.Label(self, image=photo_image)
            image_label.pack(side="left", padx=10, pady=10)
            
            # Store the PhotoImage object in a list to prevent it from being garbage collected
            self.photo_images.append(photo_image)

if __name__ == '__main__':
    app = FullScreenApp()
    app.mainloop()
