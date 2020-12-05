from PyQt5 import QtCore
from PyQt5.QtWidgets import QProgressBar

class ProgressBar(QProgressBar):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.setMaximum(0)
        self.setTextVisible(False)
        self.setAlignment(QtCore.Qt.AlignCenter)