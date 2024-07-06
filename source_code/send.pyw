import socket
from tkinter import *
from tkinter import messagebox
import json

window = Tk()
scrx = window.winfo_screenwidth() // 2
scry = window.winfo_screenheight() // 2
window_sz = str(scrx)+"x"+str(scry)
window.geometry(window_sz)
window.title("消息收发器")
hosts = {"(fallback)":"127.0.0.1"}
names = ["(fallback)"]
variable = StringVar()
targ = OptionMenu(window, variable, *names)
targ.configure(font=("Consolas", 13))
targ['menu'].configure(font=("Consolas", 13))

def set_optionmenu(opl):
    targ['menu'].delete(0, 'end')
    for op in opl:
        targ['menu'].add_command(label=op, command=lambda x=op:variable.set(x))
    variable.set(opl[-1])

def work(tar, ip):
    hosts[tar] = ip
    if names.count(tar) == 0:
        names.append(tar)
    set_optionmenu(names)
    with open('ip.json','w') as f:
        json.dump(hosts, f)
    with open('names.json','w') as f:
        json.dump(names, f)

"""
 
root = tk.Tk()
 
variable = tk.StringVar()
variable.set(OPTIONS[0])
 
w = tk.OptionMenu(root, variable, *names)
w.pack()
 
def callback():
    print(variable.get())
 
tk.Button(root, text="点我", command=callback).pack()
"""

def add_host():
    New = Tk()
    New.geometry('400x150')
    New.title("添加新对象")

    name = Entry(New, width=20, font=("Consolas", 14))
    ip = Entry(New, width=20, font=("Consolas", 14))
    btn = Button(New, text="完成", font=("Consolas", 13), command=lambda: [work(name.get(), ip.get()), New.destroy()])
    btn.pack(side=BOTTOM)
    ip.pack(side=BOTTOM, anchor=CENTER)
    intro2 = Label(New, text="请输入发送对象的IP:", font=("Consolas", 15))
    intro2.pack(side=BOTTOM, anchor=CENTER)
    name.pack(side=BOTTOM, anchor=CENTER)
    intro1 = Label(New, text="请输入发送对象的名称:", font=("Consolas", 15))
    intro1.pack(side=BOTTOM, anchor=CENTER)

    New.mainloop()

def main():
    target = variable.get()
     
    host = hosts[target]
    msg = inmsg.get(1.0, "end-1c")
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_client.settimeout(2)
    try:
        socket_client.sendto(msg.encode("UTF-8"), (host, 1234))
        # 接收服务端的数据
        conn, addr = socket_client.recvfrom(2048)
        data_from_server = conn.decode("UTF-8")
        if data_from_server == "recieved":
            messagebox.showinfo("消息", "消息接收成功！")
        elif data_from_server == "refused":
            messagebox.showinfo("消息", "发送过于频繁！")
    except:
        messagebox.showerror("错误", "接收端未开启或不可用")

    socket_client.close()
 
if __name__ == '__main__':
    try:
        with open('ip.json','r') as f:
            hosts = json.loads(f.read())
        with open('names.json','r') as f:
            names = json.loads(f.read())
    except:
        with open('ip.json','w+') as f:
            json.dump(hosts, f)
        with open('names.json','w+') as f:
            json.dump(names, f)

    set_optionmenu(names)
    btn = Button(window, text="发送", font=("Consolas", 13), command=main)
    btn.pack(side=BOTTOM)
    inmsg = Text(window, height=10, font=("Consolas", 13))
    inmsg.pack(side=BOTTOM, fill=BOTH, expand=YES)
    targ.pack(side=LEFT, anchor=CENTER)
    create = Button(window, text="添加……", font=("Consolas", 13), command=add_host)
    create.pack(side=LEFT, anchor=CENTER)
    window.mainloop()
