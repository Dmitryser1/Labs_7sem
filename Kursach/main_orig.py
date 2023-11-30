import tkinter as tk
from tkinter import *
from tkinter import font

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy import optimize


def f(x):
    return np.tan(x) - ls * Hs / (2 * x)
def df(x):
    return 1 / np.cos(x) ** 2 + ls * Hs / (2 * x ** 2)
def get_lam(l):
    points = []
    for i in range(100):
        k = np.pi * i + 0.1
        points.append(optimize.root_scalar(f, fprime=df, x0=k, method="newton").root * 2 / l)
    return points
def funct(l, points, t, x, b, D):
    summ = 0
    for lam in points:
        summ += (-32 * np.pi ** 2 * np.sin(l * lam / 2)) / (lam * (lam ** 2 * l ** 2 - 4 * np.pi ** 2) * (
                (np.sin(l * lam)) / (2 * lam) + l / 2)) * np.exp(
            t * (b - lam ** 2 * D)) * np.cos(lam * (x - l / 2))
    return summ
def psi(i, hx, l):
    return 8 * np.sin(np.pi * i * hx / l) ** 2

def soluteYav(D, beta, tt, ll, ii, kk, H):
    hx = ll / (ii * 2)
    ht = tt / kk
    ksi = (D * ht) / (hx ** 2)
    eta = beta * ht
    u = np.zeros((ii + 1, kk + 1))
    for i in range(ii + 1):
        u[i][0] = psi(i, hx, ll)
    for k in range(kk):
        j = 1
        while j < ii:
            u[j][k + 1] = (1 - 2 * ksi + eta) * u[j][k] + ksi * (u[j + 1][k] + u[j - 1][k])
            j += 1
        u[0][k + 1] = u[1][k + 1] / (1 + hx * H)
        u[ii][k + 1] = u[ii - 1][k + 1]
    return u

def drawgraphYav():
    global plot1, plot2, fig, canvas, toolbar, ls, Hs
    plot1.clear()
    plot2.clear()
    ls = float(el.get())
    Ds = float(eD.get())
    bs = float(eb.get())
    Hs = float(eH.get())
    ts = float(eT.get())
    I = int(eI.get())
    K = int(eK.get())
    points = get_lam(ls)
    tt = [0, ts / 5, 2 * ts / 5, 3 * ts / 5, 4 * ts / 5, ts]
    x_old = np.linspace(0, ls / 2, 100, endpoint=True)
    # for it in tt:
    #     y_old = funct(ls, points, it, x_old, bs, Ds)
    #     plot1.plot(x_old, y_old, label="t=" + str(it))
    #     yt = soluteYav(Ds, bs, it, ls, I, K, Hs)[:, K]
    #     plot1.plot(x, yt, label="t=" + str(it))
    #     plot1.plot(x, yt, label="t=" + str(it) + " без Рунге")
    #     yt2 = soluteRunge(Ds, bs, it, ls, I, K, Hs)[:, K]
    #     plot1.plot(x, yt2, label="t=" + str(it) + " с Рунге")
    #     plot1.legend()
    it = tt[2]
    y_old = funct(ls, points, it, x_old, bs, Ds)
    plot1.plot(x_old, y_old, label="Аналитическое: t=" + str(it))
    I = 10
    K = 1000
    x = np.linspace(0, ls / 2, I + 1)
    yt = soluteYav(Ds, bs, it, ls, I, K, Hs)[:, K]
    plot1.plot(x, yt, label="Явная: I=" + str(I)+", K="+str(K))
    I = 10
    K = 2000
    x = np.linspace(0, ls / 2, I + 1)
    yt = soluteYav(Ds, bs, it, ls, I, K, Hs)[:, K]
    plot1.plot(x, yt, label="Явная: I=" + str(I)+", K="+str(K))
    # yt2 = soluteRunge(Ds, bs, it, ls, I, K, Hs)[:, K]
    # plot1.plot(x, yt2, label="t=" + str(it) + " с Рунге")
    # yt3 = soluteYav1(Ds, bs, it, ls, I, K, Hs)[:, K]
    # plot1.plot(x, yt3, label="t=" + str(it) + " с Рунге2")
    plot1.legend()
    plot1.set_xlabel('x')
    plot1.set_ylabel('$u(x)$')
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
    xx = [1 / 2, ls / 10, 3 * ls / 20, 3 * ls / 10, 5 * ls / 20, ls / 2]
    t_old = np.linspace(0, ts, 200, endpoint=True)
    ix = xx[5]
    y_o = funct(ls, points, t_old, ix, bs, Ds)
    plot2.plot(t_old, y_o, label="Аналитическое: x=" + str(ix))
    I=10
    K=2000
    t = np.linspace(0, ts, K + 1)
    i = int((2 * ix * I) / ls)
    yx = soluteYav(Ds, bs, ts, ls, I, K, Hs)[i]
    plot2.plot(t, yx, label="Явная: I=" + str(I)+", K="+str(K))
    I=10
    K=2000
    t = np.linspace(0, ts, K + 1)
    i = int((2 * ix * I) / ls)
    yx = soluteYav(Ds, bs, ts, ls, I, K, Hs)[i]
    plot2.plot(t, yx, label="Явная: I=" + str(I)+", K="+str(K))
    plot2.legend()
    plot2.set_xlabel('t')
    plot2.set_ylabel('$u(t)$')
    toolbar.update()
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, pady=50)
def defaulters():
    global ls, Hs
    ls = 12
    Ds = 0.085
    bs = 0.001
    Hs = 0.004
    ts = 250
    I = 25
    K = 1100
    el.delete(0, END)
    el.insert(0, str(ls))
    eD.delete(0, END)
    eD.insert(0, str(Ds))
    eH.delete(0, END)
    eH.insert(0, str(Hs))
    eb.delete(0, END)
    eb.insert(0, str(bs))
    eT.delete(0, END)
    eT.insert(0, str(ts))
    eI.delete(0, END)
    eI.insert(0, str(I))
    eK.delete(0, END)
    eK.insert(0, str(K))
