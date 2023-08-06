import matplotlib.pyplot as plt
import mpl_scatter_density, numpy

class RootPlotter():
    left, width = 0.1, 0.60
    bottom, height = 0.1, 0.60
    bottom_h = left_h = left + width + 0.02

    def __init__(self, fig_size: tuple) -> None:
        self.cmap = plt.get_cmap("white_turbo")
        rect_scatter = [self.left, self.bottom, self.width, self.height]
        rect_color = [self.left_h + 0.19, self.bottom, 0.02, self.height]
        rect_histx = [self.left, self.bottom_h, self.width, 0.17]
        rect_histy = [self.left_h, self.bottom, 0.17, self.height]
        
        self.figure = plt.figure(1, figsize=fig_size)
        self.axScatter = self.figure.add_axes(rect_scatter,projection="scatter_density")
        self.axHistx = self.figure.add_axes(rect_histx)
        self.axHisty = self.figure.add_axes(rect_histy)
        self.axColor = self.figure.add_axes(rect_color)

    def select_cmap(self, cmap_name: str) -> None:
        self.cmap = plt.get_cmap(cmap_name)

    def plot(self, data_x, data_y, bins) -> None:
        density = self.axScatter.scatter_density(data_x, data_y, self.cmap)
        self.axScatter.sharex(self.axHistx)
        self.axScatter.sharey(self.axHisty)

        self.figure.colorbar(density, self.axColor, label="Points per pixel")

        hist = numpy.histogram(data_x, bins)
        self.axHistx.plot(hist[1][1:],hist[0],drawstyle="steps-mid")
        self.axHistx.set_ylim(0, max(hist[0][10:]))

        hist = numpy.histogram(data_y, bins)
        self.axHisty.plot(hist[1][1:],hist[0],drawstyle="steps-mid")
        self.axHisty.set_xlim(0,max(hist[0][10:]))

        plt.setp(self.axHistx.get_xticklabels(), visible=False)
        plt.setp(self.axHisty.get_yticklabels(), visible=False)

        self.axScatter.set_xlabel("Start Energy")
        self.axScatter.set_ylabel("Stop Energy")

        self.axHistx.set_ylabel("Energy counts")
        self.axHisty.set_xlabel("Energy counts")

        self.axScatter.set_xlim(0,bins)
        self.axScatter.set_ylim(0,bins)       

    def show(self):
        plt.show(block=True)

    pass