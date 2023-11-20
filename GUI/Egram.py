
import numpy as np
from scipy.interpolate import make_interp_spline

class Egram:
    def __init__(self):
        self.data_points = []  # Array to store (x, y) pairs
        self.generate_ekg_data(50)  # Initially fill with 50 data points
        self.current_index = 0

    def createEgram(self, window):
        # Extract and sort (x, y) pairs based on x values
        sorted_data = sorted(self.data_points, key=lambda pair: pair[0])
        x, y = zip(*sorted_data)  # Unpack sorted (x, y) pairs

        x = np.array(x)
        y = np.array(y)
        x_scaled = (x - min(x)) / (max(x) - min(x)) * window.winfo_width()
        y_scaled = (y - min(y)) / (max(y) - min(y)) * window.winfo_height()
        y_scaled = window.winfo_height() - y_scaled

        # Remove duplicates
        unique_x, unique_y = np.unique(x_scaled, return_index=True)
        y_scaled_unique = y_scaled[unique_y]

        x_smooth = np.linspace(unique_x.min(), unique_x.max(), 100)
        spline = make_interp_spline(unique_x, y_scaled_unique, k=3)  # Degree of smoothing
        y_smooth = spline(x_smooth)

        # Draw lines
        for i in range(len(x_smooth) - 1):
            window.create_line(x_smooth[i], y_smooth[i], x_smooth[i + 1], y_smooth[i + 1], fill='blue')



    def generate_ekg_data(self, num_points):
        new_x = np.linspace(0, 4*np.pi, num_points)
        new_y = np.sin(new_x) + np.random.normal(0, 0.1, num_points)  # Simulated ECG with noise

        for x, y in zip(new_x, new_y):
            self.data_points.append((x, y))
            if len(self.data_points) > 100:
                self.data_points.pop(0)  # Keep array length at 50

    def updateEgram(self, window, num_new_points=5):
        window.delete("all")  # Clear existing graph
        self.generate_ekg_data(num_new_points)  # Generate and add new data points
        self.createEgram(window)
        window.after(100, lambda: self.updateEgram(window, num_new_points))
