import io
import base64
from PIL import Image, ImageTk, ImageGrab

from analyze_image import *

try:
    # Python2
    import Tkinter as tk, Tkconstants, tkFileDialog
    from urllib2 import urlopen
    import tkMessageBox as msg
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen
    from tkinter import messagebox as msg, filedialog

class main_gui(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.resizable(0,0)
        w = 1200
        h = 800
        x = 80
        y = 100

        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

        input_frame = tk.LabelFrame(self, width=100, height=20)
        #frame.grid(row=0, padx=5, pady=8, ipadx=10, ipady=10)
        input_frame.pack()

        l1 = tk.Label(input_frame, text="API KEY: ")
        l1.grid(row=0, column=0, sticky="W")
        l2 = tk.Label(input_frame, text="Image URL: ")
        l2.grid(row=1, column=0, sticky="W")
        api_key_Variable = tk.StringVar()
        e1 = tk.Entry(input_frame, textvariable=api_key_Variable, width=80)
        api_key_Variable.set('1b897276f50843f78412b3185b80afcd')
        e1.grid(row=0, column=1, columnspan=10, sticky="E")
        image_url_Variable = tk.StringVar()
        e2 = tk.Entry(input_frame, textvariable=image_url_Variable, width=80)
        #image_url_Variable.set('http://www.ladyissue.com/wp-content/uploads/2016/08/S__39231503.jpg')
        #image_url_Variable.set('D:/9_Github/3_Github Samples/2_Scraping/microsoft-emotion-recognition/chris_young.jpg')
        e2.grid(row=1, column=1, columnspan=10, sticky="E")

        def callback1():
            filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                       filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            image_url_Variable.set(filename)

        b2 = tk.Button(input_frame, text="Open File", command=callback1)
        b2.grid(row=1, column=12, sticky="E", padx=5, pady=5)

        def callback2():
            api_key = e1.get()
            image_url = e2.get()
            if api_key=='' or image_url=='':
                msg.showerror("Error", "You must enter 'API KEY' and 'Image URL'!!!")
            else:
                self.api_key = api_key
                self.image_url = image_url
                self.app = analyze_image(self.api_key, self.image_url)
                self.data = self.app.data
                self.label_pack()
                self.image_pack()

        b2 = tk.Button(input_frame, text="Calc", command = callback2)
        b2.grid(row=2, column=9, sticky="E")

        self.image_frame = tk.LabelFrame(self, width=1200, height=800)
        self.image_frame.pack()

        def callback3():
            f = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
            if f is None:
                return
            x = self.winfo_rootx()
            y = self.winfo_rooty()
            x1 = x + self.winfo_width()
            y1 = y + self.winfo_height()
            im = ImageGrab.grab().crop((x, y, x1, y1)).save(f.name)
            f.close()

        b3 = tk.Button(input_frame, text="Save File", command = callback3)
        b3.grid(row=2, column=12, sticky="E", padx=5, pady=5)


    def image_pack(self):

        #self.image_byt = urlopen(self.image_url).read()
        self.image_byt = open(self.image_url, "rb").read()

        # internal data file
        self.data_stream = io.BytesIO(self.image_byt)
        # open as a PIL image object
        self.pil_image = Image.open(self.data_stream)

        # convert PIL image object to Tkinter PhotoImage object
        canvas = tk.Canvas(self.image_frame, width=1000, height=800)
        canvas.grid(column = 1, row = 0, sticky="W", padx=5, pady=5)
        size = 1000, 800

        width_org, height_org = self.pil_image.size
        self.pil_image.thumbnail(size, Image.ANTIALIAS)
        width, height = self.pil_image.size
        self.w_rate = width_org/width
        self.h_rate = height_org/height
        self.tk_image = ImageTk.PhotoImage(self.pil_image)

        canvas.create_image(0, 0, anchor="nw", image = self.tk_image)

        h = self.data['faceRectangle']['height']
        l = self.data['faceRectangle']['left']
        t = self.data['faceRectangle']['top']
        w = self.data['faceRectangle']['width']
        x0 = l
        y0 = t
        x1 = l + w
        y1 = t + h
        canvas.create_rectangle(x0/self.w_rate,y0/self.h_rate,x1/self.w_rate,y1/self.h_rate, outline='red', width=3)

    def label_pack(self):
        labelframe = tk.LabelFrame(self.image_frame, text=" Detailed Analysis ")
        labelframe.configure(bg="#4f617b", fg="white", font=('courier', 18, 'bold'),
                             relief="sunken", labelanchor="n")
        # labelframe.grid(row=0, sticky='WE', padx=5, pady=15, ipadx=5, ipady=5)
        labelframe.grid(column = 0, row= 0, sticky="WN", padx=5, pady=5)

        frame = tk.Frame(labelframe)
        frame.configure(background="#4f617b")
        frame.pack(padx=5, pady=5, ipadx=5, ipady=5)

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=0, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Anger")

        anger = self.data["scores"]["anger"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=0, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(anger))

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=1, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Contempt")

        contempt = self.data["scores"]["contempt"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=1, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(contempt))

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=2, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Disgust")

        disgust = self.data["scores"]["disgust"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=2, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(disgust))

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=3, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Fear")

        fear = self.data["scores"]["fear"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=3, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(fear))

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=4, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Happiness")

        happiness = self.data["scores"]["happiness"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=4, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(happiness))

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=5, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Neutral")

        neutral = self.data["scores"]["neutral"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=5, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(neutral))

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=6, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Sadness")

        sadness = self.data["scores"]["sadness"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=6, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(sadness))

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=10,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=0, row=7, columnspan=7, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("Surprise")

        surprise = self.data["scores"]["surprise"]

        labelVariable = tk.StringVar()
        label_title = tk.Label(frame, textvariable=labelVariable,
                               width=20,
                               anchor="nw", justify="left",
                               fg="white", bg="#4f617b", font=('courier', 15, 'normal'))
        label_title.grid(column=9, row=7, columnspan=14, sticky="W",
                         padx=3, pady=3, ipadx=3, ipady=3)
        labelVariable.set("{}".format(surprise))




if __name__ == '__main__':
    api_key = '1b897276f50843f78412b3185b80afcd'

    image_url = 'http://www.ladyissue.com/wp-content/uploads/2016/08/S__39231503.jpg'
    #image_url = 'https://jbf-media.s3.amazonaws.com/production/event/2016/10/3/del_coro_ben1.jpg'
    #image_url = 'http://i46.tinypic.com/r9oh0j.gif'
    app = main_gui(None)
    app.title("Face Emotion Recognition")
    app.mainloop()