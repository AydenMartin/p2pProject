import socket
from tkinter import *
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Peer to Peer gui")
        frame=Frame(master, width=500, height=500)
        frame.pack()
        self.create_widgets(frame)

    def create_widgets(self,frame):
        Listen = Button(frame,text="Listen",fg="blue",command=lambda :self.startListening(frame))
        Listen.place(x=200,y=10,height=30,width=50)
        Connect = Button(frame,text="connect",fg="blue",command=lambda :self.startConnecting(frame))
        Connect.place(x=250,y=10,height=30,width=50)


    def startListening(self,frame):
        peer1 = peerService()

        for widget in frame.winfo_children():
            widget.destroy()

        port = Text(frame)
        port.place(x=200, y=40, width=100, height=20)

        submit = Button(frame, text="submit",
                        command=lambda: peer1.listen(int(port.get("1.0", END))))
        submit.place(x=225, y=80, height=50, width=50)



    def startConnecting(self,frame):
        peer2 = peerService

        for widget in frame.winfo_children():
            widget.destroy()
        ip = Text(frame)

        ip.place(x=200,y=10,height=20,width=100)

        port = Text(frame)
        port.place(x=200,y=40,width=100,height=20)

        submit = Button(frame,text="submit",
                        command=lambda :peer2.connection(peer2,ip.get("1.0",END),int(port.get("1.0",END))))
        submit.place(x=225,y=80,height=50,width=50)
        print("check1")





class peerService:
    def connection(self,ip,port):
        friend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def connect(ip, port, friend):
            friend.connect((ip, port))

        connect(ip, port, friend)
        print('You connect. \n Type \"quit\" to exit')
        while True:
                message = input("")
                while message != 'quit':
                    print("You: " + message)
                    friend.send(message.encode())
                    data = friend.recv(4096).decode()
                    if not data:
                        break
                    print('Friend:' + data)

                    message = input()
                print("Connection has been terminated.")
                exit(0)


    def listen(self,port):
        host = "127.0.0.1"
        print("check2")
        client1 = socket.socket()
        client1.bind((host, port))

        client1.listen(1)
        conn, addr = client1.accept()
        print("Your friend connected from: " + str(addr) + ". Type \"quit\" to exit")
        while True:
            data = conn.recv(4096).decode()
            if not data:
                break
            print("Friend: " + str(data))
            message = input()
            print("You: " + str(message))
            if message == "quit":
                print("Connection has been terminated.")
                exit(0)
            conn.send(message.encode())

        print("Connection has been terminated.")
        exit(0)

def start():
    top = tk.Tk()
    top.minsize(500, 500)
    Application(master=top)
    top.mainloop()

start()
