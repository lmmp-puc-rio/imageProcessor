

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matplotlib.ticker as mtick
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
from skimage.filters import threshold_otsu,threshold_triangle,gaussian
from utils.resize_image import resize_image, resize_image_predifined
from utils.nav_utils import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import cv2

class FullScreenApp(tk.Tk):

    def __init__(self):
        super().__init__()
        
        ###############
        #Basic config
        ###############
        self.attributes("-fullscreen", True)
        self.overrideredirect(False)

        #colors in app
        self.pry_color = "#5376D6"
        self.sec_color = "#CFCECE"
        self.btn_color = "#6484DA"
        self.bg_container_color = "#DEDDDD"

        #font
        self.font='Monstserrat'

        # Set the app title in the title bar
        self.title('Image Processor')

        #font sizes
        self.fz_mn = 12
        self.fz_md = 14
        self.fz_lg = 18
        self.fz_xl = 22

        #root config
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=9)
        self.rowconfigure(2, weight=1)

        #title
        self.title("Image Processor")

        # Change the icon of the application
        #icon_path = r"/home/renan/Repositorio/imageProcessor/src/images/lmmp_200x65.ico"  # trocar por uma imagem de tamanho ideal
        #self.iconbitmap(icon_path)


        #variables
        self.contrast_value = 1.0
        self.threshold_value = None
        self.histogram_data = None  
        self.original_size = None 
        self.blur_value = 0
        self.image_original = None
        self.image_original_tk = None
        self.image_edited = None
        self.image_edited_tk = None
        self.original_edited_width = None
        self.original_edited_height = None
        self.image_without_blur = None
        self.num_of_bins = int(256/2)

        ###############
        #top frame
        ###############

        self.header_frame = tk.Frame(self, background = self.pry_color)
        self.header_frame.columnconfigure(0, weight=0)
        self.header_frame.columnconfigure(1, weight=8)
        self.header_frame.columnconfigure(2, weight=1)

        #home button
        self.img_home= (Image.open(r'/home/renan/Repositorio/imageProcessor/src/images/logo_grey.png'))
        self.btn_home_img = resize_image(self.img_home,(240,100))
        self.btn_home_model = ImageTk.PhotoImage(self.btn_home_img)
        self.home_btn = tk.Button(self.header_frame, image= self.btn_home_model, background= self.pry_color, borderwidth=0, highlightthickness = 0 , activebackground= self.btn_color,relief='sunken', command=home_page)
        self.home_btn.bind("<Button-1>", lambda x: self.webbrowser.open_new("http://tmp-lmmp.mec.puc-rio.br/"))
        
        #upload button
        self.img_upload= (Image.open(r'src/images/upld_btn.png'))
        self.btn_img_upload_img = resize_image(self.img_upload,(200,100))
        self.btn_img_upload_model = ImageTk.PhotoImage(self.btn_img_upload_img)
        self.upload_btn = tk.Button(self.header_frame, image=self.btn_img_upload_model,bg= self.pry_color, borderwidth=0,highlightthickness = 0, activebackground=self.pry_color, command=self.upload_image)

        #help button
        self.img_help= (Image.open(r'src/images/help_img.png'))
        self.btn_img_help_img = resize_image(self.img_help,(200,100))
        self.btn_img_help_model = ImageTk.PhotoImage(self.btn_img_help_img)
        self.help_btn = tk.Button(self.header_frame, image = self.btn_img_help_model, bg= self.pry_color, borderwidth=0,highlightthickness = 0,  activebackground=self.pry_color, command=help_page)

        #close button
        self.img_close= (Image.open(r'src/images/cls_btn.png'))
        self.btn_img_close_img = resize_image_predifined(self.img_close,(35,30))
        self.btn_img_close_model = ImageTk.PhotoImage(self.btn_img_close_img)
        self.close_btn = tk.Button(self.header_frame, image=self.btn_img_close_model,bg= self.pry_color, borderwidth=0,highlightthickness = 0, activebackground=self.pry_color, command=self.quit_application)

        #minimize button
        self.img_minimize= (Image.open(r'src/images/min_btn.png'))
        self.btn_img_minimize_img = resize_image_predifined(self.img_minimize,(35,30))
        self.btn_img_minimize_model = ImageTk.PhotoImage(self.btn_img_minimize_img)
        self.minimize_btn = tk.Button(self.header_frame, image=self.btn_img_minimize_model,bg= self.pry_color, borderwidth=0, highlightthickness = 0, activebackground=self.pry_color, command=self.minimize_application)

        #top widget
        self.header_frame.grid(row=0, column=0, sticky='WENS')
        self.home_btn.grid(row= 0 , column= 0, sticky ='W', ipady=5, ipadx=7)
        self.upload_btn.grid(row= 0 , column= 1, padx=(0,255), sticky ='E', pady=2)
        self.help_btn.grid(row= 0 , column= 1, padx=(0,50), sticky ='E', pady=2)
        self.minimize_btn.grid(row= 0 , column= 2, sticky ='E', padx=(0,45), pady=2)
        self.close_btn.grid(row= 0 , column= 2, sticky ='E', padx=(2,5), pady=2)

        ###############
        #main
        ###############

        #main Segmentation
        self.main_frame = tk.Frame(self, background= self.bg_container_color)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=0)

        #main Elemnts txt
        self.original_txt = tk.Label(self.main_frame, text='Original Image',font= (self.font, self.fz_lg, 'bold'), background= self.bg_container_color )
        self.edited_txt = tk.Label(self.main_frame, text='Edited Image', font= (self.font, self.fz_lg, 'bold'), background= self.bg_container_color )
        self.histogram_txt = tk.Label(self.main_frame, text='Pixel Histogram', font= (self.font, self.fz_lg, 'bold'), background= self.bg_container_color )

        #main Elemnts Canvas
        self.original_img_label= tk.Label(self.main_frame, background = self.sec_color)
        self.edited_img_label = tk.Label(self.main_frame, background = self.sec_color)
        self.histogram_img_label = tk.Label(self.main_frame, background = self.sec_color)
        self.histogram_inner_frame = tk.Frame(self.histogram_img_label)

        self.histogram_img_label.rowconfigure(0, weight=1)
        self.histogram_img_label.rowconfigure(1, weight=1)
        self.histogram_img_label.rowconfigure(2, weight=1)

        self.histogram_inner_frame.grid(row=1, column=0)

        #histogram
        self.histogram_container = plt.Figure()
        self.histogram_container.patch.set_facecolor(self.sec_color)
        self.histogram_canvas = FigureCanvasTkAgg(self.histogram_container, master=self.histogram_inner_frame)
        self.histogram_canvas.get_tk_widget().pack( fill='both')
    
        #main Position
        self.main_frame.grid(row=1, column=0, sticky='WENS')

        self.original_txt.grid(row=0, column=0, sticky='N', pady=(6,2))
        self.edited_txt.grid(row=0, column=1, sticky='N', pady=(6,2))
        self.histogram_txt.grid(row=0, column=2, sticky='N', pady=(6,2))

        self.original_img_label.grid(row=1, column=0, sticky='WENS',padx=1.5, pady=3)
        self.edited_img_label.grid(row=1, column=1, sticky='WENS',padx=1.5, pady=3)
        self.histogram_img_label.grid(row=1, column=2, sticky='WENS',padx=1.5,pady=3)

        ###############
        #footer frame
        ###############

        self.footer_frame = tk.Frame(self, background=self.pry_color, height=50)
        self.footer_frame.rowconfigure(0, weight=1)

        self.footer_frame.grid(row=2, column=0, sticky='WENS')
        
        self.footer_frame.columnconfigure(0, weight=0)
        self.footer_frame.columnconfigure(1, weight=0)
        self.footer_frame.columnconfigure(2, weight=1)

        self.contrast_frame = tk.Frame(self.footer_frame, background=self.pry_color)
        self.treshold_frame = tk.Frame(self.footer_frame, background=self.pry_color)
        self.save_frame = tk.Frame(self.footer_frame, background=self.pry_color, bg=self.pry_color)


        #footer Wdiget
   
        self.contrast_frame.grid(row=0, column=0,sticky='WENS', ipadx=3,padx=2, pady=3)
        self.treshold_frame.grid(row=0, column=1,sticky='WENS', ipadx=3,padx=2, pady=3)
        self.save_frame.grid(row=0, column=2,sticky='WENS', ipadx=3,padx=2, pady=3)


        #Contrast Frame
        self.contrast_frame.columnconfigure(0, weight=0)
        self.contrast_frame.columnconfigure(1, weight=0)
    
        self.contrast_frame.rowconfigure(0, weight=1)
        self.contrast_frame.rowconfigure(1, weight=1)
        self.contrast_frame.rowconfigure(2, weight=1)
        self.contrast_frame.rowconfigure(3, weight=1)
        self.contrast_frame.rowconfigure(4, weight=1)


        #scale bar

        self.value_scale = tk.StringVar()
        self.text_contrast = tk.Label(self.contrast_frame, text='CONTRAST',font= (self.font, self.fz_lg, 'bold'),anchor=tk.N, background= self.pry_color)
        self.bar_contrast = tk.Scale(self.contrast_frame, from_=0.1, to=5.0,orient='horizontal',font = (self.font, self.fz_mn),tickinterval= 0.5, resolution=0.1, label="Value",
                                troughcolor = self.sec_color, variable = self.value_scale ,bg= self.pry_color, border=None ,highlightthickness = 0, activebackground=self.pry_color, command = self.update_scale)
        self.text_contrast.grid(row=0, column=0,columnspan=2, sticky='NS', padx=3, pady=(5,10))
        self.bar_contrast.grid(row=1, column=0,columnspan=2, sticky='EW', padx=25, pady=5, ipadx=5, ipady=5)

        #blur filter
        self.radio_blur_selected = tk.StringVar(value='deactivated')
        self.blur_text = tk.Label(self.contrast_frame, text = 'BLUR', font = (self.font, self.fz_md, 'bold'), anchor=tk.N, background=self.pry_color)
        self.blur_text.grid(row=2, column=0, columnspan=3, sticky='N')

        #blur configs
        self.blur_label1 = tk.Label(self.contrast_frame,  background= self.pry_color)
        self.blur_label1.grid(row=3, column=0, sticky='w')
        self.blur_label1.columnconfigure(0,weight=0)
        self.blur_label1.columnconfigure(1,weight=0)
        self.radio1_btn_blur =tk.Radiobutton(self.blur_label1, text='Activated', variable = self.radio_blur_selected, value= "activated",  anchor=tk.W, bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font, self.fz_mn))
        self.radio2_btn_blur =tk.Radiobutton(self.blur_label1, text='Deactivated', variable = self.radio_blur_selected, value= "deactivated",  anchor=tk.E, bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font, self.fz_mn))
        self.radio1_btn_blur.grid(row= 0, column= 0, padx=(20,10)) 
        self.radio2_btn_blur.grid(row= 0, column= 1, padx=(10,20))

        self.blur_label2 = tk.Label(self.contrast_frame,  background= self.pry_color)
        self.blur_label2.columnconfigure(0,weight=0)
        self.blur_label2.columnconfigure(0,weight=1)
        self.blur_label2.columnconfigure(0,weight=2)

        self.blur_label2.grid(row=3, column=1, sticky='W')

        self.blur_value_label = tk.Label(self.blur_label2,  text='Blur Value: ', bg= self.pry_color,font= (self.font, self.fz_mn))
        self.blur_value_textbox = tk.Text(self.blur_label2,  width=2, height=1, font=(self.font, self.fz_md))
        self.blur_text_box_alert = tk.Label(self.blur_label2, anchor=tk.S,  text='* only use values between 1 and 9.',font=(self.font, 8), bg= self.pry_color)
        self.blur_text_box_alert_hidden = tk.Label(self.blur_label2, bg= self.pry_color) # create a label for hide the alert in the screen
        
        #image blur btn
        self.blur_btn_img= (Image.open(r'src/images/blur_btn.png'))
        self.btn_blur_btn_img = resize_image(self.blur_btn_img,(120,30))
        self.btn_blur_btn = ImageTk.PhotoImage(self.btn_blur_btn_img)
        self.btn_run_blur = tk.Button(self.contrast_frame, image=self.btn_blur_btn,bg= self.pry_color, borderwidth=0,highlightthickness = 0, activebackground=self.pry_color, command = self.apply_blur)

        self.blur_value_label.grid(row= 0, column=0, padx=6)
        self.blur_value_textbox.grid(row= 0, column=1, padx=6)
        self.blur_text_box_alert.grid(row= 0, column=2, padx=6)
        self.blur_text_box_alert_hidden.grid(row= 0, column=2,sticky='WENS', padx=6)
        self.blur_value_textbox.config(state='disabled')
        self.blur_value_textbox.bind("<Key>", self.validate_blur_value)

        self.btn_run_blur.grid(row=4, column=0, columnspan=2, sticky="N", pady=5)

        # monitora cada mudança no radio button do blur para ativar ou desativar a caixa de texto do blur
        self.radio_blur_selected.trace("w", lambda *args: self.verify_blur())

        #treshold Frame
        self.radio_selected = 0

        self.treshold_frame.columnconfigure(0, weight=3)
        self.treshold_frame.columnconfigure(1, weight=3)

        self.treshold_frame.rowconfigure(0, weight=1)
        self.treshold_frame.rowconfigure(1, weight=1)
        self.treshold_frame.rowconfigure(2, weight=1)
        self.treshold_frame.rowconfigure(3, weight=1)
        self.treshold_frame.rowconfigure(4, weight=1)

        
        #combobox
        self.list_treshold_model = ['OTSU', 'TRIANGLE']
        self.clicked_model = tk.StringVar()
        self.clicked_model.set(self.list_treshold_model[0])
        self.combobox_models = ttk.Combobox(self.treshold_frame, values=self.list_treshold_model, font= (self.font, self.fz_md), state="readonly", takefocus=None)
        self.combobox_models.current(0)
        
        #radioBtn Treshhold
        self.radio_selected = tk.StringVar(value="automatic")
        self.radio1_btn_treshold =tk.Radiobutton(self.treshold_frame,text='Automatic', variable = self.radio_selected, value= "automatic", bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font, self.fz_md))
        self.radio2_btn_treshold =tk.Radiobutton(self.treshold_frame,text='Manual', variable = self.radio_selected, value= "manual", bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font, self.fz_md))
        
        
        #Model Value and alert msg
        self.value_model_label = tk.Label(self.treshold_frame, bg=self.pry_color)

        self.value_model_label.columnconfigure(0, weight=1)
        self.value_model_label.columnconfigure(1, weight=1)
        self.value_model_label.columnconfigure(2, weight=1)

        self.value_treshold = tk.Label(self.value_model_label, text= 'Value: ', bg= self.pry_color,highlightthickness = 0, font = (self.font, self.fz_mn))
        self.text_box_treshold = tk.Text(self.value_model_label, width=4, height=1, font=(self.font, self.fz_md))
        self.text_box_alert = tk.Label(self.value_model_label, text='* only use values between 0 and 255.',font=(self.font, 8), bg= self.pry_color)
        self.text_box_alert_hidden = tk.Label(self.value_model_label, bg= self.pry_color) # create a label for hide the alert in the screen

        
        # monitora cada mudança na variavel para chamar a função automaticamente
        self.radio_selected.trace("w", lambda *args: self.on_radio_select())

        # value treshold starts disabled
        self.text_box_treshold.config(state='disabled')

        #btn Run Model
        self.run_model_img= (Image.open(r'src/images/run_btn.png'))
        self.btn_run_model_img = resize_image(self.run_model_img,(200,100))
        self.btn_run_model = ImageTk.PhotoImage(self.btn_run_model_img)
        self.treshold_label = tk.Label(image=self.btn_run_model, background= self.pry_color)
        self.treshold_btn = tk.Button(self.treshold_frame, image=self.btn_run_model,bg= self.pry_color, borderwidth=0, activebackground=self.pry_color,highlightthickness = 0, command= self.on_treshold_btn_click)
        
        #btn Reset Project
        self.reset_project_img= (Image.open(r'src/images/reset_btn.png'))
        self.btn_reset_project_img = resize_image(self.reset_project_img,(200,100))
        self.btn_reset_project = ImageTk.PhotoImage(self.btn_reset_project_img)
        self.reset_label = tk.Label(image=self.btn_reset_project, background= self.pry_color)
        self.reset_btn = tk.Button(self.treshold_frame, image=self.btn_reset_project, bg= self.pry_color, borderwidth=0, activebackground=self.pry_color,highlightthickness = 0, command= self.reset_project)
        

        #treshold Widget 

        self.text_treshold = tk.Label(self.treshold_frame, text='TRESHOLD',font= (self.font, self.fz_lg, 'bold'), background= self.pry_color)
        self.text_treshold.grid(row=0, column=0,columnspan=2,sticky='N', padx=3, pady=5)
        self.combobox_models.grid(row=1, column=0,sticky='N', padx=5, pady=5)
        self.radio1_btn_treshold.grid(row=2, column=0,sticky='N', padx=5, pady=2)
        self.treshold_btn.grid(row=2, column=1, columnspan=2,padx=(55,0), pady=5)
        self.reset_btn.grid(row=3, column=1, columnspan=2, padx=(55,0),pady=5)
        self.radio2_btn_treshold.grid(row=3, column=0, sticky='N', padx=5, pady=2)

        self.value_model_label.grid(row=4,column=0, columnspan=2, sticky='N')
        self.value_treshold.grid(row=0, column=0,sticky='E',padx=(30,0), pady=5)
        self.text_box_treshold.grid(row=0, column=1,sticky='N', padx=(30,0), pady=2)
        self.text_box_alert.grid(row=0, column=2,sticky='S', padx= (12,0))
        self.text_box_alert_hidden.grid(row=0, column=2,sticky='WENS', padx= (12,0))
        self.text_box_treshold.bind("<Key>", self.validate_model_value)


        #Save Frame

        self.save_frame.columnconfigure(0, weight=1)
        self.save_frame.columnconfigure(1, weight=0)
        self.save_frame.rowconfigure(0, weight=1)
        self.save_frame.rowconfigure(1, weight=1)
        self.save_frame.rowconfigure(2, weight=1)
        self.save_frame.rowconfigure(3, weight=1)
        self.save_frame.rowconfigure(4, weight=1)

        #checkbox widget

        text_checkbox = tk.Label(self.save_frame, text='SAVE PROJECT',font= (self.font, self.fz_lg, 'bold'), background= self.pry_color)

        #Check Box
        self.img_save_value = tk.IntVar()
        self.history_save_value = tk.IntVar()
        self.histogram_save_value = tk.IntVar()             

        self.checkbox1_frame = tk.Checkbutton(self.save_frame, text="SAVE IMAGE", variable = self.img_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font, self.fz_md),highlightthickness = 0)
        self.checkbox2_frame = tk.Checkbutton(self.save_frame, text="SAVE HISTORY", variable = self.history_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font, self.fz_md),highlightthickness = 0)
        self.checkbox3_frame = tk.Checkbutton(self.save_frame, text="SAVE HISTOGRAM", variable = self.histogram_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font, self.fz_md),highlightthickness = 0)

        #Load an image for the save btn
        self.img= (Image.open(r'src/images/save_btn.png'))
        self.img = resize_image(self.img,(200,100))
        self.img_save = ImageTk.PhotoImage(self.img)
        self.img_save_label = tk.Label(image=self.img_save, background= self.pry_color)
        self.save_btn = tk.Button(self.save_frame, image=self.img_save,bg= self.pry_color, borderwidth=0,highlightthickness = 0, activebackground=self.pry_color, command= self.save_files, anchor='e')

        #self.text_checkbox.grid(row=0, column=0,columnspan=2, sticky='N', padx=2, pady=3)
        self.checkbox1_frame.grid(row=1, column=0, sticky='w', padx=(75,0), pady=3)
        self.checkbox2_frame.grid(row=2, column=0, sticky='w', padx=(75,0), pady=3)
        self.checkbox3_frame.grid(row=3, column=0, sticky='w', padx=(75,0), pady=3)
        self.save_btn.grid(row=2, column=1, sticky='e', padx=(2,20), pady=3)
      

    def quit_application(self):
            close_app(self)
    
    def minimize_application(self):
            minimize_app(self)   
    
    #Show the scale value in real time
    def update_scale(self, *args):
        self.contrast_value = self.value_scale.get()
        self.update_contrast(self.image_original, self.contrast_value)
    
    #validate user input in blur value
    def validate_blur_value(self, event):
        
        def validate_input( P):
            return P.isdigit() and 1 <= int(P) <= 9
        

        def on_validate_input( P):
            return validate_input(P) or P == ""


        if event.char == '\x08':  # Check for backspace character
            return  # Allow backspace

        #current_position = self.text_box_treshold.index(tk.INSERT)
        current_char = event.char
        new_value = self.blur_value_textbox.get("1.0", "end-1c") + current_char
    
        if not on_validate_input(new_value):
            self.blur_text_box_alert_hidden.grid_remove()#row=0, column=2,sticky='S',columnspan=2, padx=(135,0), pady=(16,0))
            return "break"  
    
    #validate user input in treshold value
    def validate_model_value(self, event):
        
        def validate_input( P):
            return P.isdigit() and 0 <= int(P) <= 255
        

        def on_validate_input( P):
            return validate_input(P) or P == ""


        if event.char == '\x08':  # Check for backspace character
            return  # Allow backspace

        #current_position = self.text_box_treshold.index(tk.INSERT)
        current_char = event.char
        new_value = self.text_box_treshold.get("1.0", "end-1c") + current_char
    
        if not on_validate_input(new_value):
            self.text_box_alert_hidden.grid_remove()#row=0, column=2,sticky='S',columnspan=2, padx=(135,0), pady=(16,0))
            return "break"  
            
    # verifica sempre que o radio button muda de auto para manual, dessa forma mudando o estado do TextBox
    def on_radio_select(self):
        if self.radio_selected.get() == "automatic":
            self.text_box_treshold.config(state='disabled')

        else:
            self.text_box_treshold.config(state='normal')
    
    #verifica sempre que o blur radio button muda para ativo
    def verify_blur(self):
        selected_item = self.radio_blur_selected.get()
        self.blur_value = self.blur_value_textbox.get("1.0","2.0")

        if selected_item == "activated":
            self.blur_value_textbox.config(state='normal')
        else:
            self.blur_value_textbox.config(state='disabled')
    
    def apply_blur(self):
 
        #create a copy of the photo so you don't apply blur on top of blur, that way you always apply it to the image without blur
        image = self.image_without_blur

        self.blur_value = int(self.blur_value_textbox.get("1.0","2.0"))

    
        # Convert the PIL image to a NumPy array
        image_array = np.array(image)


        # Apply Gaussian blur using OpenCV
        blurred_image = cv2.GaussianBlur(image_array, (0, 0), self.blur_value)
        # blurred_image = cv2.GaussianBlur(image_array, (3, 3),1)

        # Convert the NumPy array back to a PIL image

        blurred_image = Image.fromarray(blurred_image)

        #w, h = blurred_image.size
                
        self.image_edited = blurred_image
        

        self.update_image(self.image_edited)

        plt.clf()
        plt.hist(self.image_edited.histogram(), bins=self.num_of_bins, range=(0, 256))

        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(self.image_edited.histogram(), bins=self.num_of_bins, weights=np.ones(len(self.image_edited.histogram()))/len(self.image_edited.histogram()), range=(0, 256))        
        self.hist = self.histogram_container.gca()
        self.hist.hist(self.image_edited.histogram(), bins=self.num_of_bins,weights=np.ones(len(self.image_edited.histogram()))/len(self.image_edited.histogram()), range=(0, 256))#(photo.histogram(), bins=256, range=(0, 256))
        self.hist.set_xlabel('Pixel Value', fontsize = 12)
        self.hist.set_title('Pixel Histogram', fontsize = 12)
            
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        self.histogram_canvas.draw()

    
    def on_treshold_btn_click(self):

        selected_item = self.combobox_models.get()
        self.text_box_alert_hidden.grid()
        self.blur_text_box_alert_hidden.grid()

        if selected_item == self.list_treshold_model[0]:
            self.otsu_threshold(self.image_edited)

        elif selected_item == self.list_treshold_model[1]:
            self.triangle_threshold(self.image_edited)

    def show_histogram(self, photo):
        rcParams['font.weight'] = 'bold'       
        plt.clf()
        plt.hist(photo.histogram(), weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))
        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(photo.histogram(), bins=self.num_of_bins, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))       
        self.hist = self.histogram_container.gca()
        self.hist.hist(photo.histogram(), bins=self.num_of_bins, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))#(self.image_edited.histogram(), bins=256, range=(0, 256)
        self.hist.set_xlabel('Pixel Value', fontdict=dict(weight='bold',fontsize = 12))
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        self.histogram_canvas.draw()
      
    def otsu_threshold(self, photo):
        # Convert image to grayscale and get pixel values
        photo_gray = photo.convert("L")
        pixels = np.array(photo_gray.getdata()) #gray# 
        
        pixels = pixels.astype(np.uint8)

        if self.radio_selected.get() == "manual" and self.text_box_treshold.get("1.0", "end") != (f"\n"):

            self.threshold_value = int(self.text_box_treshold.get("1.0", "end"))
        else: 
            self.threshold_value = threshold_otsu(pixels)
            

        photo_binary = photo_gray.point(lambda x: 0 if x < self.threshold_value else 255)

        #set the otsu value in the valuebox
        self.text_box_treshold.config(state='normal')
        self.text_box_treshold.delete("1.0", "end")  # Clear the existing text
        self.text_box_treshold.insert("1.0", self.threshold_value ) # insert the threshold value in the text box
        

        # Update image display
        self.image_edited = photo_binary
        self.update_image(self.image_edited)
        self.draw_red_line_in_hist()

    def triangle_threshold(self, photo):

        # Convert image to grayscale and get pixel values
        photo_gray = photo.convert("L")
        pixels = np.array(photo_gray.getdata()) 
        pixels = pixels.astype(np.uint8)

        if self.radio_selected.get() == "manual" and self.text_box_treshold.get("1.0", "end") != (f"\n"):
            self.threshold_value = int(self.text_box_treshold.get("1.0", "end"))
        else: 
            self.threshold_value = threshold_triangle(pixels)

        photo_binary = photo_gray.point(lambda x: 0 if x < self.threshold_value else 255)

        #set the otsu value in the valuebox

        self.text_box_treshold.config(state='normal')
        self.text_box_treshold.delete("1.0", "end")  # Clear the existing text
        self.text_box_treshold.insert("1.0", self.threshold_value ) # insert the threshold value in the text box

        

        # Update image display
        self.image_edited = photo_binary
        self.update_image(self.image_edited)
        self.draw_red_line_in_hist()

    
    def draw_red_line_in_hist(self):
        rcParams['font.weight'] = 'bold' 
        #apply the red line in the histogram
          
        self.hist.axvline(self.threshold_value, color='r', ls='--')
        self.histogram_canvas.draw()


    def update_contrast(self,photo, value): 
        # Update image display
        new_width_edited =  self.edited_img_label.winfo_width()
        new_height_edited =  self.edited_img_label.winfo_height()
        
        photo = resize_image(photo, ((new_width_edited), (new_height_edited)))

        enhancer = ImageEnhance.Contrast(photo)
        photo_contrast = enhancer.enhance(float(value))
        self.image_edited = enhancer.enhance(float(value))      
        self.image_without_blur = self.image_edited

        self.update_image(photo_contrast)

        plt.clf()
        plt.hist(photo_contrast.histogram(), bins=self.num_of_bins, range=(0, 256))

        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(photo_contrast.histogram(), bins=self.num_of_bins, weights=np.ones(len(photo_contrast.histogram()))/len(photo_contrast.histogram()), range=(0, 256))        
        self.hist = self.histogram_container.gca()
        self.hist.hist(photo_contrast.histogram(), bins=self.num_of_bins,weights=np.ones(len(photo_contrast.histogram()))/len(photo_contrast.histogram()), range=(0, 256))#(photo.histogram(), bins=256, range=(0, 256))
        self.hist.set_xlabel('Pixel Value', fontsize = 12)
        self.hist.set_title('Pixel Histogram', fontsize = 12)
            
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        self.histogram_canvas.draw()
   
    def update_image(self, photo): #receber a photo_image_edited    

        # Clear any existing canvas and create a new one
        if hasattr(photo, "edited_canvas"):
            self.edited_canvas.destroy()  # Destroy the previous canvas

        #new_width_edited =  self.edited_img_label.winfo_width() 
        #new_height_edited =  self.edited_img_label.winfo_height()
        
        new_width_edited = self.original_edited_width
        new_height_edited = self.original_edited_height

        # Calculate the coordinates to center the image in the canvas
        x_center_edited = (new_width_edited - self.image_edited_tk.width()) / 2
        y_center_edited = (new_height_edited - self.image_edited_tk.height()) / 2


        self.image_edited = photo
        self.image_edited_tk = ImageTk.PhotoImage(photo)

        # Create a canvas widget to display the edited image
        self.edited_canvas = tk.Canvas(self.edited_img_label)
        self.edited_canvas.config(borderwidth=0)
        self.edited_canvas.pack()  # Place canvas inside the label
        self.edited_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
        self.edited_canvas.create_image(x_center_edited, y_center_edited, anchor=tk.NW, image=self.image_edited_tk )
  
    def upload_image(self):
        # Open a file dialog and get the path of the selected file
        filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=filetypes)
        
        if file_path:
            #reset all the variables
            self.contrast_value = 1.0
            self.threshold_value = None
            self.histogram_data = None  

            # Create a PhotoImage object from the selected file
            self.file_path = file_path
            self.image_original = Image.open(self.file_path)
            self.original_size = self.image_original.size

            
            # Resize the image to fit the canvas while maintaining aspect ratio
            new_width = self.original_img_label.winfo_width()  
            new_height = self.original_img_label.winfo_height() 
        
            new_width_edited =  self.edited_img_label.winfo_width() 
            new_height_edited =  self.edited_img_label.winfo_height()

            self.original_edited_width = new_width_edited
            self.original_edited_height = new_height_edited


            self.image_original = resize_image(self.image_original, ((new_width), (new_height)))
            self.image_edited = resize_image(self.image_original, ((new_width_edited), (new_height_edited)))
            
            self.image_original_tk = self.image_original.copy()
            self.image_edited_tk = self.image_edited.copy()
            
            # Resize image to fit canvas and convert to PhotoImage
            self.image_original_tk = ImageTk.PhotoImage(self.image_original)
            self.image_edited_tk = ImageTk.PhotoImage(self.image_edited)
            
            # Clear any existing canvas and create a new one
            if hasattr(self, "original_canvas"):
                self.original_canvas.destroy()
                self.edited_canvas.destroy()  # Destroy the previous canvas
            
            # Calculate the coordinates to center the image in the canvas
            x_center = (new_width - self.image_original_tk.width()) / 2
            y_center = (new_height - self.image_original_tk.height()) / 2


            x_center_edited = (new_width_edited - self.image_edited_tk.width()) / 2
            y_center_edited = (new_height_edited - self.image_edited_tk.height()) / 2

            # Create a canvas widget to display the image
            self.original_canvas = tk.Canvas(self.original_img_label)
            self.original_canvas.config(borderwidth=0)
            self.original_canvas.pack()
            self.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
            self.original_canvas.create_image(x_center, y_center, anchor=tk.NW, image=self.image_original_tk)
            
            # Create a canvas widget to display the edited image
            self.edited_canvas = tk.Canvas(self.edited_img_label)
            self.edited_canvas.config(borderwidth=0)
            self.edited_canvas.pack()  # Place canvas inside the label
            self.edited_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
            self.edited_canvas.create_image(x_center_edited, y_center_edited, anchor=tk.NW, image=self.image_edited_tk)
            self.show_histogram(self.image_edited)
            self.bar_contrast.set(1.0)

    def reset_project(self):
        #reseting the edited image for the original
        self.image_edited = self.image_original
        self.image_edited = resize_image(self.image_original, ((self.original_edited_width),(self.original_edited_height)))
        self.update_image(self.image_edited)

        #reset contrast
        self.bar_contrast.set(1.0)
        self.contrast_value = 0
        #self.update_contrast(self.image_edited, self.contrast_value)
        

        #reset Blur
        self.blur_value_textbox.delete("1.0","2.0")
        self.blur_value = 0

        #reset MODEL
        #self.show_histogram(self.image_edited)
        self.text_box_treshold.delete("1.0", "end")
        self.radio_selected.set('automatic')
        self.text_box_treshold.config(state='disable')

        #reset histogram
        self.show_histogram(self.image_edited)

    def save_files(self):


        if (self.img_save_value.get()==1) or (self.history_save_value.get()==1) or (self.histogram_save_value.get()==1):

            #user insert the name than will be used in the folder
            name_folder =  simpledialog.askstring(title="Save files", prompt="Insert the name of the folder.")

            if not name_folder:
                name_folder = "Binary_project" #  VER SE ESSE NOME FAZ SENTIDO PARA TODOS OS ARQUIVOS
            
            if (self.img_save_value.get()==1) and (self.history_save_value.get()==1) and (self.histogram_save_value.get()==1):
                self.save_image_edited(name_folder)
                self.save_history(name_folder)
                self.save_histogram(name_folder)

            elif (self.img_save_value.get()==1) and (self.history_save_value.get()==1):
                self.save_image_edited(name_folder)
                self.save_history(name_folder)

            elif (self.img_save_value.get()==1) and (self.histogram_save_value.get()==1):
                self.save_image_edited(name_folder)
                self.save_histogram(name_folder)

            elif (self.history_save_value.get()==1) and (self.histogram_save_value.get()==1):
                self.save_history(name_folder)
                self.save_histogram(name_folder)

            elif (self.img_save_value.get()==1):
                self.save_image_edited(name_folder)

            elif (self.history_save_value.get()==1):
                self.save_history(name_folder) 

            elif (self.histogram_save_value.get()==1):
                self.save_histogram(name_folder)

            else:
                return

    #save edited Image
    def save_image_edited(self, folder_name):

        #makes the image binary image back to PIL format
        self.binary_photo_for_save_tk = self.image_edited
        
        self.binary_photo_for_save_tk = self.binary_photo_for_save_tk.resize(self.original_size)

        self.image_original = self.image_original.resize(self.original_size)

        # Define the folder where you want to save the image
        save_folder =f"./projects/{folder_name}" #folder_name
        
        # Ensure the folder exists; create it if it doesn't

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
            
        # Save the image with a new name in the folder
        output_path = os.path.join(save_folder, 'image_edited')
        self.binary_photo_for_save_tk.save(output_path, 'PNG')
        output_path_original = os.path.join(save_folder, 'orinal_image')
        self.image_original.save(output_path_original, 'PNG')
       
    #save histogram
    def save_histogram(self, folder_name):
        
        # Define the folder where you want to save the image
        save_folder =f"./projects/{folder_name}" #folder_name
        
        # Ensure the folder exists; create it if it doesn't

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
            
        output_path = os.path.join(save_folder, 'histogram')
        self.hist.figure.savefig(output_path)

    #save history
    def save_history(self, folder_name):      
        # Define the folder where you want to save the image

        save_folder =f"./projects/{folder_name}" #folder_name
        
        # Ensure the folder exists; create it if it doesn't

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Create string with processing history data
        history_data = f"Image file path: {self.file_path}\nContrast value: {self.contrast_value}\n"

        if self.threshold_value is not None:
            history_data += f"Otsu threshold value: {self.threshold_value}\n"

        if self.blur_value is not None:
            history_data += f"Blur value: {self.blur_value}\n"

        if self.histogram_data is not None:
            history_data += "Histogram data:\n"
            for i, value in enumerate(self.histogram_data):
                history_data += f"{i}: {value}\n"

        # Write string to text file
        filepath = os.path.join(save_folder, 'contrast history')
        with open(filepath, "w") as f:
            f.write(history_data)

            

if __name__ == '__main__':
    app = FullScreenApp()
    app.mainloop()