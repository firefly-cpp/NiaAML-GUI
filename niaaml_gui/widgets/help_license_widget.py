from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton
import webbrowser

from niaaml_gui.widgets.base_main_widget import BaseMainWidget


class HelpLicenseWidget(BaseMainWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        vBoxLayout = QVBoxLayout(self._parent)
        vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        license_title = QLabel("License")
        font = QFont()
        font.setPointSize(20)
        license_title.setFont(font)

        vBoxLayout.addWidget(license_title)

        contentFont = QFont()
        contentFont.setPointSize(12)

        license_content = QLabel("This package is distributed under the MIT License. "
                                    "This license can be found online at http://www.opensource.org/licenses/MIT.")
        license_content.setFont(contentFont)
        license_content.setStyleSheet("""
            QLabel {
                padding-bottom: 12px;
            }
        """)

        button = QPushButton('Open license')
        button.clicked.connect(self.open_license_link)
        button.setFont(contentFont)

        vBoxLayout.addWidget(license_content)
        vBoxLayout.addWidget(button)

        self.setLayout(vBoxLayout)

    def open_license_link(self):
        # Define the URL you want to open
        url = 'http://www.opensource.org/licenses/MIT'

        # Open the URL in the default web browser
        webbrowser.open(url)
