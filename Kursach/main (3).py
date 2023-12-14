import tkinter as tk
from tkinter import *
from tkinter import font

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy import optimize

As = 0.12 #alpha
Cs = 0.8 #c
Gs= 10# psi/gammafunc


def funct2e(D, alpha, tt, ll, C):
    ii = 100
    kk = 10000
    hx = ll / (2 * ii)
    ht = tt / (kk)
    caf= D*ht/C
    gamma = (alpha * ht) / (C * hx ** 2)
    u = np.zeros((ii + 1, kk + 1))
    for i in range(ii + 1):
        u[i][0] = 0
    for k in range(kk):
        j = 1
        while j < ii:
            u[j][k + 1] = (1 - 2 * gamma) * u[j][k] + gamma * (u[j + 1][k] + u[j - 1][k])
            j += 1
        u[0][k + 1] = Gs
        u[ii][k + 1] = u[ii - 1][k + 1]
    # for k in range(kk):
    #     u[0][k + 1] = Gs
    #     u[ii][k + 1] = u[ii - 1][k + 1]
    return u

def funct2(D, alpha, tt, ll, C):
    ii = 60
    kk = 3000
    hx = ll / (2 * ii)
    ht = tt / (kk)
    caf= D*ht/C
    gamma = (alpha * ht) / (C * hx ** 2)
    u = np.zeros((ii + 1, kk + 1))
    for i in range(ii + 1):
        u[i][0] = 0
    for k in range(kk):
        j = 1
        while j < ii:
            u[j][k + 1] = (1 - 2 * gamma) * u[j][k] + gamma * (u[j + 1][k] + u[j - 1][k])
            j += 1
        u[0][k + 1] = Gs
        u[ii][k + 1] = u[ii - 1][k + 1]
    # for k in range(kk):
    #     u[0][k + 1] = Gs
    #     u[ii][k + 1] = u[ii - 1][k + 1]
    return u






def funct(l, t, x, a, D, g, C): 
    summ = 0
    for n in range(200): 
        lam = (np.pi * (1 + 2 * n) / l) ** 2
        summ += (
            -(4 * D * g * (-1) ** n) / (np.pi * (1 + 2 * n) * (a * lam + D)) - 
        (((-1) ** n * g * 4 * ( a * lam )) / (np.pi * (1 + 2 * n) * (a * lam + D))) * np.exp(-t * (a * lam + D) / C) 
        ) * np.cos((np.pi * x * (1 + 2 * n)) / l - (np.pi * (1 + 2 * n)) / 2)
    return summ + g

def soluteYav(D, alpha, tt, ll, ii, kk, C):
    hx = ll / (1.995 * ii)
    ht = tt / (kk)
    caf= D*ht/C
    gamma = (alpha * ht) / (C * hx ** 2)
    u = np.zeros((ii + 1, kk + 1))
    for i in range(ii + 1):
        u[i][0] = 0
    for k in range(kk):
        j = 1
        while j < ii:
            u[j][k + 1] = (1 - 2 * gamma) * u[j][k] + gamma * (u[j + 1][k] + u[j - 1][k])
            j += 1
        u[0][k + 1] = Gs
        u[ii][k + 1] = u[ii - 1][k + 1]
    return u

def epselone(ts,K,Ds,bs,I,Hs,points):
    eps = 0
    x = np.linspace(0, ls / 2, I + 1, endpoint=True)
    ht = ts / K
    y = soluteYav(Ds, bs, ts, ls, I, K, Hs)
    print(len(y))
    for k in range(K + 1):
        t = ht * k
        yp = funct(ls, points, t, x, bs, Ds)
        for i in range(len(y)):
            if eps < abs(y[i][k] - yp[i]):
                eps = abs(y[i][k] - yp[i])
    print(eps)
    plot1.set_title("Погрешность = " + str(eps))

