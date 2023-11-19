
import numpy as np
from scipy.interpolate import make_interp_spline

class Egram:
    def __init__(self):
        self.full_x, self.full_y = self.generate_ekg_data(1000)
        self.current_index = 0


    def createEgram(self,window,x,y):
        x = np.array(x)
        y = np.array(y)
        x_scaled = (x - min(x)) / (max(x) - min(x)) * window.winfo_width()
        y_scaled = (y - min(y)) / (max(y) - min(y)) * window.winfo_height()
        y_scaled = window.winfo_height() - y_scaled

        x_smooth = np.linspace(x_scaled.min(), x_scaled.max(), 300)
        spline = make_interp_spline(x_scaled, y_scaled, k=3)  # k is the degree of smoothing
        y_smooth = spline(x_smooth)

        # Draw lines
        for i in range(len(x_smooth) - 1):
            window.create_line(x_smooth[i], y_smooth[i], x_smooth[i + 1], y_smooth[i + 1], fill='blue')
    
    def generate_ekg_data(self,num_points):
        self.x = np.linspace(0, 4*np.pi, num_points)
        self.y = np.sin(self.x) + np.random.normal(0, 0.1, num_points)  # Adding a bit of noise
        return self.x, self.y
    
    def updateEgram(self, window, num_points=100):
        window.delete("all")  # Clear existing graph
        end_index = self.current_index + num_points
        if end_index > len(self.full_x):
            end_index = len(self.full_x)
            self.current_index = 0  # Reset to loop the signal

        x = self.full_x[self.current_index:end_index]
        y = self.full_y[self.current_index:end_index]

        self.createEgram(window, x, y)
        self.current_index += 10  # Move the window for the next update

        window.after(100, lambda: self.updateEgram(window, num_points)) 