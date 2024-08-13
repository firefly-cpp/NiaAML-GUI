from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSpacerItem

from niaaml_gui.widgets.base_main_widget import BaseMainWidget


class HelpAuthorsWidget(BaseMainWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        vBoxLayout = QVBoxLayout(self._parent)
        vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        maintainers_title = QLabel("Maintainers")
        font = QFont()
        font.setPointSize(20)
        maintainers_title.setFont(font)

        vBoxLayout.addWidget(maintainers_title)

        contentFont = QFont()
        contentFont.setPointSize(12)

        maintainers_content = QLabel()
        maintainers_content.setText("""
            <html>
                <ul>
                    <li>Iztok Fister, Jr. @firefly-cpp</li>
                </ul>
            </html>
        """)
        maintainers_content.setFont(contentFont)

        maintainers_content.setStyleSheet("""
            QLabel {
                padding-bottom: 12px;
            }
        """)

        vBoxLayout.addWidget(maintainers_content)

        contributors_title = QLabel("Contributors (in alphabetical order by surname)")
        font = QFont()
        font.setPointSize(20)
        contributors_title.setFont(font)

        vBoxLayout.addWidget(contributors_title)

        contributors_content = QLabel()
        contributors_content.setText("""
            <html>
                <ul>
                    <li>Ben Beasley @musicinmybrain</li>
                    <li>Zala Lahovnik @zala-lahovnik</li>
                    <li>Luka Pečnik @lukapecnik</li>
                    <li>Žiga Stupan @zStupan</li>
                </ul>
            </html>
        """)
        contributors_content.setFont(contentFont)

        vBoxLayout.addWidget(contributors_content)

        self.setLayout(vBoxLayout)
