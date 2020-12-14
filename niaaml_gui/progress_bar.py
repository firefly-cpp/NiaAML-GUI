from PyQt5 import QtCore
from PyQt5.QtWidgets import QProgressBar

class ProgressBar(QProgressBar):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.setTextVisible(True)
        self.setMaximum(100)
        self.setAlignment(QtCore.Qt.AlignCenter)