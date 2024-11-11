from tkinter import Tk, Label, Entry, Button, messagebox
import customtkinter
import math as math
from math import sqrt
def calc():
    try:
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get())
        z = int((-4*a*c))*(-1)
        y = int(b*b)
        x = int(2*a)
        l = int(b*(-1))
        p = int(y-z)        
        k = (math.sqrt(p))
    except:  
        
        messagebox.showerror('error de calculo','La raiz es negativa no es posible dar un resultado')
    else:
        primerasolucion = str((l+k)/x)
        segundasolucion = str((l-k)/x)
        soluciones = list(primerasolucion)
        soluciones.append(segundasolucion)
        
        soluciones_label = Label(window, text=soluciones)
        soluciones_label.pack()


    
#pagina principal
window = Tk()
window.title("calculadora")
window.geometry("300x200")
#a
a_label = Label(window, text='Escribe el valor de a:')
a_label.pack()
a_entry = Entry(window)
a_entry.pack()
#b
b_label = Label(window, text='Escribe el valor de b:')
b_label.pack()
b_entry = Entry(window)
b_entry.pack()
#c
c_label = Label(window, text='Escribe el valor de c:')
c_label.pack()
c_entry = Entry(window)
c_entry.pack()
#botones
calc_button = Button(window, text='Pulse para calcular', command=calc)
calc_button.pack()
#estetica
customtkinter.set_default_color_theme("dark-blue")



window.mainloop()