from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QTabWidget
from NiaPy.algorithms.utility import AlgorithmUtility
from niaaml_gui.widgets.list_widget_custom import ListWidgetCustom
from niaaml_gui.widgets.base_main_widget import BaseMainWidget
from niaaml.classifiers import ClassifierFactory
from niaaml.preprocessing.feature_selection import FeatureSelectionAlgorithmFactory
from niaaml.preprocessing.feature_transform import FeatureTransformAlgorithmFactory

class OptimizationWidget(BaseMainWidget):
    __niapyAlgorithms = list(AlgorithmUtility().algorithm_classes.keys())
    __niaamlFeatureSelectionAlgorithms = list(FeatureSelectionAlgorithmFactory().get_name_to_classname_mapping().keys())
    __niaamlFeatureTransformAlgorithms = list(FeatureTransformAlgorithmFactory().get_name_to_classname_mapping().keys())
    __niaamlClassifiers = list(ClassifierFactory().get_name_to_classname_mapping().keys())

    def __init__(self, parent, *args, **kwargs):
        self.__niapyAlgorithms.sort()
        self.__niaamlFeatureSelectionAlgorithms.sort()
        self.__niaamlFeatureTransformAlgorithms.sort()
        self.__niaamlClassifiers.sort()
        super().__init__(parent, *args, **kwargs)

        selectFileBar = QHBoxLayout(self._parent)
        selectFileBar.setSpacing(0)
        selectFileBar.setContentsMargins(0, 5, 5, 5)
        fNameLine = QLineEdit(self._parent)
        fNameLine.setObjectName('csvFile')
        fNameLine.setPlaceholderText('Select a CSV dataset file...')
        fNameLine.setReadOnly(True)
        font = fNameLine.font()
        font.setPointSize(12)
        fNameLine.setFont(font)
        selectFileBar.addWidget(fNameLine)
        selectFileBar.addWidget(self._createButton('Select file', self._openCSVFile))

        hBoxLayout = QHBoxLayout(self._parent)
        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        vBoxLayout = QVBoxLayout(self._parent)
        vBoxLayout.setContentsMargins(0, 34, 0, 0)

        h1BoxLayout = QHBoxLayout(self._parent)
        h1BoxLayout.setContentsMargins(0, 0, 0, 0)
        
        fsasBox = self.__createGridLayoutBox((0, 5, 3, 5), True)
        fsasList = self.__createListWidget([], None, 'fsasList')
        fsasBox.addWidget(fsasList)
        h1BoxLayout.addItem(fsasBox)

        ftasBox = self.__createGridLayoutBox((3, 5, 3, 5), True)
        ftasList = self.__createListWidget([], None, 'ftasList')
        ftasBox.addWidget(ftasList)
        h1BoxLayout.addItem(ftasBox)

        classifiers = self.__createGridLayoutBox((3, 5, 5, 5), True)
        classifiersList = self.__createListWidget([], None, 'classifiersList')
        classifiers.addWidget(classifiersList)
        h1BoxLayout.addItem(classifiers)

        settingsBox = self.__createGridLayoutBox((0, 0, 5, 5), False, 'transparent')
        settingsBox.setVerticalSpacing(10)

        optAlgos = self.__createComboBox('Optimization Algorithm (components selection):', self.__niapyAlgorithms, 'optAlgos')
        optAlgosInner = self.__createComboBox('Optimization Algorithm (parameter tuning) - same as first if not selected:', [*['None'], *self.__niapyAlgorithms], 'optAlgosInner')
        popSize = self.__createTextInput('Population size (components selection):', 'popSize')
        popSizeInner = self.__createTextInput('Population size (parameter tuning):', 'popSizeInner')
        numEvals = self.__createTextInput('Number of evaluations (components selection):', 'numEvals')
        numEvalsInner = self.__createTextInput('Number of evaluations (parameter tuning):', 'numEvalsInner')

        settingsBox.addItem(optAlgos)
        settingsBox.addItem(optAlgosInner)
        settingsBox.addItem(popSize)
        settingsBox.addItem(popSizeInner)
        settingsBox.addItem(numEvals)
        settingsBox.addItem(numEvalsInner)

        confirmBar = QHBoxLayout(self._parent)
        confirmBar.setContentsMargins(5, 5, 5, 5)
        confirmBar.addStretch()
        confirmBar.addWidget(self._createButton('Start optimization', self.__runOptimize))

        vBoxLayout.addItem(selectFileBar)
        vBoxLayout.addItem(h1BoxLayout)
        vBoxLayout.addItem(settingsBox)
        vBoxLayout.addItem(confirmBar)

        exploreBox = self.__createGridLayoutBox((0, 0, 0, 0), False)
        exploreBox.addWidget(self.__createTabs(fsasList, ftasList, classifiersList))

        hBoxLayout.addItem(exploreBox)
        hBoxLayout.addItem(vBoxLayout)
        hBoxLayout.setStretchFactor(exploreBox, 1)
        hBoxLayout.setStretchFactor(vBoxLayout, 2)

        self.setLayout(hBoxLayout)
    
    def __createComboBox(self, label, items, name):
        comboBox = QVBoxLayout()
        comboBox.setSpacing(5)
        label = QLabel(label, self._parent)
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        cb = QComboBox()
        cb.setObjectName(name)
        cb.setFont(font)
        for k in items:
            cb.addItem(k)
        comboBox.addWidget(label)
        comboBox.addWidget(cb)
        return comboBox
    
    def __createTextInput(self, label, name):
        textBox = QVBoxLayout()
        textBox.setSpacing(5)
        label = QLabel(label, self._parent)
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        tb = QLineEdit(self._parent)
        tb.setObjectName(name)
        tb.setFont(font)
        textBox.addWidget(label)
        textBox.addWidget(tb)
        return textBox

    def __createGridLayoutBox(self, tupleMargins, visibleBorder, background_color = '#fff'):
        l = QGridLayout()
        l.setContentsMargins(*tupleMargins)
        return l
    
    def __createListWidget(self, items, targetBox = None, name = None):
        listWidget = ListWidgetCustom(items, targetBox, name)
        font = listWidget.font()
        font.setPointSize(12)
        listWidget.setFont(font)
        return listWidget
    
    def __createTabs(self, fsasList, ftasList, classifiersList):
        tabs = QTabWidget(self._parent)

        fsas = self.__createListWidget(self.__niaamlFeatureSelectionAlgorithms, fsasList)
        fsasList.setTarget(fsas)
        tabs.addTab(fsas, 'Feature Selection Algorithms')

        ftas = self.__createListWidget(self.__niaamlFeatureTransformAlgorithms, ftasList)
        ftasList.setTarget(ftas)
        tabs.addTab(ftas, 'Feature Selection Algorithms')

        clas = self.__createListWidget(self.__niaamlClassifiers, classifiersList)
        classifiersList.setTarget(clas)
        tabs.addTab(clas, 'Classifiers')

        font = tabs.font()
        font.setPointSize(10)
        tabs.setFont(font)
        tabs.setStyleSheet("QTabBar::tab { height: 40px; }")
        return tabs
    
    def __runOptimize(self):
        err = ''

        csvSrc = self.findChild(QLineEdit, 'csvFile').text()
        if self._isNoneOrWhiteSpace(csvSrc):
            err += 'Select CSV dataset file.\n'

        optAlgName = str(self.findChild(QComboBox, 'optAlgos').currentText())
        optAlgInnerName = str(self.findChild(QComboBox, 'optAlgosInner').currentText())
        if optAlgInnerName == 'None':
            optAlgInnerName = optAlgName

        popSize = self.findChild(QLineEdit, 'popSize').text()
        if self._isNoneOrWhiteSpace(popSize):
            err += 'Select population size.\n'
        else:
            try:
                popSize = int(popSize)
            except:
                err += 'Invalid population size value.\n'

        popSizeInner = self.findChild(QLineEdit, 'popSizeInner').text()
        if self._isNoneOrWhiteSpace(popSizeInner):
            err += 'Select inner population size.\n'
        else:
            try:
                popSizeInner = int(popSizeInner)
            except:
                err += 'Invalid inner population size value.\n'

        numEvals = self.findChild(QLineEdit, 'numEvals').text()
        if self._isNoneOrWhiteSpace(numEvals):
            err += 'Select number of evaluations.\n'
        else:
            try:
                numEvals = int(numEvals)
            except:
                err += 'Invalid number of evaluations.\n'

        numEvalsInner = self.findChild(QLineEdit, 'numEvalsInner').text()
        if self._isNoneOrWhiteSpace(numEvalsInner):
            err += 'Select number of inner evaluations.\n'
        else:
            try:
                numEvalsInner = int(numEvalsInner)
            except:
                err += 'Invalid number of inner evaluations.\n'
        
        fsasList = self.findChild(ListWidgetCustom, 'fsasList')
        fsas = [fsasList.item(i).text() for i in range(fsasList.count())]

        ftasList = self.findChild(ListWidgetCustom, 'ftasList')
        ftas = [ftasList.item(i).text() for i in range(ftasList.count())]

        clsList = self.findChild(ListWidgetCustom, 'classifiersList')
        classifiers = [clsList.item(i).text() for i in range(clsList.count())]
        if len(classifiers) == 0:
            err += 'Select at least one classifier.\n'
        
        if not self._isNoneOrWhiteSpace(err):
            self._parent.errorMessage.setText(err)
            self._parent.errorMessage.show()
        
        # TODO optimization