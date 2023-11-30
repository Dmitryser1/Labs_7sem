import tkinter as tk
from tkinter import font, NW, NE, LEFT, TOP, END
import numpy as np
import sympy as sm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy import optimize

a = sm.Symbol('α')
l = sm.Symbol('l')
D = sm.Symbol('D')
t = sm.Symbol('T')
C = sm.Symbol('C')
lam = sm.Symbol('λ')
x = sm.Symbol('x')
ls = 12 #l
Ds = 0.007 #D
As = 0.12 #alpha
cs = 0.8 #c
ts = 80 #T
Gs = 10# gamma

def funct(l, t, x, a, D, g, C): 
    summ = 0
    for n in range(200): 
        lam = (np.pi * (1 + 2 * n) / l) ** 2
        summ+=((-(4 * D * g * (-1) ** n) / (np.pi * (1 + 2 * n) * (a * lam + D))) *
        (D + a* lam * np.exp(-t * (a * lam + D) / C)) 
        ) * np.cos((np.pi * x * (1 + 2 * n)) / l - (np.pi * (1 + 2 * n)) / 2) 
        # summ+=(-(4 * D * g * (-1) ** n) / (np.pi * (1 + 2 * n) * (a * lam + D)) - 
        # (((-1) ** n * g * 4 * ( a * lam )) / (np.pi * (1 + 2 * n) * (a * lam + D))) * np.exp(-t * (a * lam + D) / C) 
        # ) * np.cos((np.pi * x * (1 + 2 * n)) / l - (np.pi * (1 + 2 * n)) / 2)
    return summ + g

def g1():
    global ls, Ds, bs, ts, Hs, el, eD, eb, eH
    try:
        ls = float(el.get())
        Ds = float(eD.get())
        As = float(eA.get())
        Hs = float(eH.get())
    except:
        pass
    init()
    #points = get_lam()
    tt = [0, ts / 5, 2 * ts / 5, 3 * ts / 5, 4 * ts / 5, ts]
    x = np.linspace(0, ls, 100, endpoint=True)
    fig = Figure(figsize=(5, 5), dpi=100)
    plot1 = fig.add_subplot(1, 1, 1)
    for it in tt:
        y = funct(ls, it, x, As, Ds, Gs, cs)
        plot1.plot(x, y, label="t=" + str(it))
        plot1.legend()
    plot1.set_xlabel('x')
    plot1.set_ylabel('$u(x)$')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=LEFT)
    #toolbar = NavigationToolbar2Tk(canvas, root)
    #toolbar.update()
    #canvas.get_tk_widget().pack(side=TOP)
    g2()

def g2():
    xx = [0, ls / 5, 3 * ls / 10, 3 * ls / 5, 5 * ls / 10, ls]
    fig = Figure(figsize=(5, 5), dpi=100)
    plot1 = fig.add_subplot(1, 1, 1)
    t = np.linspace(0, ts, 200, endpoint=True)
    for ix in xx:
        y = funct(ls, t, ix, As, Ds, Gs, cs)
        plot1.plot(t, y, label="x=" + str(ix))
        plot1.legend()
    plot1.set_xlabel('t')
    plot1.set_ylabel('$u(t)$')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=LEFT)
    #toolbar = NavigationToolbar2Tk(canvas, root)
    #toolbar.update()
    #canvas.get_tk_widget().pack()

def defa():
    global root, el, eD, eA, eG, f1, font1, ls, Ds, As, ts, Gs
    ls = 12 #l
    Ds = 0.007 #D
    As = 0.12 #alpha
    cs = 0.8 #c
    ts = 80 #T
    Gs = 10
    el.delete(0, END)
    el.insert(0, str(ls))
    eD.delete(0, END)
    eD.insert(0, str(Ds))
    eA.delete(0, END)
    eA.insert(0, str(As))
    eG.delete(0, END)
    eG.insert(0, str(Gs))
    
def init():
    global root, el, eD, eA, eG, f1, font1, ls, Ds, As, ts, Gs
    root.destroy()
    root = tk.Tk()
    root.title("Диффузия вещества")
    root["bg"] = "grey"
    root.geometry("1450x700")
    font1 = font.Font(family="Arial", size=20, weight="normal", slant="roman")
    f1 = tk.Frame(root, background="grey")
    el = tk.Entry(f1, font=font1, background="mintcream")
    eD = tk.Entry(f1, font=font1, background="mintcream")
    eA = tk.Entry(f1, font=font1, background="mintcream")
    eG = tk.Entry(f1, font=font1, background="mintcream")
    lb1 = tk.Label(f1, text='Диффузия вещества', font=font1, background="grey")
    lbc = tk.Label(f1, text='Текущие параметры\n l = ' + str(ls) + ', D = ' + str(Ds) + ',\n α = ' + str(As) + ', γ = ' + str(Gs), font=font1, background="grey")
    lbl = tk.Label(f1, text='Введите l', font=font1, background="grey")
    lbD = tk.Label(f1, text='Введите D', font=font1, background="grey")
    lba = tk.Label(f1, text='Введите α', font=font1, background="grey")
    lbG = tk.Label(f1, text='Введите γ', font=font1, background="grey")
    bt = tk.Button(f1, text="Применить", font=font1, command=g1, background="mintcream")
    bd = tk.Button(f1, text="По умолчанию", font=font1, command=defa, background="mintcream")
    f1.pack(side=LEFT)
    lb1.pack(anchor=NW, padx=20, pady=10)
    lbc.pack(anchor=NW, padx=20, pady=10)
    lbl.pack(anchor=NW, padx=20)
    el.pack(anchor=NW, padx=20)
    lbD.pack(anchor=NW, padx=20)
    eD.pack(anchor=NW, padx=20)
    lba.pack(anchor=NW, padx=20)
    eA.pack(anchor=NW, padx=20)
    lbG.pack(anchor=NW, padx=20)
    eG.pack(anchor=NW, padx=20)
    bt.pack(anchor=NW, padx=80, pady=15)
    bd.pack(anchor=NW, padx=55, pady=15)

root = tk.Tk()
font1 = font.Font(family="Arial", size=20, weight="normal", slant="roman")
f1 = tk.Frame(root, background="grey")
el = tk.Entry(f1, font=font1, background="mintcream")
eD = tk.Entry(f1, font=font1, background="mintcream")
eA = tk.Entry(f1, font=font1, background="mintcream")
eG = tk.Entry(f1, font=font1, background="mintcream")
init()
root.mainloop()
