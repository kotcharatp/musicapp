__author__ = 'hibiki'

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

from Cores import core


class FrequencyWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(FrequencyWidget, self).__init__()

        self.parent = parent
        self.init_widget()

    def init_widget(self):

        # create root layout
        root = QtGui.QVBoxLayout()

        # create hboxes for grouping
        slider_group = QtGui.QHBoxLayout()

        # create slider
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setFocusPolicy(QtCore.Qt.NoFocus)
        slider.setGeometry(30, 40, 100, 30)
        slider.setRange(0, 50)

        # set the value Changed Handler
        slider.valueChanged[int].connect(self.handle_slider_change)

        # set the global Graph background and foreground as Black,White
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # create plot area
        self.plot_widget = pg.PlotWidget()

        # create label
        self.label = QtGui.QLabel('0', self)

        # add slider and label into group
        slider_group.addWidget(slider)
        slider_group.addWidget(self.label)

        # add slider and plot area into ROOT
        root.addWidget(self.plot_widget)
        root.addLayout(slider_group)

        # set layout
        self.setLayout(root)

    def plot(self, x, y, pen='r', clear=True):
        self.plot_widget.plot(x, y, pen=pen, clear=clear)

    # declare a handler to change label according to the value from slider
    def handle_slider_change(self, value):

        # get parent shares as shares
        shares = self.parent.shares

        # update current value
        self.label.setText(str(value))
        shares['deg_freq'] = value

        # recalculate values
        shares['all'] = core.smooth(shares['original'], shares['deg_freq'], shares['deg_amp'])

        # update values in each component
        shares['time'] = shares['all'][:, 0]
        shares['freq'] = shares['all'][:, 1]
        shares['amp'] = shares['all'][:, 2]

        # update plot
        self.parent.freq_widget.plot(self.parent.shares['time'], self.parent.shares['original'][:, 1])
        self.parent.freq_widget.plot(shares['time'], shares['freq'], pen='b', clear=False)
