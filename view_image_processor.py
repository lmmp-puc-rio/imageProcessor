import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter.filedialog import askopenfilename #TIRAR 
import tkinter.font as TkFont
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matplotlib.ticker as mtick
from PIL import Image, ImageTk, ImageEnhance
from skimage.filters import threshold_otsu,threshold_triangle
from utils.resize_image import resize_image, resize_image_predifined
from utils.nav_utils import *
from utils.name_folder import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from utils.CustomImage import CustomImage


class FullScreenApp(tk.Tk):

    def __init__(self):
        super().__init__()
        
        #####################
        ##   Basic config  ##
        #####################

        #app in fullscreen
        self.attributes("-fullscreen", True)
        self.overrideredirect(False)

        #colors in app
        self.pry_color = "#5376D6"
        self.sec_color = "#CFCECE"
        self.btn_color = "#6484DA"
        self.bg_container_color = "#DEDDDD"

       
        #font sizes
        self.fz_alerts = 7
        self.fz_mn = 10
        self.fz_md = 12
        self.fz_lg = 14
        self.fz_xl = 22
        
        #fonts config

        self.font_name = "LKLUG"
        self.font_alerts = TkFont.Font(font=(self.font_name, self.fz_mn))
        self.font_mn = TkFont.Font(font=(self.font_name, self.fz_mn))
        self.font_md = TkFont.Font(font=(self.font_name, self.fz_md))
        self.font_lg = TkFont.Font(font=(self.font_name, self.fz_lg))
        self.font_xl = TkFont.Font(font=(self.font_name, self.fz_xl))

        self.font_md_bold = TkFont.Font(font=(self.font_name, self.fz_md, "bold"))
        self.font_lg_bold = TkFont.Font(font=(self.font_name, self.fz_lg, "bold"))

        # Set the app title in the title bar
        self.title('Image Processor')

        #root config
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=9)
        self.rowconfigure(2, weight=1)

        #App title
        self.title("Image Processor")

        #Global variables
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
        ## top frame ##
        ###############

        #grid config
        self.header_frame = tk.Frame(self, background = self.pry_color)
        self.header_frame.columnconfigure(0, weight=0)
        self.header_frame.columnconfigure(1, weight=8)
        self.header_frame.columnconfigure(2, weight=1)

        #home button
        self.img_home= (Image.open(r'src/images/logo_grey.png'))
        self.btn_home_img = resize_image(self.img_home,(240,100))
        self.btn_home_model = ImageTk.PhotoImage(self.btn_home_img)
        self.home_btn = tk.Button(self.header_frame, image= self.btn_home_model, background= self.pry_color, borderwidth=0, highlightthickness = 0 , activebackground= self.btn_color,relief='sunken', command=home_page)
        self.home_btn.bind("<Button-1>", lambda x: self.webbrowser.open_new("http://tmp-lmmp.mec.puc-rio.br/"))      
        
        #upload button
        self.img_upload= (Image.open(r'src/images/upld_btn.png'))
        self.btn_img_upload_img = resize_image(self.img_upload,(200,100))
        self.btn_img_upload_model = ImageTk.PhotoImage(self.btn_img_upload_img)
        #This Button calls the Class CustomImage
        self.upload_btn = tk.Button(self.header_frame, image=self.btn_img_upload_model,bg= self.pry_color, borderwidth=0,highlightthickness = 0, activebackground=self.pry_color, command=self.create_object_image)

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

        #Placing widget in main framePlacing widget in top widget
        self.header_frame.grid(row=0, column=0, sticky='WENS')
        self.home_btn.grid(row= 0 , column= 0, sticky ='W', ipady=5, ipadx=7)
        self.upload_btn.grid(row= 0 , column= 1, padx=(0,255), sticky ='E', pady=2)
        self.help_btn.grid(row= 0 , column= 1, padx=(0,50), sticky ='E', pady=2)
        self.minimize_btn.grid(row= 0 , column= 2, sticky ='E', padx=(0,45), pady=2)
        self.close_btn.grid(row= 0 , column= 2, sticky ='E', padx=(2,5), pady=2)

        ###############
        ##    main   ##
        ###############

        #Grid config
        self.main_frame = tk.Frame(self, background= self.bg_container_color)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=0)

        #main titles texts
        self.original_txt = tk.Label(self.main_frame, text='ORIGINAL IMAGE',font= (self.font_lg_bold), background= self.bg_container_color )
        self.edited_txt = tk.Label(self.main_frame, text='EDITED IMAGE', font= (self.font_lg_bold), background= self.bg_container_color )
        self.histogram_txt = tk.Label(self.main_frame, text='PIXEL HISTOGRAM', font= (self.font_lg_bold), background= self.bg_container_color )

        #main Canvas
        self.original_img_label= tk.Label(self.main_frame, background = self.sec_color)
        self.edited_img_label = tk.Label(self.main_frame, background = self.sec_color)
        self.histogram_img_label = tk.Label(self.main_frame, background = self.sec_color)
        self.histogram_inner_frame = tk.Frame(self.histogram_img_label)

        #Canvas grid config
        self.histogram_img_label.rowconfigure(0, weight=1)
        self.histogram_img_label.rowconfigure(1, weight=1)
        self.histogram_img_label.rowconfigure(2, weight=1)

        self.histogram_inner_frame.grid(row=1, column=0)

        #histogram
        self.histogram_container = plt.Figure()
        self.histogram_container.patch.set_facecolor(self.sec_color)
        self.histogram_canvas = FigureCanvasTkAgg(self.histogram_container, master=self.histogram_inner_frame)
        self.histogram_canvas.get_tk_widget().pack( fill='both')
    
        #Placing widget in main frame
        self.main_frame.grid(row=1, column=0, sticky='WENS')
        self.original_txt.grid(row=0, column=0, sticky='N', pady=(6,2))
        self.edited_txt.grid(row=0, column=1, sticky='N', pady=(6,2))
        self.histogram_txt.grid(row=0, column=2, sticky='N', pady=(6,2))
        self.original_img_label.grid(row=1, column=0, sticky='WENS',padx=1.5, pady=3)
        self.edited_img_label.grid(row=1, column=1, sticky='WENS',padx=1.5, pady=3)
        self.histogram_img_label.grid(row=1, column=2, sticky='WENS',padx=1.5,pady=3)

        ##################
        ## footer frame ##
        ##################

        #Grid config
        self.footer_frame = tk.Frame(self, background=self.pry_color, height=50)
        self.footer_frame.grid(row=2, column=0, sticky='WENS')
        self.footer_frame.rowconfigure(0, weight=1)
        self.footer_frame.columnconfigure(0, weight=0)
        self.footer_frame.columnconfigure(1, weight=0)
        self.footer_frame.columnconfigure(2, weight=1)

        #footer widgets
        self.contrast_frame = tk.Frame(self.footer_frame, background=self.pry_color)
        self.treshold_frame = tk.Frame(self.footer_frame, background=self.pry_color)
        self.save_frame = tk.Frame(self.footer_frame, background=self.pry_color, bg=self.pry_color)

        #placing footer widgets   
        self.contrast_frame.grid(row=0, column=0,sticky='WENS', ipadx=3,padx=2, pady=3)
        self.treshold_frame.grid(row=0, column=1,sticky='WENS', ipadx=3,padx=2, pady=3)
        self.save_frame.grid(row=0, column=2,sticky='WENS', ipadx=3,padx=2, pady=3)

        ##############################
        ##Contrast Frame Gird Config##
        ##############################

        self.contrast_frame.columnconfigure(0, weight=0)
        self.contrast_frame.columnconfigure(1, weight=0)
        self.contrast_frame.rowconfigure(0, weight=1)
        self.contrast_frame.rowconfigure(1, weight=1)
        self.contrast_frame.rowconfigure(2, weight=1)
        self.contrast_frame.rowconfigure(3, weight=1)
        self.contrast_frame.rowconfigure(4, weight=1)

        #Scale Bar Widgets
        self.value_scale = tk.StringVar()
        self.text_contrast = tk.Label(self.contrast_frame, text='CONTRAST',font= (self.font_md_bold),anchor=tk.N, background= self.pry_color)
        self.bar_contrast = tk.Scale(self.contrast_frame, from_=0.1, to=5.0,orient='horizontal',font = (self.font_mn),tickinterval= 0.5, resolution=0.1, label="Value",
                                troughcolor = self.sec_color, variable = self.value_scale ,bg= self.pry_color, border=None ,highlightthickness = 0, activebackground=self.pry_color, command = self.update_scale)
        self.text_contrast.grid(row=0, column=0,columnspan=2, sticky='NS', padx=3, pady=(5,10))
        self.bar_contrast.grid(row=1, column=0,columnspan=2, sticky='EW', padx=25, pady=5, ipadx=5, ipady=5)

        #blur filter WIdgets
        self.radio_blur_selected = tk.StringVar(value='deactivated')
        self.blur_text = tk.Label(self.contrast_frame, text = 'BLUR', font = (self.font_md_bold), anchor=tk.N, background=self.pry_color)
        self.blur_text.grid(row=2, column=0, columnspan=3, sticky='N')

        #blur configs
        self.blur_label1 = tk.Label(self.contrast_frame,  background= self.pry_color)
        self.blur_label1.grid(row=3, column=0, sticky='w')
        self.blur_label1.columnconfigure(0,weight=0)
        self.blur_label1.columnconfigure(1,weight=0)
        self.radio1_btn_blur =tk.Radiobutton(self.blur_label1, text='Activated', variable = self.radio_blur_selected, value= "activated",  anchor=tk.W, bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font_mn))
        self.radio2_btn_blur =tk.Radiobutton(self.blur_label1, text='Deactivated', variable = self.radio_blur_selected, value= "deactivated",  anchor=tk.E, bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font_mn))
        self.radio1_btn_blur.grid(row= 0, column= 0, padx=(20,10)) 
        self.radio2_btn_blur.grid(row= 0, column= 1, padx=(10,20))

        self.blur_label2 = tk.Label(self.contrast_frame,  background= self.pry_color)
        self.blur_label2.columnconfigure(0,weight=0)
        self.blur_label2.columnconfigure(0,weight=1)
        self.blur_label2.columnconfigure(0,weight=2)

        self.blur_label2.grid(row=3, column=1, sticky='W')

        self.blur_value_label = tk.Label(self.blur_label2,  text='Blur Value: ', bg= self.pry_color,font= (self.font_mn))
        self.blur_value_textbox = tk.Text(self.blur_label2,  width=3, height=1, font=(self.font_mn))
        self.blur_text_box_alert = tk.Label(self.blur_label2, anchor=tk.S,  text='* only use values between 1 and 9.',font=(self.font_alerts), bg= self.pry_color)
        
        # create a label for hide the alert in the screen
        self.blur_text_box_alert_hidden = tk.Label(self.blur_label2, bg= self.pry_color)
        
        #image blur btn
        self.blur_btn_img= (Image.open(r'src/images/blur_btn.png'))
        self.btn_blur_btn_img = resize_image(self.blur_btn_img,(120,30))
        self.btn_blur_btn = ImageTk.PhotoImage(self.btn_blur_btn_img)
        self.btn_run_blur = tk.Button(self.contrast_frame, image=self.btn_blur_btn,bg= self.pry_color, borderwidth=0,highlightthickness = 0, activebackground=self.pry_color, command = self.apply_blur,state = "disable")

        self.blur_value_label.grid(row= 0, column=0, padx=6)
        self.blur_value_textbox.grid(row= 0, column=1, padx=6)
        self.blur_text_box_alert.grid(row= 0, column=2, padx=6)
        self.blur_text_box_alert_hidden.grid(row= 0, column=2,sticky='WENS', padx=6)
        self.blur_value_textbox.config(state='disabled')
        self.blur_value_textbox.bind("<Key>", self.validate_blur_value)

        self.btn_run_blur.grid(row=4, column=0, columnspan=2, sticky="N", pady=5)

        # monitors each change in the blur radio button to activate or deactivate the blur text box
        self.radio_blur_selected.trace("w", lambda *args: self.verify_blur())


        ##############################
        ##      treshold Frame      ##
        ##############################

        #Grid Config
        self.treshold_frame.columnconfigure(0, weight=3)
        self.treshold_frame.columnconfigure(1, weight=3)
        self.treshold_frame.rowconfigure(0, weight=1)
        self.treshold_frame.rowconfigure(1, weight=1)
        self.treshold_frame.rowconfigure(2, weight=1)
        self.treshold_frame.rowconfigure(3, weight=1)
        self.treshold_frame.rowconfigure(4, weight=1)

        
        #model Combobox
        self.list_treshold_model = ['OTSU', 'TRIANGLE']
        self.clicked_model = tk.StringVar()
        self.clicked_model.set(self.list_treshold_model[0])
        self.combobox_models = ttk.Combobox(self.treshold_frame, values=self.list_treshold_model, font= (self.font_mn), state="readonly", takefocus=None)
        self.combobox_models.current(0)
        
        #Radio buttons Treshhold
        self.radio_selected = 0
        self.radio_selected = tk.StringVar(value="automatic")
        self.radio1_btn_treshold =tk.Radiobutton(self.treshold_frame,text='Automatic', variable = self.radio_selected, value= "automatic", bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font_md))
        self.radio2_btn_treshold =tk.Radiobutton(self.treshold_frame,text='Manual', variable = self.radio_selected, value= "manual", bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font_md))
        
        
        #Model Value and alert msg
        self.value_model_label = tk.Label(self.treshold_frame, bg=self.pry_color)

        self.value_model_label.columnconfigure(0, weight=1)
        self.value_model_label.columnconfigure(1, weight=1)
        self.value_model_label.columnconfigure(2, weight=1)

        self.value_treshold = tk.Label(self.value_model_label, text= 'Value: ', bg= self.pry_color,highlightthickness = 0, font = (self.font_mn))
        self.text_box_treshold = tk.Text(self.value_model_label, width=4, height=1, font=(self.font_mn))
        self.text_box_alert = tk.Label(self.value_model_label, text='* only use values between 0 and 255.',font=(self.font_alerts), bg= self.pry_color)

        # create a label for hide the alert in the screen
        self.text_box_alert_hidden = tk.Label(self.value_model_label, bg= self.pry_color)

        # monitors each change in the model radio button to activate or deactivate the value model text box
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

        self.text_treshold = tk.Label(self.treshold_frame, text='TRESHOLD',font= (self.font_md_bold), background= self.pry_color)
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

        #########################
        ##      Save Frame     ##
        #########################

        #Grid Config
        self.save_frame.columnconfigure(0, weight=1)
        self.save_frame.columnconfigure(1, weight=0)
        self.save_frame.rowconfigure(0, weight=1)
        self.save_frame.rowconfigure(1, weight=1)
        self.save_frame.rowconfigure(2, weight=1)
        self.save_frame.rowconfigure(3, weight=1)
        self.save_frame.rowconfigure(4, weight=1)

        #Check Boxs for saves
        self.img_save_value = tk.IntVar()
        self.history_save_value = tk.IntVar()
        self.histogram_save_value = tk.IntVar()             

        self.checkbox1_frame = tk.Checkbutton(self.save_frame, text="SAVE IMAGE", variable = self.img_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font_md),highlightthickness = 0)
        self.checkbox2_frame = tk.Checkbutton(self.save_frame, text="SAVE HISTORY", variable = self.history_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font_md),highlightthickness = 0)
        self.checkbox3_frame = tk.Checkbutton(self.save_frame, text="SAVE HISTOGRAM", variable = self.histogram_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font_md),highlightthickness = 0)

        #Save button
        self.img= (Image.open(r'src/images/save_btn.png'))
        self.img = resize_image(self.img,(200,100))
        self.img_save = ImageTk.PhotoImage(self.img)
        self.img_save_label = tk.Label(image=self.img_save, background= self.pry_color)
        self.save_btn = tk.Button(self.save_frame, image=self.img_save,bg= self.pry_color, borderwidth=0,highlightthickness = 0,
                                  activebackground=self.pry_color, command= self.save_files, anchor='e')

        self.checkbox1_frame.grid(row=1, column=0, sticky='w', padx=(90,0), pady=3)
        self.checkbox2_frame.grid(row=2, column=0, sticky='w', padx=(90,0), pady=3)
        self.checkbox3_frame.grid(row=3, column=0, sticky='w', padx=(90,0), pady=3)
        self.save_btn.grid(row=2, column=1, sticky='e', padx=(2,20), pady=3)
    
    def quit_application(self):
        """!
        @brief ends the application
        
        @param self app
        
        @note Closes the app with the tk.destroy()
        
        @return None
        """
        close_app(self)
    
    def minimize_application(self):
        """!
        @brief minimize the application
        
        @param self app
        
        @note minimize the app and quit the fullscreen with the app.iconify()
        
        @return None
        """
        minimize_app(self)   
    
    #Show the scale value in real time
    def update_scale(self, *args):
        """!
        @brief take the atual value of the contrast bar.
        
        @param self.value_scale(str)
        
        @note Take the value of the contrast bar e pass to the update_contrast function for update the edited image with the contrast value
        
        @return self.update_contrast(self,photo, value)
        """
        self.contrast_value = self.value_scale.get()
        # 
        if type(self.image_original) is not type(None):
            self.image_original.update_contrast(self.contrast_value)
            
    #validate user input in blur value
    def validate_blur_value(self, event):
        """!
        @brief show an alert msg on blur value
        
        @param key pressed on self.blur_value_textbox(str)
        
        @note shows a warning message when the user enters a value that is not accepted,
         just removes the label above the message.
        
        @return None
        """
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
            self.blur_text_box_alert_hidden.grid_remove()
            return "break"  
    
    #validate user input in treshold value
    def validate_model_value(self, event):
        """!
        @brief show an alert msg on model value
        
        @param key pressed on self.model_value_textbox(str)
        
        @note shows a warning message when the user enters a value that is not accepted,
         just removes the label above the message.
        
        @return None
        """
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
        """!
        @brief check the changes of the radio button
        
        @param self.radio_selected(radion button)
        
        @note checks whenever the radio button changes from auto to manual,
          changing the state of the Model TextBox
        
        @return None
        """
        if self.radio_selected.get() == "automatic":
            self.text_box_treshold.config(state='disabled')

        else:
            self.text_box_treshold.config(state='normal')
    
    #verifica sempre que o blur radio button muda para ativo
    def verify_blur(self):
        """!
        @brief Verify and configure blur settings based on the selected item.

        @param self.radio_blur_selected

        @note This function verifies the selected blur setting (activated or disabled) and configures
        the blur value textbox accordingly. If 'activated' is selected, the textbox is enabled
        to allow user input for the blur value. If 'disabled' is selected, the textbox is disabled.

        @return: None
        """
        selected_item = self.radio_blur_selected.get()
        self.blur_value = self.blur_value_textbox.get("1.0","2.0")

        if selected_item == "activated":
            self.blur_value_textbox.config(state='normal')
            self.btn_run_blur['state'] = "normal"
        else:
            self.blur_value_textbox.config(state='disabled')
            self.btn_run_blur['state'] = "disable"

    def apply_blur(self):
        if self.blur_value_textbox:
            #self.apply_blur()
            self.blur_value = int(self.blur_value_textbox.get("1.0","2.0"))
            self.image_original.apply_blur(self.blur_value)
        else:
            pass

    def on_treshold_btn_click(self):
        """!
        @brief Apply Gaussian blur to the image.

        @param The function uses attributes: `self.image_without_blur`, `self.blur_value_textbox`,
        `self.blur_value`, `self.num_of_bins`, `self.image_edited`, `self.histogram_canvas`.

        @note This function applies Gaussian blur to the edited image using the specified blur value.
        It also updates the edited image, displays the updated image, and generates the new pixel histogram for the updated edited image.

        @return: None
        """
        selected_item = self.combobox_models.get()
        self.text_box_alert_hidden.grid()
        self.blur_text_box_alert_hidden.grid()

        if selected_item == self.list_treshold_model[0]:
            if self.radio_selected.get() == "manual" and self.text_box_treshold.get("1.0", "end") != (f"\n"):
                manual_threshold_value = int(self.text_box_treshold.get("1.0", "end"))
                self.image_original.apply_model_otsu_treashold(manual_threshold_value)
            else: 
                self.image_original.apply_model_otsu_treashold()
                model_value = self.image_original.get_model_value()
                self.insert_model_value_in_box(model_value)

        elif selected_item == self.list_treshold_model[1]:
            if self.radio_selected.get() == "manual" and self.text_box_treshold.get("1.0", "end") != (f"\n"):
                manual_threshold_value = int(self.text_box_treshold.get("1.0", "end"))
                self.image_original.apply_model_triangle_treashold(manual_threshold_value)
            else: 
                self.image_original.apply_model_triangle_treashold()
                model_value = self.image_original.get_model_value()
                self.insert_model_value_in_box(model_value)

    def update_image_edited(self, value):
        self.image_original.update_image(value)

    def insert_model_value_in_box(self, value):
        self.text_box_treshold.config(state='normal')
        self.text_box_treshold.delete("1.0", "end")  # Clear the existing text
        self.text_box_treshold.insert("1.0", value)

    def create_object_image(self):
        self.bar_contrast.set(1.0)
        self.image_original = CustomImage(app = self, label_original = self.original_img_label,  label_edited =self.edited_img_label, label_histogram = self.histogram_container, canvas_histogram = self.histogram_canvas)
        
    def reset_project(self):
        """!
        @brief Resets all variables , photos and histogram

        @param 'self.image_original'(PIL image), 'self.image_edited'(PIL image), 'self.contrast_value'(float), 'self.contrast_value(int)', 'self.blur_value(int)'

        @note This function updates the edited image, the original image, the histogram and updates all variables relating to photo editing and the histogram

        @return: None
        """

        #hidden alert msg
        self.text_box_alert_hidden.grid()
        self.blur_text_box_alert_hidden.grid()
        
        #reset contrast
        self.bar_contrast.set(1.0)      

        #reset Blur
        self.blur_value_textbox.delete("1.0","2.0")

        #reset MODEL
        self.text_box_treshold.delete("1.0", "end")
        self.radio_selected.set('automatic')
        self.text_box_treshold.config(state='disable')        

        #reset the image and the values
        self.image_original.reset_project()

    def save_files(self):
        """!
        @brief call one or all chosen save option

        @param 'self.img_save_value, 'self.history_save_value', 'self.histogram_save_value'

        @note this function calls each function related to a type of recording. Just the photos, the histogram or the history or all of them together

        @return: None
        """

        if (self.img_save_value.get()==1) or (self.history_save_value.get()==1) or (self.histogram_save_value.get()==1):

            #user insert the name than will be used in the folder
            name_folder =  simpledialog.askstring(title="Save files", prompt="Insert the name of the folder.")
            #Calls the function to generate a not duplicated folder
            name_folder = create_unique_folder_name(name_folder)

            # Define the folder where you want to save the image
            save_folder =f"./projects/{name_folder}" #folder_name
            
            #Ensure the folder exists; create it if it doesn't
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            if not name_folder:
                name_folder = "Binary_project"
            
            if (self.img_save_value.get()==1) and (self.history_save_value.get()==1) and (self.histogram_save_value.get()==1):
                self.image_original.save_image_edited(save_folder)
                self.image_original.save_history(save_folder)
                self.image_original.save_histogram(save_folder)

            elif (self.img_save_value.get()==1) and (self.history_save_value.get()==1):
                self.image_original.save_image_edited(save_folder)
                self.image_original.save_history(save_folder)

            elif (self.img_save_value.get()==1) and (self.histogram_save_value.get()==1):
                self.image_original.save_image_edited(save_folder)
                self.image_original.save_histogram(save_folder)

            elif (self.history_save_value.get()==1) and (self.histogram_save_value.get()==1):
                self.image_original.save_history(save_folder)
                self.image_original.save_histogram(save_folder)

            elif (self.img_save_value.get()==1):
                self.image_original.save_image_edited(save_folder)

            elif (self.history_save_value.get()==1):
                self.image_original.save_history(save_folder) 

            elif (self.histogram_save_value.get()==1):
                self.image_original.save_histogram(save_folder)

            else:
                return


if __name__ == '__main__':
    app = FullScreenApp()
    app.mainloop()