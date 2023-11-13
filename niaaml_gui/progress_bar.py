from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.setTextVisible(True)
        self.setMaximum(100)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
