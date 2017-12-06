"""

The aim of this code is to make interactive stacked plots of the data by dragging plots up and down as needed
The code can be modified for any transformation, but our application involves lining up data on top of one another
TODO: Fix bug where the data can get lost when more than one plot is graphed. Need to retain data for each plot individually
TODO: Also fix inconsistency in selecting graphs
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class DraggablePlot:
    lock = None

    def __init__(self,lineplot):
        self.lineplot = lineplot
        self.press = None
        self.xdata= None
        self.ydata = None
        self.picked_plot = None
        self.released_plot = None

    def connect(self):
        # print('connect')
        self.cidpick = self.lineplot.figure.canvas.mpl_connect('pick_event', self.on_pick)
        # self.cidpress = self.lineplot.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.lineplot.figure.canvas.mpl_connect('button_release_event', self.on_release)
    def on_pick(self,event):
        # print('onpress')
        self.picked_plot = event.mouseevent.ydata
        # print('mouseevent1')
        # print(str(self.picked_plot))
        # print('hi mouseevent1')
        thisline = event.artist
        self.xdata = thisline.get_xdata()
        self.ydata = thisline.get_ydata()
        # self.press = self.on_press()
        # ind = event.ind
        # points = tuple(zip(self.xdata[ind], self.ydata[ind]))
        # print('onpick points:', points)
    #
    # def on_press(self,event):
    #     ycoords_press = event.ydata
    #     print('hi_press')
    #     print(str(ycoords_press))
    #     print('hi press')
    #     # mouseevent = event.mouseevent.ydata
    #     # blah = self.on_pick(ycoords_press)

        # return

    def on_release(self, event):
        self.released_plot = event.ydata
        # print('hi_release')
        # print(str(self.released_plot))
        # print('hi_release')
        if self.picked_plot is not None and self.released_plot is not None:
            deltay = self.released_plot - self.picked_plot
            self.lineplot.set_ydata(self.ydata + deltay)
            # self.ydata = self.ydata + deltay
            ax.relim()
            ax.autoscale_view()
            self.lineplot.figure.canvas.draw()

            self.picked_plot = None
    #     return ycoords_release
        # print('onrelease_begin')
        # if event.inaxes:
        #     ydat = event.ydata
        #     deltay = self.press - ydat
        #     print('delta y is '+str(deltay))
        #     self.lineplot.figure.canvas.draw()
        #     print('onrelease')
        # else:
        #     print('you clicked outside the axes\n')


    def disconnect(self):
        # print('disconnect')
        self.lineplot.figure.canvas.mpl_disconnect(self.cidpick)
        # self.lineplot.figure.canvas.mpl_disconnect(self.cidpress)
        self.lineplot.figure.canvas.mpl_disconnect(self.cidrelease)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on points')

# np.random.seed(1)
# x = np.random.rand(10)
# y = np.random.rand(10)
x = np.arange(-1,10,1)
y = 2*x+6
y2 = -5*x-2

lines = ax.plot(x, y, x, y2, picker=5)# 5 points tolerance

lines_cat = [] #need to figure out if i need this

for lineobj in lines:
    draglines = DraggablePlot(lineobj)
    draglines.connect()
    lines_cat.append(draglines)

plt.show()