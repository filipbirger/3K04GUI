import tkinter as tk
import struct
import serial
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from threading import Thread
import time
import SerialComm
class Egram:
    def __init__(self,serialComm):
        self.comm = serialComm
        self.startTime = time.time()



   
    def update_plot(self, frame):
        current_time = (time.time() - self.startTime) * 1500
        x_data = [current_time - i*1500 for i in range(len(self.comm.egramList))]
        y_data_atr = [pair[0] for pair in self.comm.egramList]
        y_data_vent = [pair[1] for pair in self.comm.egramList] 

       
        self.line_atr.set_data(x_data, y_data_atr)
        self.line_vent.set_data(x_data, y_data_vent)

        #self.line_atr.set_linestyle('')  
        #self.line_vent.set_linestyle('')
        #self.line_atr.set_marker('o')  
        #self.line_vent.set_marker('o')

        return self.line_atr, self.line_vent

    def run(self,window):
        self.root = tk.Toplevel(window)
        self.root.title("Egram Viewer")
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.line_atr, = self.ax.plot([], [], lw=2, label='ATR Signal')
        self.line_vent, = self.ax.plot([], [], lw=2, label='VENT Signal')
        self.ax.legend()
        self.ax.set_xlim(0, 10000)
        self.ax.set_ylim(-5000, 5000)
        self.ax.set_xlabel('Time (ms)')
        self.ax.set_ylabel('Signal')

   
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)


        Thread(target=self.read_data_continuously).start()
    

        self.ani = animation.FuncAnimation(self.fig, self.update_plot, blit=True)

        self.root.mainloop()

    def read_data_continuously(self):
        while True:
            self.comm.readIn()
            time.sleep(1)  

