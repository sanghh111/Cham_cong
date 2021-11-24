from numpy.lib.arraypad import pad
from Detector import main_app
from Manager import Manager
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import Label, font as tkfont
from tkinter import messagebox,PhotoImage
#from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender
names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        global namess
        global manager 
        manager = None
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour,PageManagerLogin,PageManager,PageAddUser):
            page_name = F.__name__
            print('page_name: ', page_name)
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("PageManagerLogin")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew")
            button1 = tk.Button(self, text="       Chấm Công      ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button2 = tk.Button(self, text="   Quản lý đăng nhập  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageManagerLogin"))
            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)


class PageManagerLogin(tk.Frame):
    def __init__(self,parent,controller):
        self.manager  = Manager()
        tk.Frame.__init__(self,parent)
        self.controller = controller
        tk.Label(self, text="QUẢN LÝ ĐĂNG NHẬP",fg="#263942", font='Helvetica 14 bold').grid(row=0, column=1, pady=20,columnspan=2)
        tk.Label(self, text="Account", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, pady=(20,10), padx=(110,10))
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=1, column=1, pady=(20,10), padx=0)
        tk.Label(self, text="Password", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=0, pady=10, padx=(110,10))
        self.password = tk.Entry(self, borderwidth=2, show="*", bg="lightgrey", font='Helvetica 11')
        self.password.grid(row=2, column=1, pady=10, padx=0)
        self.buttoncanc = tk.Button(self, text="QUAY LẠI", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonlogin = tk.Button(self, text="ĐĂNG NHẬP", fg="#ffffff", bg="#263942", command=self.login)
        self.buttoncanc.grid(row=3, column=0, pady=10, ipadx=5, ipady=4,padx=(110,10))
        self.buttonlogin.grid(row=3, column=1, pady=10, ipadx=5, ipady=4,padx=(40,0))
        # self.bind()

    def login(self):
        state =  self.manager.login(self.user_name.get(),self.password.get())
        if state:
            self.controller.show_frame("PageManager")

class PageManager(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #load = Image.open("homepagepic.png")
        #load = load.resize((250, 250), Image.ANTIALIAS)
        render = PhotoImage(file='managepage.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        label = tk.Label(self,    text="        Quản Lý         ", font=self.controller.title_font,fg="#263942")
        label.grid(row=0, sticky="ew")
        button1 = tk.Button(self, text="     Thêm nhân viên     ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageAddUser"))
        button2 = tk.Button(self, text="   Thêm data khuôn mặt  \ncho nhân viên", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
        # button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        # button3.grid(row=3, column=0, ipady=3, ipadx=32)

class PageAddUser(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        tk.Label(self, text="ID", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, pady=(20,10), padx=(110,10))
        self.id = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.id.grid(row=1, column=1, pady=(20,10), padx=0)
        tk.Label(self, text="Full name", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=0, pady=(20,10), padx=(110,10))
        self.gmail = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.gmail.grid(row=2, column=1, pady=(20,10), padx=0)
        tk.Label(self, text="Gmail", fg="#263942", font='Helvetica 12 bold').grid(row=3, column=0, pady=(20,10), padx=(110,10))
        self.dayOfBirth = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.dayOfBirth.grid(row=3, column=1, pady=(20,10), padx=0)
        tk.Label(self, text="Phone", fg="#263942", font='Helvetica 12 bold').grid(row=4, column=0, pady=(20,10), padx=(110,10))
        self.phone = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.phone.grid(row=4, column=1, pady=(20,10), padx=0)
        button1 = tk.Button(self, text="Thêm nhân viên", fg="#ffffff", bg="#263942",command= self.addUser)
        button2 = tk.Button(self, text="   Quay lại   ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageManager"))
        # button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
        button1.grid(row=5, column=1, ipady=3, ipadx=7)
        button2.grid(row=5, column=0, ipady=3, ipadx=2)

    def addUser(self):
        pass


app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

