__author__ = 'hibiki'
#Test
import sys
from PyQt4 import QtGui

from Widgets.frequency import FrequencyWidget
from Widgets.amplitude import AmplitudeWidget
from Widgets.mainmenu import MainMenuWidget


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.shares = {}
        self.init_ui()

    def init_ui(self):

        self.shares['deg_freq'] = 0
        self.shares['deg_amp'] = 0

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Music App Project')

        # set up layouts and customize their properties
        root = QtGui.QVBoxLayout()

        # create hbox to wrap graph amp and freq widgets
        upper_hbox = QtGui.QHBoxLayout()
        lower_hbox = QtGui.QHBoxLayout()

        # create all the widgets
        self.freq_widget = FrequencyWidget(self)
        self.amp_widget = AmplitudeWidget(self)
        self.menu_widget = MainMenuWidget(self)

        # add freq and amp widget into upper_hbox
        upper_hbox.addWidget(self.freq_widget)
        upper_hbox.addWidget(self.amp_widget)

        # add main menu into lower hbox
        lower_hbox.addWidget(self.menu_widget)

        # add widget into root
        root.addLayout(upper_hbox)
        root.addLayout(lower_hbox)

        # set box as layout
        self.setLayout(root)

        self.show()

    def register_handler(self, name, handler):
        self.handlers[name] = handler


def main():
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
