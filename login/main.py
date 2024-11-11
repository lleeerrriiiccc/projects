from other.tools.functions import *
import tkinter as tk

#main window
root = tk.Tk()
root.title('app')
root.geometry('300x300')
root.title('app')

# login frame
frame = tk.Frame(root)
frame.pack()
user = tk.Entry(frame)
user.pack()
password = tk.Entry(frame)
password.pack()

def clearentry(id):
    id.delete(0, 'end')
    return

#functions
def frame_unpack():
    frame.pack_forget()
    user.pack_forget()
    password.pack_forget()
    login.pack_forget()

def frame_pack():
    frame.pack()
    user.pack()
    password.pack()
    login.pack()


def frame2_unpack():    
    frame2.pack_forget()
    root.config(menu='')
def comands():
    if loginfun(user.get(), password.get()) == True:
        dashboard()
        clearentry(user)
        clearentry(password)
login = tk.Button(frame, text='Login', command=comands) 
login.pack()
def logout():
    frame_pack()
    frame2_unpack()

def newuser():
    username = tk.Entry(frame2)
    password = tk.Entry(frame2)
    isadmin = tk.Checkbutton(frame2, onvalue="true", offvalue="false", text=" is admin?")
    username.pack()
    password.pack()
    isadmin.pack()
    create = tk.Button(frame2, text='Crear', command=lambda: createuser(username.get(), password.get(), isadmin.getboolean(1)))
    create.pack()

def deluser():
    username = tk.Entry(frame2)
    username.pack()
    delete = tk.Button(frame2, text='Eliminar', command=lambda: delete("login/other/data/data.json", "user", username.get()))
    delete.pack()


    



def dashboard():
    frame_unpack()
    frame2.pack()
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    filemenu = tk.Menu(menubar)
    menubar.add_cascade(label="Archivo", menu=filemenu)
    filemenu.add_command(label="Cerrar sesion", command=logout)
    
    obj = list("login/other/data/logeduser.json", 0)
    
    id = obj["id"]  
    if isadmin(id) == True:
        adminmenu = tk.Menu(root)
        menubar.add_cascade(label="Administrar", menu=adminmenu)
        adminmenu.add_command(label="Crear usuario", command=newuser)
        adminmenu.add_command(label="Eliminar usuario", command=deluser)


frame2 = tk.Frame(root)


root.mainloop()
