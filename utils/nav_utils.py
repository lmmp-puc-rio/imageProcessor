from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from utils.resize_image import resize_image

import webbrowser


def home_page():
    webbrowser.open_new(r"http://tmp-lmmp.mec.puc-rio.br/")

def help_page():
    webbrowser.open_new(r"https://drive.google.com/file/d/1-MgFsss6qrnetYDDEAJwozX1AoTjc367/view?usp=share_link")

def close_app(app):
    # self.destroy()
    proceed = askyesno('Quit Application', 'Do you want to quit the Image Processor?')
    proceed = bool(proceed) # So it is a bool

    if proceed:
        app.destroy()
    else:
        # You don't really need to do this
        pass

def minimize_app(app):
    app.iconify()

#def upload_img():
 #   filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp, *.tif, *.jtif")]
  #  filename = askopenfilename(initialdir="/images", text="Select Image", filetypes= filetypes)
   # if filename:
    #        image = Image.open(filename)
     #       resized_image = resize_image(image, (400, 300))
      #      self.displayed_image = ImageTk.PhotoImage(resized_image)

       #     if hasattr(self, "image_label"):
        #        self.image_label.config(image=self.displayed_image)
         #   else:
          #      self.image_label = tk.Label(self.display_frame, image=self.displayed_image)
           #     self.image_label.pack()