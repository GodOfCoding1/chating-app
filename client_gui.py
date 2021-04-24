import socket
import threading
from tkinter import *
import webbrowser


PORT = 6000
SERVER = input("enter server address")
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)
class GUI:

    def __init__(self):

        self.Window = Tk()
        self.Window.withdraw()
        self.Window.iconbitmap("icon.ico")
        self.login = Toplevel()
        self.login.iconbitmap("icon.ico")
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=80)

        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.50,
                             relx=0.05,
                             rely=0.2)
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.5,
                             relheight=0.45,
                             relx=0.20,
                             rely=0.2)
        self.entryName.focus()
        self.go = Button(self.login,
                         text="SUBMIT",
                         font="Helvetica 12 bold",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.75,
                      rely=0.21)
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv = threading.Thread(target=self.receive)
        rcv.start()
    def layout(self, name):

        self.name = name
        self.Window.deiconify()
        self.Window.title("CHAT APP")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550
                              )
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,

                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0)

        self.labelBottom = Label(self.Window,

                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.745)

        self.entryMsg = Entry(self.labelBottom,

                              font="Helvetica 13")

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()


        self.madeby = Label(self.Window, text="Made by Madhav")
        self.madeby.place(relheight=0.15, relwidth=0.3, relx=0.733, rely=0.9)
        self.adbutton = Button(self.Window,
                                text="Watch an Ad",
                                font="Helvetica 10 bold",
                                width=20,

                                command=self.ads)
        self.adbutton.place(relx=0.03,
                             rely=0.925,
                             relheight=0.06,
                             relwidth=0.70)
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,

                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == '?NAME?':
                    client.send(self.name.encode(FORMAT))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occured!")
                client.close()
                break
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break
    def ads(self):
        webbrowser.open("adsbymadhav.ddns.net")
g = GUI()