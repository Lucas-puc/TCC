################################################ ##
### Real time data plotter in opencv (python)   ###
## Plot multiple data for debugging and analysis ##
## Contributors - Vinay @ www.connect.vin        ##
## For more details, check www.github.com/2vin   ##
###################################################

import cv2 as cv
import numpy as np
import time

# Plot values in opencv program
class Plotter:
    def __init__(self, plot_width, plot_height, num_plot_values):
        self.width = plot_width
        self.height = plot_height
        self.color_list = [(0, 0, 255), (0, 250, 0), (255, 0, 0), (0, 255, 250), (250, 0, 250), (250, 250, 0),
                            (200, 100, 200), (100, 200, 200), (200, 200, 100)]
        self.color = []
        self.val = []
        # self.plot = np.ones((self.height, self.width, 3))*255
        self.plot = cv.imread("Graph_bg.png")

        for i in range(num_plot_values):
            self.color.append(self.color_list[i])

    # Update new values in plot
    def multiplot(self, val, label="Erros ao Centro"):
        self.val.append(val)
        while len(self.val) > self.width:
            self.val.pop(0)

        self.show_plot(label)

    # Show plot using opencv imshow
    def show_plot(self, label):
        # self.plot = np.zeros((self.height, self.width, 3))*255
        self.plot = cv.imread("Graph_bg.png")
        for i in range(len(self.val)-1):
            for j in range(len(self.val[0])):
                cv.line(self.plot, (i, int(self.height/2) - self.val[i][j]), (i+1, int(self.height/2) - self.val[i+1][j]), self.color[j], 1)
        cv.imshow(label, self.plot)
        cv.waitKey(1)
