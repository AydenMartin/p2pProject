import socket
from tkinter import *
import tkinter as tk
import threading

class Application(tk.Frame):
    global frame
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Peer to Peer gui")
        frame = Frame(master, width=500, height=500)
        frame.pack()
        self.create_widgets(frame)

    def create_widgets(self,frame):
        Listen = Button(frame,text="Listen",fg="blue",command=lambda :self.startListening(frame))
        Listen.place(x=200,y=10,height=30,width=50)

        Connect = Button(frame,text="connect",fg="blue",command=lambda :self.startConnecting(frame))
        Connect.place(x=250,y=10,height=30,width=50)


    def startListening(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        iplabel = Label(frame, text="IP")
        iplabel.place(x=175, y=10)
        ip = Entry(frame)
        ip.place(x=200, y=10, height=20, width=100)

        portlabel = Label(frame, text="PORT")
        portlabel.place(x=155, y=40)
        port = Entry(frame)
        port.place(x=200, y=40, width=100, height=20)

        submit = Button(frame, text="submit")
        submit.place(x=225, y=80, height=50, width=50)
        submit["command"] = lambda: self.Listen(frame,ip.get(),int(port.get()))


    def Listen(self,frame,ip,port):
        peer1 = peerService()

        for widget in frame.winfo_children():
            widget.destroy()

        #messageThread = threading.Thread(target=self.Messaging, args=[frame])
        listenThread = threading.Thread(target=peer1.listen,args=[frame,ip,port])
        listenThread.start()
        #messageThread.start()

    def startConnecting(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        iplabel = Label(frame,text="IP")
        iplabel.place(x=175,y=10)
        ip = Entry(frame)
        ip.place(x=200,y=10,height=20,width=100)

        portlabel = Label(frame,text="PORT")
        portlabel.place(x=155,y=40)
        port = Entry(frame)
        port.place(x=200,y=40,width=100,height=20)

        submit = Button(frame,text="submit")
        submit.place(x=225,y=80,height=50,width=50)
        submit["command"] = lambda :self.Connect(frame,ip.get(),port.get())

    def Connect(self,frame,ip,port):
        peer2 = peerService()
        for widget in frame.winfo_children():
            widget.destroy()

        #messageThread = threading.Thread(target=self.Messaging, args=[frame])
        listenThread = threading.Thread(target=peer2.connection, args=[frame,ip,int(port)])
        #messageThread.start()
        listenThread.start()

    # def Messaging(self,frame):
    #     msgLabel = Label(frame, text="your msg")
    #     msgLabel.place(x=50, y=50)
    #     textSubmit = Entry(frame)
    #     textSubmit.place(x=300, y=400, height=50, width=100)

class peerService:
    counter = 1.0
    def connection(self,frame,ip,port):
        friend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            friend.connect((ip,port))
        except ConnectionRefusedError:
            print("connection couldnt be established")

        start()
        print('You connected succesfully')
        SENDthread = threading.Thread(target=self.Messaging, args=[frame,friend])
        SENDthread.start()
        messages = Text(frame)
        messages.place(x=50, y=10, height=200, width=200)
        while True:
                data = friend.recv(4096).decode()
                self.Recv(messages, data)
                if not data:
                    break
                print(data)

        print("Connection has been terminated.")
        exit(0)


    def listen(self,frame,ip,port):
        client1 = socket.socket()
        client1.bind((ip, port))
        client1.listen(1)
        friend, addr = client1.accept()
        SENDthread = threading.Thread(target=self.Messaging, args=[frame,friend])
        SENDthread.start()
        messages = Text(frame)
        messages.place(x=50, y=10, height=200, width=200)
        while True:
            data = friend.recv(4096).decode()
            self.Recv(messages,data)
            if not data:
                break
            print(data)

        print("Connection has been terminated.")
        exit(0)


    def Recv(self,messages,msg):
        messages.insert(self.counter,msg)
        self.counter = self.counter + 1.0

    def Messaging(self, frame, friend):
        textSubmit = Entry(frame)
        textSubmit.place(x=175, y=350, height=50, width=100)
        submit = Button(frame,text="Submit")
        submit.place(x=200,y=420)
        submit["command"]=lambda: self.send(friend, textSubmit.get())
        textSubmit.delete(0,END)

    def send(self,conn,msg):
        conn.send(msg.encode())


def start():
    top = tk.Tk()
    top.minsize(500, 500)
    Application(master=top)
    top.mainloop()

start()