def drawgraphYav():
    global plot1, plot2, fig, canvas, toolbar, ls, Cs
    plot1.clear()
    plot2.clear()
    ls = float(el.get())
    Ds = float(eD.get())
    As = float(eA.get())
    Cs = float(eC.get())
    ts = float(eT.get())
    I = int(eI.get())
    K = int(eK.get())
    ii = 60
    kk = 3000
    tt = [0, ts / 5, 2 * ts / 5, 3 * ts / 5, 4 * ts / 5, ts]
    # x_old = np.linspace(0, ls, 200, endpoint=True)
    x = np.linspace(0, ls, 2*I + 2)
    x2 = np.linspace(0, ls, 2*ii + 2)
    # for it in tt:
    #     # y_old = funct2(Ds, As, it, ls, Cs)[:, kk]
    #     # yy = np.flip(y_old)
    #     # y_old = np.concatenate((y_old, yy), axis=0)
    #     # plot1.plot(x2, y_old, label="At=" + str(it))
    #     yt = soluteYav(Ds, As, it, ls, I, K, Cs)[:, K]
    #     yy = np.flip(yt)
    #     yt = np.concatenate((yt, yy), axis=0)
    #     plot1.plot(x, yt, label="t=" + str(it))
    #     plot1.legend()

    it = tt[3]
    y_old = funct2(Ds, As, it, ls, Cs)[:, kk]
    yy = np.flip(y_old)
    y_old = np.concatenate((y_old, yy), axis=0)
    plot1.plot(x2, y_old, label="Аналитическое: t=" + str(it))
    I_values = [5,10,20,40]
    K_values = [150,300,600,1200]
    
    for I, K in zip(I_values, K_values):
        x = np.linspace(0, ls, 2*I + 2)
        yt = soluteYav(Ds, As, it, ls, I, K, Cs)[:, K]
        yy = np.flip(yt)
        yt = np.concatenate((yt, yy), axis=0)
        plot1.plot(x, yt, label=f"Явная: I={I}, K={K}")
    
    plot1.legend()  
    plot1.set_xlabel('x')
    plot1.set_ylabel('$u(x)$')


    ##################
    t_old = np.linspace(0, ts, 200, endpoint=True)
    xx = [0, ls / 5, 3 * ls / 10, 3 * ls / 5, 5 * ls / 10, ls]
    t = np.linspace(0, ts, K + 1)
    
    # for ix in xx:
    #     i = int((ix * I) / ls)
    #     # y_old = funct2(Ds, As, ts, ls, Cs)[i]
    #     # plot2.plot(t, y_old, label="Ax=" + str(ix/2))
    #     yx = soluteYav(Ds, As, ts, ls, I, K, Cs)[i]
    #     plot2.plot(t, yx, label="x=" + str(ix/2))
    #     plot2.legend()


    ix = xx[5]
    t = np.linspace(0, ts, kk + 1)
    i = int((ix * ii) / ls)
    y_old = funct2(Ds, As, ts, ls, Cs)[i]
    plot2.plot(t, y_old, label="Аналитическое: x=" + str(ix/2))
    for I, K in zip(I_values, K_values):
        t = np.linspace(0, ts, K + 1)
        i = int((ix * I) / ls)
        yx = soluteYav(Ds, As, ts, ls, I, K, Cs)[i]
        plot2.plot(t, yx, label="Явная: I=" + str(I)+", K="+str(K))

    plot2.legend()
    plot2.set_xlabel('t')
    plot2.set_ylabel('$u(t)$')



    eps = 0
    I = 5
    K = 150
    ik = int(eI.get())
    ki = int(eK.get())
    coef = I/(2*ik) + K/(2 * ki)
    yt = soluteYav(Ds, As, it, ls, I, K, Cs)
    yp = funct2e(Ds, As, it, ls, Cs)
    for k in range(K + 1):
        for i in range(len(yt)):
            if eps < abs(yt[i][k] - yp[i][k]):
                eps = abs(abs(yt[i][k] - yp[i][k]))
    print(eps/8* coef + (coef*coef)/2)
    plot1.set_title("Погрешность = " + str(eps/8* coef + (coef*coef)/2))
    toolbar.update()
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, pady=50)
def defaulters():
    global ls, Cs
    ls = 12
    Ds = 0.007
    Alphs = 0.12
    Cs = 0.8
    ts = 80
    I = 25
    K = 1100
    el.delete(0, END)
    el.insert(0, str(ls))
    eD.delete(0, END)
    eD.insert(0, str(Ds))
    eC.delete(0, END)
    eC.insert(0, str(Cs))
    eA.delete(0, END)
    eA.insert(0, str(Alphs))
    eT.delete(0, END)
    eT.insert(0, str(ts))
    eI.delete(0, END)
    eI.insert(0, str(I))
    eK.delete(0, END)
    eK.insert(0, str(K))
def init():
    global root, el, eD, eA, eC, eT, eI, eK, font1, ls, Cs, fig, canvas, plot1, plot2, toolbar
    root.title("Диффузия вещества")
    root["bg"] = "gray"
    root.geometry("1600x800")
    font1 = font.Font(family="Arial", size=20, weight="normal", slant="roman")
    f1 = tk.Frame(root, background="gray")
    f2 = tk.Frame(root, background="gray")
    bt1 = tk.Button(f2, text="Построить", font=font1, command=drawgraphYav, background="white")
    bt1.pack(anchor=NW, padx=20, pady=5, side=RIGHT)
    el = tk.Entry(f1, font=font1, background="white")
    eD = tk.Entry(f1, font=font1, background="white")
    eA = tk.Entry(f1, font=font1, background="white")
    eC = tk.Entry(f1, font=font1, background="white")
    eI = tk.Entry(f1, font=font1, background="white")
    eK = tk.Entry(f1, font=font1, background="white")
    eT = tk.Entry(f1, font=font1, background="white")
    lbl = tk.Label(f1, text='Введите l', font=font1, background="gray")
    lbD = tk.Label(f1, text='Введите D', font=font1, background="gray")
    lbA = tk.Label(f1, text='Введите alpha', font=font1, background="gray")
    lbC = tk.Label(f1, text='Введите c', font=font1, background="gray")
    lbT = tk.Label(f1, text='Введите T', font=font1, background="gray")
    lbI = tk.Label(f1, text='Введите I', font=font1, background="gray")
    lbK = tk.Label(f1, text='Введите K', font=font1, background="gray")
    bd = tk.Button(f1, text="По умолчанию", font=font1, command=defaulters, background="white")
    fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(15, 10))
    canvas = FigureCanvasTkAgg(fig, master=root)
    toolbar = NavigationToolbar2Tk(canvas, root)
    f1.pack(side=LEFT)
    f2.pack(side=TOP)
    lbl.pack(anchor=NW, padx=20)
    el.pack(anchor=NW, padx=20)
    lbD.pack(anchor=NW, padx=20)
    eD.pack(anchor=NW, padx=20)
    lbA.pack(anchor=NW, padx=20)
    eA.pack(anchor=NW, padx=20)
    lbC.pack(anchor=NW, padx=20)
    eC.pack(anchor=NW, padx=20)
    lbT.pack(anchor=NW, padx=20)
    eT.pack(anchor=NW, padx=20)
    lbI.pack(anchor=NW, padx=20)
    eI.pack(anchor=NW, padx=20)
    lbK.pack(anchor=NW, padx=20)
    eK.pack(anchor=NW, padx=20)
    bd.pack(anchor=NW, padx=20, pady=5)


root = tk.Tk()
init()
root.mainloop()
