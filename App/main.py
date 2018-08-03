import prueba
import functions
import numpy as np
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *
import tkinter as tk
from tkinter import ttk, font
plt.use("TkAgg")


class Aplicacion:
    def __init__(self):
        self.raiz = Tk()
        fuente = font.Font(weight='bold')
        self.raiz.configure(bg='beige')
        self.raiz.title('Aplicación')
        
        self.entry1 = ttk.Label(self.raiz, text="Precio:", font=fuente)
        self.entry2 = ttk.Label(self.raiz, text="Tasa libre de riesgo", font=fuente)
        self.entry3 = ttk.Label(self.raiz, text="Simbolo de la empresa", font=fuente)
        self.entry4 = ttk.Label(self.raiz, text="Tiempo de ejercicio (meses)", font=fuente)
        self.price = DoubleVar(value=0)
        self.riskfree = DoubleVar(value=0)
        self.symbol = StringVar()
        self.estimate = DoubleVar(value=0)
        self.rangetime = IntVar()
        self.ctext1 = ttk.Entry(self.raiz, textvariable=self.price, width=30)
        self.ctext2 = ttk.Entry(self.raiz, textvariable=self.riskfree, width=30)
        self.ctext3 = ttk.Entry(self.raiz, textvariable=self.symbol, width=30)
        self.ctext4 = ttk.Entry(self.raiz, textvariable=self.rangetime, width=30)
        self.separ1 = ttk.Separator(self.raiz, orient=HORIZONTAL)
        self.button1 = ttk.Button(self.raiz, text='Salir', command=quit)
        self.button2 = ttk.Button(self.raiz, text='Calcular', command=self.mainbutton)
        self.estimate_value = ttk.Label(self.raiz, text="Valor Estimado: ", font=fuente)
        self.estimate_gain = ttk.Label(self.raiz, text='Ganancia Estimada: ', font=fuente)

        self.entry1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctext1.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.entry2.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctext2.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.entry3.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctext3.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.entry4.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctext4.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.estimate_value.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.estimate_gain.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.button2.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        self.button1.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        self.ctext1.focus_set()
        self.raiz.mainloop()
    
    def mainbutton(self, *args):
        prueba.download_quotes(self.symbol.get(), self.rangetime.get())
        df = functions.icsv('csv/' + self.symbol.get() + '.csv')
        volatility = functions.volatility(df)
        y_axis, St_pre, Sf_fin = functions.iterations(10, 5000, float(self.price.get()), float(self.riskfree.get()),
                                                      volatility, self.rangetime.get())
        size_interval = (self.rangetime.get()/12)/5000
        x_axis = np.linspace(size_interval, self.rangetime.get()/12, 5000)
        self.estimate_gain.config(text='Ganancia estimada: ' +
                                       str(np.exp(-self.riskfree.get()*self.rangetime.get()/12*St_pre)))
        self.estimate_value.config(text='Valor estimado: ' + str(Sf_fin))
        self.board = Toplevel()

        f = Figure(figsize=(8, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(x_axis, y_axis, color='green')

        canvas = FigureCanvasTkAgg(f, self.board)
        canvas.draw()
        canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self.board)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

        print('Terminado!')


def main():
    miview = Aplicacion()
    return 0


if __name__ == '__main__':
    main()