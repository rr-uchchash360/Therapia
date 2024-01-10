# ================================ Responsible for plotting graph =======================================


# ================================LIBRARY IMPORT BLOCK STARTS============================================

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.backends
import matplotlib.backend_bases
import matplotlib.backend_managers
import matplotlib.backend_tools

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


# ================================CLASS BLOCK STARTS=====================================================

# ***Define the class.***
class CanvasGraph(FC):

    # ================================CLASS INITIALIZATION BLOCK=========================================

    # **Define routine to initialize an instance.**
    def __init__(self, parent=None, three=True, width_=5, height_=3, dpi_=95):

        self.fig = plt.figure(figsize=(width_, height_), dpi=dpi_, facecolor='#f9f9f0', frameon=True)  # define figure

        # check if main or result generation graph is being set
        if three:
            # 3D axis
            self.ax = plt.subplot2grid((5, 1), (0, 0), projection='3d', rowspan=5, colspan=1, facecolor='#f9f9f0')  # define 3D axis
            self.ax.axis('off')  # disable axis properties
            plt.subplots_adjust(left=0, right=1.01, top=1.02, bottom=0)

        FC.__init__(self, self.fig)  # initialize canvas
        self.setParent(parent)  # set parent

        self.fig.canvas.move(0, 0)  # move the canvas to the desired co-ordinates
