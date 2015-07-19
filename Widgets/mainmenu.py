__author__ = 'hibiki'


__author__ = 'hibiki'

from PyQt4 import QtGui
from Cores import core, utils
import numpy as np
import shutil


class MainMenuWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(MainMenuWidget, self).__init__()
        self.parent = parent
        self.init_widget()

    def init_widget(self):

        # create root layout
        root = QtGui.QHBoxLayout()

        # create button
        load_btn = QtGui.QPushButton('Load Music')
        export_btn = QtGui.QPushButton('Export')

        # add event handler
        load_btn.clicked.connect(self.handle_load_btn)
        export_btn.clicked.connect(self.handle_export_btn)

        # add slider and plot area into ROOT
        root.addWidget(load_btn)
        root.addWidget(export_btn)

        # set layout
        self.setLayout(root)

    def handle_load_btn(self):
        # open file dialog
        filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open music', '', '.wav file (*.wav)')
        # save source path
        self.parent.shares['source'] = filename

        # extract amplitude and frequency
        utils.extract_amplitude(filename, 'share/amp.csv')
        utils.extract_frequency(filename, 'share/freq.csv')

        # extract duration of this music
        self.parent.shares['duration'] = utils.extract_duration()

        # prepare values for later operations
        prepared_values = core.prepare('share/freq.csv', 'share/amp.csv')
        self.parent.shares['original'] = prepared_values
        self.parent.shares['all'] = prepared_values

        # extract components
        self.parent.shares['time'] = prepared_values[:, 0]
        self.parent.shares['freq'] = prepared_values[:, 1]
        self.parent.shares['amp'] = prepared_values[:, 2]

        # plot both of them on the graph
        self.parent.freq_widget.plot(self.parent.shares['time'], self.parent.shares['freq'])
        self.parent.amp_widget.plot(self.parent.shares['time'], self.parent.shares['amp'])

    def handle_export_btn(self):
        alls = np.zeros((len(self.parent.shares['time']), 3))
        alls[:, 0] = self.parent.shares['time']
        alls[:, 1] = self.parent.shares['freq']
        alls[:, 2] = self.parent.shares['amp']

        # export dataset.js for viewing in the web
        core.export(alls)

        # copy source wave file and overwrite in output www-source
        shutil.copy2(self.parent.shares['source'], 'www-source/music.wav')

        # overwrite inject.js with proper value of music_duration
        with open('www-source/inject.js', 'w') as inject:
            inject.write('var music_duration = ')
            inject.write(str(self.parent.shares['duration']))

        QtGui.QMessageBox.information(self.parent, 'Export',
                                      "Successfully Exported. Please check dataset.json in www-source",
                                      QtGui.QMessageBox.Ok)



