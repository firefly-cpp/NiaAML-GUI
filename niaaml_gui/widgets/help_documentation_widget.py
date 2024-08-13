from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTextBrowser, QLabel, QVBoxLayout, QPushButton, QSizePolicy
import webbrowser

from niaaml_gui.widgets.base_main_widget import BaseMainWidget


class HelpDocumentationWidget(BaseMainWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        vBoxLayout = QVBoxLayout(self._parent)
        vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        documentation_label = QLabel("Documentation:")
        font = QFont()
        font.setPointSize(20)
        documentation_label.setFont(font)

        vBoxLayout.addWidget(documentation_label)

        button = QPushButton('Open documentation')
        button.clicked.connect(self.open_link)

        button_font = QFont()
        button_font.setPointSize(12)

        button.setFont(button_font)

        vBoxLayout.addWidget(button)

        self.setLayout(vBoxLayout)

    def open_link(self):
        # Define the URL you want to open
        url = 'https://github.com/firefly-cpp/NiaAML-GUI/blob/master/README.md'

        # Open the URL in the default web browser
        webbrowser.open(url)
