import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matplotlib.ticker as mtick
from PIL import Image, ImageTk, ImageEnhance
from skimage.filters import threshold_otsu
from utils.resize_image import resize_image, resize_image_predifined
from utils.nav_utils import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.threshold_value = None

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
        self.edited_img_label = tk.Label(self.main_frame, background = self.sec_color) #, width= self.original_img_label.winfo_width(), height= self.original_img_label.winfo_height())
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
        # self.histogram_canvas.get_tk_widget().pack(side=tk.RIGHT)#, anchor='s')
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
        self.footer_frame.columnconfigure(0, weight=5)
        self.footer_frame.columnconfigure(1, weight=2)
        self.footer_frame.columnconfigure(2, weight=1)

        self.contrast_frame = tk.Frame(self.footer_frame, background=self.pry_color)
        self.treshold_frame = tk.Frame(self.footer_frame, background=self.pry_color)
        self.save_frame = tk.Frame(self.footer_frame, background=self.pry_color)


        #footer Wdiget
        self.footer_frame.grid(row=2, column=0, sticky='WENS')
        self.contrast_frame.grid(row=0, column=0,sticky='WENS', ipadx=3,padx=2, pady=3)
        self.treshold_frame.grid(row=0, column=1,sticky='WENS', ipadx=3,padx=2, pady=3)
        self.save_frame.grid(row=0, column=2, ipadx=3,sticky='WENS',padx=2, pady=3)


        #Contrast Frame
        self.contrast_frame.columnconfigure(0, weight=1)
        self.contrast_frame.rowconfigure(0, weight=1)
        self.contrast_frame.rowconfigure(1, weight=1)


        #scale bar

        self.value_scale = tk.StringVar()
        self.text_contrast = tk.Label(self.contrast_frame, text='CONTRAST',font= (self.font, self.fz_lg, 'bold'),anchor=tk.N, background= self.pry_color)
        self.bar_contrast = tk.Scale(self.contrast_frame, from_=0.1, to=5.0,orient='horizontal',font = (self.font, self.fz_mn),tickinterval= 0.5, resolution=0.1, label="Value",
                                troughcolor = self.sec_color, variable = self.value_scale ,bg= self.pry_color, border=None ,highlightthickness = 0, activebackground=self.pry_color, command = self.update_scale)

        self.text_contrast.grid(row=0, column=0,sticky='NS', padx=3, pady=(5,10))
        self.bar_contrast.grid(row=1, column=0,sticky='EW', padx=25, pady=5, ipadx=5, ipady=5)

        #treshold Frame
        self.radio_selected = 0

        self.treshold_frame.columnconfigure(0, weight=3)
        self.treshold_frame.columnconfigure(1, weight=3)

        self.treshold_frame.rowconfigure(0, weight=1)
        self.treshold_frame.rowconfigure(1, weight=1)
        self.treshold_frame.rowconfigure(2, weight=1)
        self.treshold_frame.rowconfigure(3, weight=1)
        self.treshold_frame.rowconfigure(4, weight=1)
        
        #----- combobox
        self.list_treshold_model = ['OTSU', 'XXXX']
        self.clicked_model = tk.StringVar()
        self.clicked_model.set(self.list_treshold_model[0])
        #dropdow_treshold = tk.OptionMenu(treshold_frame,clicked_model, *list_treshold_model)
        self.combobox_models = ttk.Combobox(self.treshold_frame, values=self.list_treshold_model, font= (self.font, self.fz_md), state="readonly")
        self.combobox_models.current(0)
        #self.combobox_models.bind("<<ComboboxSelected>>", self.on_combobox_select)
        #print(self.combobox_models.get())
        
        #----- radioBtn Treshhold
        self.radio_selected = tk.StringVar(value="automatic")
        self.radio1_btn_treshold =tk.Radiobutton(self.treshold_frame,text='Automatic', variable = self.radio_selected, value= "automatic", bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font, self.fz_md))
        self.radio2_btn_treshold =tk.Radiobutton(self.treshold_frame,text='Manual', variable = self.radio_selected, value= "manual", bg= self.pry_color,highlightthickness = 0, activebackground= self.pry_color, font= (self.font, self.fz_md))
        self.value_treshold = tk.Label(self.treshold_frame, text= 'VALUE: ', bg= self.pry_color,highlightthickness = 0, font= (self.font, self.fz_mn))
        self.text_box_treshold = tk.Text(self.treshold_frame, width=4, height=1, font=(self.font, self.fz_md), highlightthickness = 0)
        
        # monitora cada mudança na variavel para chamar a função automaticamente
        self.radio_selected.trace("w", lambda *args: self.on_radio_select())

        #btn Run Model
        self.run_model_img= (Image.open(r'src/images/run_btn.png'))
        self.btn_run_model_img = resize_image(self.run_model_img,(200,100))
        self.btn_run_model = ImageTk.PhotoImage(self.btn_run_model_img)
        self.treshold_label = tk.Label(image=self.btn_run_model, background= self.pry_color)
        self.treshold_btn = tk.Button(self.treshold_frame, image=self.btn_run_model,bg= self.pry_color, borderwidth=0, activebackground=self.pry_color,highlightthickness = 0, command= self.on_treshold_btn_click)
        

        #treshold Widget 

        self.text_treshold = tk.Label(self.treshold_frame, text='TRESHOLD',font= (self.font, self.fz_lg, 'bold'), background= self.pry_color)
        self.text_treshold.grid(row=0, column=0,columnspan=2,sticky='N', padx=3, pady=5)
        self.combobox_models.grid(row=1, column=0,sticky='N', padx=5, pady=5)
        self.radio1_btn_treshold.grid(row=2, column=0,sticky='N', padx=5, pady=2)
        self.radio1_btn_treshold.config(command=self.on_radio_select)

        self.radio2_btn_treshold.grid(row=3, column=0,sticky='N', padx=5, pady=2)

        self.value_treshold.grid(row=4, column=0,sticky='N', padx=5, pady=5)
        self.treshold_btn.grid(row=2, column=1,rowspan=3,sticky='N', padx=3, pady=5)
        self.text_box_treshold.grid(row=4, column=0,sticky='N', padx=(140,0), pady=2)

        #Save Frame

        self.save_frame.columnconfigure(0, weight=7)
        self.save_frame.columnconfigure(1, weight=3)
        self.save_frame.rowconfigure(0, weight=1)
        self.save_frame.rowconfigure(1, weight=1)
        self.save_frame.rowconfigure(2, weight=1)
        self.save_frame.rowconfigure(3, weight=1)
        self.save_frame.rowconfigure(4, weight=1)

        #checkbox widget

        text_checkbox = tk.Label(self.save_frame, text='SAVE PROJECT',font= (self.font, self.fz_lg, 'bold'), background= self.pry_color)

        #----- Check Box
        self.img_save_value = tk.IntVar()
        self.history_save_value = tk.IntVar()
        self.histogram_save_value = tk.IntVar()


        def display_saves(self):
            if(self.img_save_value.get()==1):
                print("Savar imagem")
            elif (self.history_save_value.get()==1):
                print("Savar historico")
            elif (self.histogram_save_value.get()==1):
                print("Savar historico")
            else:
                print("salvar nada.")
                

        self.checkbox1_frame = tk.Checkbutton(self.save_frame, text="SAVE IMAGE", variable = self.img_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font, self.fz_md),highlightthickness = 0, command= display_saves)
        self.checkbox2_frame = tk.Checkbutton(self.save_frame, text="SAVE HISTORY", variable = self.history_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font, self.fz_md),highlightthickness = 0, command= display_saves)
        self.checkbox3_frame = tk.Checkbutton(self.save_frame, text="SAVE HISTOGRAM", variable = self.histogram_save_value, onvalue=1, offvalue=0,
                                                 bg= self.pry_color, activebackground= self.pry_color, font= (self.font, self.fz_md),highlightthickness = 0, command= display_saves)

        #Load an image for the save btn
        self.img= (Image.open(r'src/images/save_btn.png'))
        self.img = resize_image(self.img,(200,100))
        self.img_save = ImageTk.PhotoImage(self.img)
        self.img_save_label = tk.Label(image=self.img_save, background= self.pry_color)
        self.save_btn = tk.Button(self.save_frame, image=self.img_save,bg= self.pry_color, borderwidth=0,highlightthickness = 0, activebackground=self.pry_color)

        #self.text_checkbox.grid(row=0, column=0,columnspan=2, sticky='N', padx=2, pady=3)
        self.checkbox1_frame.grid(row=1, column=0, sticky='w', padx=5, pady=3)
        self.checkbox2_frame.grid(row=2, column=0, sticky='w', padx=5, pady=3)
        self.checkbox3_frame.grid(row=3, column=0, sticky='w', padx=5, pady=3)
        self.save_btn.grid(row=2, column=1, sticky='N', padx=(2,2), pady=3)

        

    def quit_application(self):
            close_app(self)
    
    def minimize_application(self):
            minimize_app(self)
    
    #Show the scale value in real time
    def update_scale(self, *args):
        value = self.value_scale.get()
        print("Scale Value:", value)
        self.update_contrast(self.edited_image, value)
         
    # verifica sempre que o radio button muda de auto para manual, dessa forma mudando o estado do TextBox
    def on_radio_select(self):
        if self.radio_selected.get() == "automatic":
            self.text_box_treshold.delete("1.0", "end")
            self.text_box_treshold.insert("1.0", "000")
            self.text_box_treshold.config(state='disabled')
        else:
            self.text_box_treshold.config(state='normal')

    def on_treshold_btn_click(self):
        selected_item = self.combobox_models.get()
        if selected_item == "OTSU":
            #self.radio1_btn_treshold.select()
            #self.text_box_treshold.delete("1.0", "end")
            #""" rodar a edição da foto e passar o valor para o model_value """
            #model_value = int(98)
            #self.text_box_treshold.insert("1.0", model_value)
            print(self.edited_image)
            self.otsu_threshold(self.edited_image)
        elif selected_item == "XXXX":
            self.radio2_btn_treshold.select()
            self.text_box_treshold.delete("1.0", "end")
            """ rodar a edição da foto e passar o valor para o model_value """
            model_value = int(84)
            self.text_box_treshold.insert("1.0", model_value)

    def upload_image(self):
        # Open a file dialog and get the path of the selected file
        filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=filetypes)
        
        if file_path:
            # Create a PhotoImage object from the selected file
            self.file_path = file_path
            self.original_image = Image.open(self.file_path)
            self.original_size = self.original_image.size
            
            # Resize the image to fit the canvas while maintaining aspect ratio
            new_width = self.original_img_label.winfo_width()
            new_height = self.original_img_label.winfo_height()
        
            new_width_edited =  self.edited_img_label.winfo_width()
            new_height_edited =  self.edited_img_label.winfo_height()

            print(new_width, new_height, new_width_edited, new_height_edited) #PARA SABER SE TEM O MESMO TAMANHO
            self.original_image = resize_image(self.original_image, ((new_width), (new_height)))
            self.edited_image = resize_image(self.original_image, ((new_width_edited), (new_height_edited)))
            
            self.image = self.original_image.copy()
            self.image_edited = self.edited_image.copy()
            
            # Resize image to fit canvas and convert to PhotoImage
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.photo_image_edited = ImageTk.PhotoImage(self.image_edited)
            
            # Clear any existing canvas and create a new one
            if hasattr(self, "original_canvas"):
                self.original_canvas.destroy()
                self.edited_canvas.destroy()  # Destroy the previous canvas
            
            # Calculate the coordinates to center the image in the canvas
            x_center = (new_width - self.photo_image.width()) / 2
            y_center = (new_height - self.photo_image.height()) / 2

            x_center_edited = (new_width_edited - self.photo_image.width()) / 2
            y_center_edited = (new_height_edited - self.photo_image.height()) / 2
            
            # Create a canvas widget to display the image
            self.original_canvas = tk.Canvas(self.original_img_label)
            self.original_canvas.config(borderwidth=0)
            self.original_canvas.pack()
            self.original_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
            self.original_canvas.create_image(x_center, y_center, anchor=tk.NW, image=self.photo_image)
            
            # Create a canvas widget to display the edited image
            self.edited_canvas = tk.Canvas(self.edited_img_label)
            self.edited_canvas.config(borderwidth=0)
            self.edited_canvas.pack()  # Place canvas inside the label
            self.edited_canvas.place(relwidth=1.0, relheight=1.0)  # Place canvas inside the label
            self.edited_canvas.create_image(x_center_edited, y_center_edited, anchor=tk.NW, image=self.photo_image_edited)
            self.show_histogram(self.image_edited) #TIRAR DEPOIS. SOMENTE PRA TESTE
    
    def show_histogram(self, photo):
        bins_used = 50
        rcParams['font.weight'] = 'bold'       
        plt.clf()
        plt.hist(photo.histogram(), weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))
        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(photo.histogram(), bins=bins_used, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))       
        self.hist = self.histogram_container.gca()
        self.hist.hist(photo.histogram(), bins=bins_used, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))#(self.photo_image_edited.histogram(), bins=256, range=(0, 256)
        self.hist.set_xlabel('Pixel Value', fontdict=dict(weight='bold',fontsize = 12))
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        self.histogram_canvas.draw()
      
    def otsu_threshold(self, photo):
        # Convert image to grayscale and get pixel values
        photo_gray = photo.convert("L")
        pixels = np.array(photo_gray.getdata())

        # Compute Otsu threshold and binary transform
        self.threshold_value = threshold_otsu(pixels)

        photo_binary = photo_gray.point(lambda x: 0 if x < self.threshold_value else 255)

        # Update image display
        new_width_edited =  self.edited_img_label.winfo_width()
        new_height_edited =  self.edited_img_label.winfo_height()

        x_center_edited = (new_width_edited - self.photo_image.width()) / 2
        y_center_edited = (new_height_edited - self.photo_image.height()) / 2

        self.photo_image_edited = ImageTk.PhotoImage(photo_binary)
        if hasattr(photo, "edited_canvas"):
                photo.edited_canvas.destroy()

        canvas = tk.Canvas(self.edited_img_label)#, width=photo.width, height=photo.height)
        canvas.pack()
        canvas.place(relwidth=1.0, relheight=1.0)
        canvas.create_image(x_center_edited, y_center_edited, anchor=tk.NW, image=self.photo_image_edited)

        self.otsu_histogram_update( photo, self.threshold_value)

    def otsu_histogram_update(self, photo, value ): #= self.threshold_value): não da pra colocar self como valor de um parametro??
         #apply the red line in the histogram
        plt.clf()
        plt.hist(photo.histogram(), bins=256, range=(0, 256))

        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(photo.histogram(), bins=20, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))       
        self.hist = self.histogram_container.gca()
        self.hist.hist(photo.histogram(), bins=20, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))#(photo.histogram(), bins=256, range=(0, 256))
        self.hist.axvline(value, color='r', ls='--')
        self.hist.set_xlabel('Pixel Value', fontsize = 12)
        self.hist.set_title('Pixel Histogram', fontsize = 12)
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        self.histogram_canvas.draw()

    def update_contrast(self,photo, value):
        """
        # Update the contrast of the image based on the current scale value
        enhancer = ImageEnhance.Contrast(photo)
        # contrasted_img = enhancer.enhance(float(value))
        photo = enhancer.enhance(float(value))
        # Resize image to fit canvas and convert to PhotoImage
        # self.image = self.image.resize(self.size , Image.LANCZOS)
        photo.thumbnail(photo.size)

        # Update the label with the new image
        self.photo_image = ImageTk.PhotoImage(photo)
        # photo_canvas.configure(image=self.photo_image)

        canvas = tk.Canvas(self, width=photo.width, height=photo.height)
        canvas.place(relx=0, rely=0.5, anchor=tk.W, y=10)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        # Store a reference to the modified image
        self.modified_img = photo.copy() 
        """
        enhancer = ImageEnhance.Contrast(photo)
        photo_contrast = enhancer.enhance(float(value))

        # Update image display
        new_width_edited =  self.edited_img_label.winfo_width()
        new_height_edited =  self.edited_img_label.winfo_height()

        x_center_edited = (new_width_edited - self.photo_image.width()) / 2
        y_center_edited = (new_height_edited - self.photo_image.height()) / 2

        self.photo_image_edited = ImageTk.PhotoImage(photo_contrast)
        if hasattr(photo, "edited_canvas"):
                photo.edited_canvas.destroy()

        canvas = tk.Canvas(self.edited_img_label)#, width=photo.width, height=photo.height)
        canvas.pack()
        canvas.place(relwidth=1.0, relheight=1.0)
        canvas.create_image(x_center_edited, y_center_edited, anchor=tk.NW, image=self.photo_image_edited)
        
        # Resize image to fit canvas and convert to PhotoImage
        # self.modified_img = self.modified_img.resize(self.original_size , Image.LANCZOS)
        plt.clf()
        plt.hist(photo.histogram(), bins=256, range=(0, 256))

        self.histogram_canvas.figure.clear()
        self.histogram_data, _ = np.histogram(photo.histogram(), bins=20, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))        
        self.hist = self.histogram_container.gca()
        self.hist.hist(photo.histogram(), bins=20, weights=np.ones(len(photo.histogram()))/len(photo.histogram()), range=(0, 256))#(photo.histogram(), bins=256, range=(0, 256))
        self.hist.set_xlabel('Pixel Value', fontsize = 12)
        self.hist.set_title('Pixel Histogram', fontsize = 12)
            
        self.hist.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        # self.histogram_canvas.figure.add_subplot(111).hist(self.image.histogram(), bins=256, range=(0, 256))

        self.histogram_canvas.draw()
        


if __name__ == '__main__':
    app = FullScreenApp()
    app.mainloop()