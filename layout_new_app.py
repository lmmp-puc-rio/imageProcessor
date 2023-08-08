'''
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename="yeti")
root.title("Image Processor")
#root.geometry("900x600")
root.attributes('-fullscreen', True)
root.overrideredirect(False)

'''
import tkinter as tk
#from tkinter import ttk
import customtkinter

root = tk.Tk()
root_ctk = customtkinter.CTk()
root.attributes("-fullscreen", True)
root.overrideredirect(False)

#colors in app
pry_color = "#5376D6"
sec_color = "#D9D9D9"
btn_color = "#DDE4F7"

#heigth in app

header_hg = root.winfo_screenheight()
main_hg = root.winfo_screenheight()
footer_hg = root.winfo_screenheight()

#root config
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=7)
root.rowconfigure(2, weight=3)

#top frame
header_frame = tk.Frame(root, background = pry_color)
header_frame.columnconfigure(0, weight=0)
header_frame.columnconfigure(1, weight=8)
header_frame.columnconfigure(2, weight=1)
img_home_btn = tk.Button(header_frame, text='entrar na Home', font=('Montserrat', 16),height= 3, width=15)
upload_btn = tk.Button(header_frame, text="Upload Image", background = btn_color)
help_btn = tk.Button(header_frame, text="Help", background = btn_color)
close_btn = tk.Button(header_frame, text='x', font=('Arial', 12), bg= btn_color, height= 1, width=2)
minimize_btn = tk.Button(header_frame, text='-', font=('Arial', 12), bg= btn_color,  height= 1, width=2)

#top widget
header_frame.grid(row=0, column=0, sticky='WENS')
img_home_btn.grid(row= 0 , column= 0, sticky ='W')
upload_btn.grid(row= 0 , column= 1, padx=40, sticky ='E', pady=2)
help_btn.grid(row= 0 , column= 1, padx=2, sticky ='E', pady=2)
minimize_btn.grid(row= 0 , column= 2, sticky ='NE', padx=30, pady=5)
close_btn.grid(row= 0 , column= 2, sticky ='NE', padx=2, pady=5)


#main frame
main_frame = tk.Frame(root, background='red')
main_frame.rowconfigure(0, weight=0)
main_frame.rowconfigure(1, weight=1)
main_frame.columnconfigure(0, weight=4)
main_frame.columnconfigure(1, weight=4)
main_frame.columnconfigure(2, weight=3)
original_txt = tk.Label(main_frame, text='Original Image')
edited_txt = tk.Label(main_frame, text='Edited Image')
histogram_txt = tk.Label(main_frame, text='Histogram')
original_img_label= tk.Label(main_frame,text =' imagem original',  background='gray')
edited_img_label = tk.Label(main_frame,text =' imagem editada', background='gray')
histogram_img_label = tk.Label(main_frame,text =' histograma ', background='gray')


#main widget
main_frame.grid(row=1, column=0, sticky='WENS')
original_txt.grid(row=0, column=0, sticky='N', pady=(6,2))
edited_txt.grid(row=0, column=1, sticky='N', pady=(6,2))
histogram_txt.grid(row=0, column=2, sticky='N', pady=(6,2))

original_img_label.grid(row=1, column=0, sticky='WENS', padx=2, pady=5)
edited_img_label.grid(row=1, column=1, sticky='WENS', padx=2, pady=5)
histogram_img_label.grid(row=1, column=2, sticky='WENS', padx=2, pady=5)


#footer Wdiget
footer_frame = tk.Frame(root, background='yellow')
footer_frame.rowconfigure(0, weight=1)
footer_frame.columnconfigure(0, weight=4)
footer_frame.columnconfigure(1, weight=4)
footer_frame.columnconfigure(2, weight=3)

contrast_frame = tk.Frame(footer_frame, background='brown')
treshold_frame = tk.Frame(footer_frame, background='green')
save_frame = tk.Frame(footer_frame, background='blue')


#footer frame
footer_frame.grid(row=2, column=0, sticky='WENS')
contrast_frame.grid(row=0, column=0,sticky='WENS', padx=3, pady=3)
treshold_frame.grid(row=0, column=1,sticky='WENS', padx=3, pady=3)
save_frame.grid(row=0, column=2, padx=3,sticky='WENS', pady=3)