def init():
    global root, el, eD, eb, eH, eT, eI, eK, font1, ls, Hs, fig, canvas, plot1, plot2, toolbar
    root.title("Диффузия вещества")
    root["bg"] = "powderblue"
    root.geometry("1600x800")
    font1 = font.Font(family="Arial", size=20, weight="normal", slant="roman")
    f1 = tk.Frame(root, background="powderblue")
    f2 = tk.Frame(root, background="powderblue")
    bt1 = tk.Button(f2, text="Явная", font=font1, command=drawgraphYav, background="mintcream")
    bt1.pack(anchor=NW, padx=20, pady=5, side=RIGHT)
    el = tk.Entry(f1, font=font1, background="mintcream")
    eD = tk.Entry(f1, font=font1, background="mintcream")
    eb = tk.Entry(f1, font=font1, background="mintcream")
    eH = tk.Entry(f1, font=font1, background="mintcream")
    eI = tk.Entry(f1, font=font1, background="mintcream")
    eK = tk.Entry(f1, font=font1, background="mintcream")
    eT = tk.Entry(f1, font=font1, background="mintcream")
    lbl = tk.Label(f1, text='Введите l', font=font1, background="powderblue")
    lbD = tk.Label(f1, text='Введите D', font=font1, background="powderblue")
    lbb = tk.Label(f1, text='Введите b', font=font1, background="powderblue")
    lbH = tk.Label(f1, text='Введите H', font=font1, background="powderblue")
    lbT = tk.Label(f1, text='Введите T', font=font1, background="powderblue")
    lbI = tk.Label(f1, text='Введите I', font=font1, background="powderblue")
    lbK = tk.Label(f1, text='Введите K', font=font1, background="powderblue")
    bd = tk.Button(f1, text="По умолчанию", font=font1, command=defaulters, background="mintcream")
    fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(15, 10))
    canvas = FigureCanvasTkAgg(fig, master=root)
    toolbar = NavigationToolbar2Tk(canvas, root)
    f1.pack(side=LEFT)
    f2.pack(side=TOP)
    lbl.pack(anchor=NW, padx=20)
    el.pack(anchor=NW, padx=20)
    lbD.pack(anchor=NW, padx=20)
    eD.pack(anchor=NW, padx=20)
    lbb.pack(anchor=NW, padx=20)
    eb.pack(anchor=NW, padx=20)
    lbH.pack(anchor=NW, padx=20)
    eH.pack(anchor=NW, padx=20)
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
