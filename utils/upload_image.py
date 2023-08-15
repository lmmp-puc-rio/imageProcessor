
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
            self.update_image()
            
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