#Contrast Frame
contrast_frame.columnconfigure(0, weight=1)
contrast_frame.rowconfigure(0, weight=1)
contrast_frame.rowconfigure(1, weight=8)
contrast_frame.rowconfigure(2, weight=1)

text_contrast = tk.Label(contrast_frame, text='CONTRAST')
bar_contrast = tk.Scale(contrast_frame, from_=0.1, to=5.0, resolution=0.1, label="Value")
value_contrast = tk.Label(contrast_frame, text='00')

text_contrast.grid(row=0, column=0,sticky='NS', padx=3, pady=(5,10))
bar_contrast.grid(row=1, column=0,sticky='EW', padx=3, pady=5)
value_contrast.grid(row=2, column=0,sticky='N', padx=3, pady=5)


#treshold Frame
radio_selected = 0
list_treshold_model = ['OTSU', 'XXX', 'YYYYYYYYYYYYYY']
list_selected = tk.StringVar()
list_selected.set(list_treshold_model[0])

def selected():
    print(tk.StringVar.get())

treshold_frame.columnconfigure(0, weight=7)
treshold_frame.columnconfigure(1, weight=3)

treshold_frame.rowconfigure(0, weight=1)
treshold_frame.rowconfigure(1, weight=1)
treshold_frame.rowconfigure(2, weight=1)
treshold_frame.rowconfigure(3, weight=1)
treshold_frame.rowconfigure(4, weight=1)

text_treshold = tk.Label(treshold_frame, text='TRESHOLD')
dropdow_treshold = tk.OptionMenu(treshold_frame,list_selected, *list_treshold_model)
radio1_btn_treshold =tk.Radiobutton(treshold_frame,text='Automatic', value=0, variable = radio_selected, command= selected)
radio2_btn_treshold =tk.Radiobutton(treshold_frame,text='Manual', value=1, variable = radio_selected, command= selected)
value_treshold = tk.Label(treshold_frame, text= '000',)
treshold_btn = tk.Button(treshold_frame, text='RUN MODEL')

text_treshold.grid(row=0, column=0,columnspan=2,sticky='N', padx=3, pady=5)
dropdow_treshold.grid(row=1, column=0,sticky='N', padx=3, pady=5)
radio1_btn_treshold.grid(row=2, column=0,sticky='N', padx=3, pady=5)
radio2_btn_treshold.grid(row=3, column=0,sticky='N', padx=3, pady=5)
value_treshold.grid(row=4, column=0,sticky='N', padx=3, pady=5)
treshold_btn.grid(row=2, column=1,rowspan=3,sticky='N', padx=3, pady=5)

#Save Frame

save_frame.columnconfigure(0, weight=7)
save_frame.columnconfigure(0, weight=3)
save_frame.rowconfigure(0, weight=1)
save_frame.rowconfigure(1, weight=1)
save_frame.rowconfigure(2, weight=1)
save_frame.rowconfigure(3, weight=1)
save_frame.rowconfigure(4, weight=1)


text_checkbox = tk.Label(save_frame, text='SAVE PROJECT')
checkbox1_frame = tk.Checkbutton(save_frame, text="SAVE IMAGE", variable= 'save_image')
checkbox2_frame = tk.Checkbutton(save_frame, text="SAVE HISTORY", variable= 'save-history')
checkbox3_frame = tk.Checkbutton(save_frame, text="SAVE HISTOGRAM", variable= 'save_histo')
checkbox_btn = tk.Button(save_frame, text='SAVE PROJECT')

text_checkbox.grid(row=0, column=0,columnspan=2, sticky='N', padx=2, pady=3)
checkbox1_frame.grid(row=1, column=0, sticky='N', padx=2, pady=3)
checkbox2_frame.grid(row=2, column=0, sticky='N', padx=2, pady=3)
checkbox3_frame.grid(row=3, column=0, sticky='N', padx=2, pady=3)
checkbox_btn.grid(row=2, column=1, sticky='N', padx=2, pady=3)




root.mainloop()

