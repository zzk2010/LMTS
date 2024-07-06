import socket
import os
from tkinter import *
from tkinter import messagebox
import threading
import time
import pyttsx3

desktop_path = os.path.expanduser("~/Desktop")
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind(('0.0.0.0', 1234))
lst = {}

def cp(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

def rd(msg):
    rd = pyttsx3.init()
    rd.say(msg)
    rd.runAndWait()

def showmsg(msg, addr):
    window = Tk()
    window.title("消息")
    window.config(bg="black")
    window.wm_attributes("-topmost", True)
    intro = Label(window, text=msg, fg="white", bg="black", font=("Consolas", 20))
    intro.grid(row=0, column=0, columnspan=2)
    frominfo = Label(window, text="\nFrom "+addr, fg="white", bg="black", font=("Consolas", 12))
    frominfo.grid(row=1, column=0, columnspan=2)
    btn_cp = Button(window, text="拷贝", font=("Consolas", 13), command=lambda:cp(msg))
    btn_cp.grid(row=2, column=0)
    btn_read = Button(window, text="朗读", font=("Consolas", 13), command=lambda:rd(msg))
    btn_read.grid(row=2, column=1)
    window.mainloop()

if __name__ == '__main__':
    while True:
        conn, addr = socket_server.recvfrom(2048)
        ip, msg = addr[0], conn.decode("UTF-8")
        if lst.get(ip) == None:
            lst[ip] = time.time()
        else:
            if time.time()-lst[ip] <= 1:
                socket_server.sendto('refused'.encode("UTF-8"), addr)
                continue
            else:
                lst[ip]=time.time()
        socket_server.sendto("recieved".encode("UTF-8"), addr)
        newThread = threading.Thread(target=showmsg, kwargs={"msg":msg, "addr":addr[0]})
        newThread.start()

