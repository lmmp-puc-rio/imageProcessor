from tkinter.messagebox import askyesno
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
