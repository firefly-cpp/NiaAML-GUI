import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QComboBox, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QFrame, QSizePolicy, QTabWidget, QScrollArea, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import QSize
from NiaPy.algorithms.utility import AlgorithmUtility

arr1 = {
    'Multi Layer Perceptron': 'MultiLayerPerceptron',
    'Ada Boosting': 'AdaBoost'
}

arr2 = {
    'Particle Swarm Optimization': 'ParticleSwarmOptimization',
    'Select K Best': 'SelectKBest'
}

arr3 = {
    'Normalizer': 'Normalizer',
    'Standard Scaler': 'StandardScaler'
}

class ListWidgetCustom(QListWidget):
    def __init__(self, items, target, *args, **kwargs):
        super(QListWidget, self).__init__(*args, **kwargs)
        self.__items = items
        self.__target = target

        for k in self.__items:
            self.addItem(k)

        self.sortItems(QtCore.Qt.AscendingOrder)
        self.itemClicked.connect(self.__clicked)

    def setTarget(self, value):
        self.__target = value

    def __clicked(self,item):
        if self.__target is not None:
            self.__target.addItem(item.text())
            self.takeItem(self.row(item))
            self.__target.sortItems(QtCore.Qt.AscendingOrder)

class Component(QPushButton):
    def __init__(self, text, *args, **kwargs):
        super(Component, self).__init__(*args, **kwargs)
        self.setText(text)
        self.setFixedHeight(100)

class HelloWindow(QMainWindow):
    __niapyAlgorithms = AlgorithmUtility().algorithm_classes.keys()

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle('NiaAML - GUI')

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        hBoxLayout = QHBoxLayout(self)

        vBoxLayout = QVBoxLayout(self)
        vBoxLayout.setContentsMargins(0, 34, 0, 0)

        h1BoxLayout = QHBoxLayout(self)
        h1BoxLayout.setContentsMargins(0, 0, 0, 0)
        
        fsasBox = self.getBox((0, 5, 3, 5), True)
        fsasList = self.getListWidget([])
        fsasBox.addWidget(fsasList)
        h1BoxLayout.addItem(fsasBox)

        ftasBox = self.getBox((3, 5, 3, 5), True)
        ftasList = self.getListWidget([])
        ftasBox.addWidget(ftasList)
        h1BoxLayout.addItem(ftasBox)

        classifiers = self.getBox((3, 5, 5, 5), True)
        classifiersList = self.getListWidget([])
        classifiers.addWidget(classifiersList)
        h1BoxLayout.addItem(classifiers)

        settingsBox = self.getBox((0, 0, 5, 5), False, 'transparent')
        settingsBox.setVerticalSpacing(10)

        optAlgos = self.getComboBox('Optimization Algorithm (components selection):', self.__niapyAlgorithms)
        optAlgosInner = self.getComboBox('Optimization Algorithm (parameter tuning) - same as first if not selected:', [*['None'], *self.__niapyAlgorithms])
        popSize = self.getTextInput('Population size (components selection):')
        popSizeInner = self.getTextInput('Population size (parameter tuning):')
        numEvals = self.getTextInput('Number of evaluations (components selection):')
        numEvalsInner = self.getTextInput('Number of evaluations (parameter tuning):')

        settingsBox.addItem(optAlgos)
        settingsBox.addItem(optAlgosInner)
        settingsBox.addItem(popSize)
        settingsBox.addItem(popSizeInner)
        settingsBox.addItem(numEvals)
        settingsBox.addItem(numEvalsInner)

        vBoxLayout.addItem(h1BoxLayout)
        vBoxLayout.addItem(settingsBox)

        exploreBox = self.getBox((0, 0, 0, 0), False)
        exploreBox.addWidget(self.getTabs(fsasList, ftasList, classifiersList))

        hBoxLayout.addItem(exploreBox)
        hBoxLayout.addItem(vBoxLayout)
        hBoxLayout.setStretchFactor(exploreBox, 1)
        hBoxLayout.setStretchFactor(vBoxLayout, 2)

        gridLayout.addLayout(hBoxLayout, 0, 0)

        centralWidget.setLayout(gridLayout)
    
    def getComboBox(self, label, items):
        comboBox = QVBoxLayout()
        comboBox.setSpacing(5)
        label = QLabel(label, self)
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        cb = QComboBox()
        cb.setFont(font)
        for k in items:
            cb.addItem(k)
        comboBox.addWidget(label)
        comboBox.addWidget(cb)
        return comboBox
    
    def getTextInput(self, label):
        textBox = QVBoxLayout()
        textBox.setSpacing(5)
        label = QLabel(label, self)
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        tb = QLineEdit(self)
        tb.setFont(font)
        textBox.addWidget(label)
        textBox.addWidget(tb)
        return textBox

    def getBox(self, tupleMargins, visibleBorder, background_color = '#fff'):
        l = QGridLayout()
        l.setContentsMargins(*tupleMargins)
        return l
    
    def getListWidget(self, items, targetBox = None):
        listWidget = ListWidgetCustom(items, targetBox)
        font = listWidget.font()
        font.setPointSize(12)
        listWidget.setFont(font)
        return listWidget
    
    def getTabs(self, fsasList, ftasList, classifiersList):
        tabs = QTabWidget(self)

        fsas = self.getListWidget(arr2, fsasList)
        fsasList.setTarget(fsas)
        tabs.addTab(fsas, 'Feature Selection Algorithms')

        ftas = self.getListWidget(arr3, ftasList)
        ftasList.setTarget(ftas)
        tabs.addTab(ftas, 'Feature Selection Algorithms')

        clas = self.getListWidget(arr1, classifiersList)
        classifiersList.setTarget(clas)
        tabs.addTab(clas, 'Classifiers')

        font = tabs.font()
        font.setPointSize(10)
        tabs.setFont(font)
        tabs.setStyleSheet("QTabBar::tab { height: 40px; }")
        return tabs

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())