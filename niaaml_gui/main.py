import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QFrame, QSizePolicy, QTabWidget
from PyQt5.QtCore import QSize

class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle('NiaAML - GUI')

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        hBoxLayout = QHBoxLayout(self)
        exploreBox = self.getBox((0, 0, 0, 0), False)
        tabs = QTabWidget(self)
        tabs.addTab(QWidget(self), 'Feature Selection Algorithms')
        tabs.addTab(QWidget(self), 'Feature Transformation Algorithms')
        tabs.addTab(QWidget(self), 'Classifiers')
        font = tabs.font()
        font.setPointSize(10)
        tabs.setFont(font)
        tabs.setStyleSheet("QTabBar::tab { height: 40px; }")
        exploreBox.addWidget(tabs)
        hBoxLayout.addItem(exploreBox)

        vBoxLayout = QVBoxLayout(self)
        vBoxLayout.setContentsMargins(0, 34, 0, 0)
        fsasBox = self.getBox((0, 5, 5, 3), True)
        ftasBox = self.getBox((0, 3, 5, 3), True)
        classifiers = self.getBox((0, 3, 5, 5), True)
        vBoxLayout.addItem(fsasBox)
        vBoxLayout.addItem(ftasBox)
        vBoxLayout.addItem(classifiers)

        hBoxLayout.addItem(vBoxLayout)
        hBoxLayout.setStretchFactor(exploreBox, 1)
        hBoxLayout.setStretchFactor(vBoxLayout, 2)

        gridLayout.addLayout(hBoxLayout, 0, 0)

        centralWidget.setLayout(gridLayout)

    def getBox(self, tupleMargins, visibleBorder):
        l = QGridLayout()
        l.setContentsMargins(*tupleMargins)
        f = QFrame(self)
        f.setFrameShape(QFrame.Box)
        b = 'border: 1px solid #d8d8d8;' if visibleBorder is True else 'border: 0px;'
        f.setStyleSheet('background-color: #fff; {border}'.format(border=b))
        l.addWidget(f, 0, 0)
        return l

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())