from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QTabWidget, QFileDialog, QCheckBox, QPushButton
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from niapy.util.factory import _algorithm_options
from niaaml_gui.widgets.list_widget_custom import ListWidgetCustom
from niaaml_gui.widgets.base_main_widget import BaseMainWidget
from niaaml_gui.windows import ProcessWindow
from niaaml_gui.process_window_data import ProcessWindowData
from niaaml.classifiers import ClassifierFactory
from niaaml.preprocessing.feature_selection import FeatureSelectionAlgorithmFactory
from niaaml.preprocessing.feature_transform import FeatureTransformAlgorithmFactory
from niaaml.fitness import FitnessFactory
from niaaml.preprocessing.encoding import EncoderFactory
from niaaml.preprocessing.imputation import ImputerFactory
import qtawesome as qta

class OptimizationWidget(BaseMainWidget):
    __niaamlFeatureSelectionAlgorithms = FeatureSelectionAlgorithmFactory().get_name_to_classname_mapping()
    __niaamlFeatureTransformAlgorithms = FeatureTransformAlgorithmFactory().get_name_to_classname_mapping()
    __niaamlClassifiers = ClassifierFactory().get_name_to_classname_mapping()
    __niaamlFitnessFunctions = FitnessFactory().get_name_to_classname_mapping()
    __niaamlEncoders = EncoderFactory().get_name_to_classname_mapping()
    __niaamlImputers = ImputerFactory().get_name_to_classname_mapping()
    __niapyAlgorithmsList = list(_algorithm_options().keys())
    __niaamlFeatureSelectionAlgorithmsList = list(__niaamlFeatureSelectionAlgorithms.keys())
    __niaamlFeatureTransformAlgorithmsList = list(__niaamlFeatureTransformAlgorithms.keys())
    __niaamlClassifiersList = list(__niaamlClassifiers.keys())
    __niaamlFitnessFunctionsList = list(__niaamlFitnessFunctions.keys())
    __niaamlEncodersList = list(__niaamlEncoders.keys())
    __niaamlImputersList = list(__niaamlImputers.keys())

    def __init__(self, parent, is_v1 = False, *args, **kwargs):
        self.__niapyAlgorithmsList.sort()
        self.__niaamlFeatureSelectionAlgorithmsList.sort()
        self.__niaamlFeatureTransformAlgorithmsList.sort()
        self.__niaamlClassifiersList.sort()
        self.__is_v1 = is_v1
        super().__init__(parent, *args, **kwargs)

        fileLayout = QHBoxLayout(self._parent)

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
        editBtn = self._createButton(None, self._editCSVFile, 'editCSVButton', qta.icon('fa5.edit'))
        editBtn.setEnabled(False)
        selectFileBar.addWidget(editBtn)
        selectFileBar.addWidget(self._createButton('Select file', self._openCSVFile))

        checkBox = QCheckBox('CSV has header')
        checkBox.setObjectName('csv')
        checkBox.setFont(font)

        fileLayout.addItem(selectFileBar)
        fileLayout.addWidget(checkBox)

        encoders = self.__createComboBox('Categorical features\' encoder:', self.__niaamlEncodersList, 'encoders')
        imputers = self.__createComboBox('Missing features\' imputer:', self.__niaamlImputersList, 'imputers')

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

        optAlgosLabel = 'Optimization Algorithm (components selection):' if not self.__is_v1 else 'Optimization Algorithm:'
        optAlgos = self.__createComboBox(optAlgosLabel, self.__niapyAlgorithmsList, 'optAlgos')

        optAlgosInner = self.__createComboBox('Optimization Algorithm (parameter tuning) - same as first if not selected:', [*['None'], *self.__niapyAlgorithmsList], 'optAlgosInner')

        validator = QtGui.QRegExpValidator(QtCore.QRegExp('[1-9][0-9]*'))

        popSizeLabel = 'Population size (components selection):' if not self.__is_v1 else 'Population size:'
        popSize = self.__createTextInput(popSizeLabel, 'popSize', validator)

        popSizeInner = self.__createTextInput('Population size (parameter tuning):', 'popSizeInner', validator)

        numEvalsLabel = 'Number of evaluations (components selection):' if not self.__is_v1 else 'Number of evaluations'
        numEvals = self.__createTextInput(numEvalsLabel, 'numEvals', validator)

        numEvalsInner = self.__createTextInput('Number of evaluations (parameter tuning):', 'numEvalsInner', validator)

        fitFuncs = self.__createComboBox('Fitness Function:', self.__niaamlFitnessFunctionsList, 'fitFuncs')

        selectOutputFolderBar = QHBoxLayout(self._parent)
        selectOutputFolderBar.setSpacing(0)
        foNameLine = QLineEdit(self._parent)
        foNameLine.setObjectName('outputFolder')
        foNameLine.setPlaceholderText('Select pipeline output folder...')
        foNameLine.setReadOnly(True)
        font = foNameLine.font()
        font.setPointSize(12)
        foNameLine.setFont(font)
        selectOutputFolderBar.addWidget(foNameLine)
        selectOutputFolderBar.addWidget(self._createButton('Select folder', self.__selectDirectory))

        settingsBox.addItem(optAlgos)
        if not self.__is_v1:
            settingsBox.addItem(optAlgosInner)
        settingsBox.addItem(popSize)
        if not self.__is_v1:
            settingsBox.addItem(popSizeInner)
        settingsBox.addItem(numEvals)
        if not self.__is_v1:
            settingsBox.addItem(numEvalsInner)
        settingsBox.addItem(fitFuncs)
        settingsBox.addItem(selectOutputFolderBar)

        confirmBar = QHBoxLayout(self._parent)
        confirmBar.setContentsMargins(5, 5, 5, 5)
        confirmBar.addStretch()
        confirmBar.addWidget(self._createButton('Start optimization', self.__runOptimize))

        vBoxLayout.addItem(fileLayout)
        vBoxLayout.addItem(encoders)
        vBoxLayout.addItem(imputers)
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
    
    def __createTextInput(self, label, name, validator=None):
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

        if validator is not None:
            tb.setValidator(validator)

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

        fsas = self.__createListWidget(self.__niaamlFeatureSelectionAlgorithmsList, fsasList)
        fsasList.setTarget(fsas)
        tabs.addTab(fsas, 'Feature Selection Algorithms')

        ftas = self.__createListWidget(self.__niaamlFeatureTransformAlgorithmsList, ftasList)
        ftasList.setTarget(ftas)
        tabs.addTab(ftas, 'Feature Selection Algorithms')

        clas = self.__createListWidget(self.__niaamlClassifiersList, classifiersList)
        classifiersList.setTarget(clas)
        tabs.addTab(clas, 'Classifiers')

        font = tabs.font()
        font.setPointSize(10)
        tabs.setFont(font)
        tabs.setStyleSheet("QTabBar::tab { height: 40px; }")
        return tabs
    
    def __selectDirectory(self):
        fname = str(QFileDialog.getExistingDirectory(parent=self._parent, caption='Select Directory'))
        self.findChild(QLineEdit, 'outputFolder').setText(fname)
    
    def __runOptimize(self):
        err = ''

        csvSrc = self.findChild(QLineEdit, 'csvFile').text()
        if self._isNoneOrWhiteSpace(csvSrc):
            err += 'Select CSV dataset file.\n'
        
        encoderName = self.__niaamlEncoders[str(self.findChild(QComboBox, 'encoders').currentText())]
        imputerName = self.__niaamlImputers[str(self.findChild(QComboBox, 'imputers').currentText())]

        optAlgName = str(self.findChild(QComboBox, 'optAlgos').currentText())

        if not self.__is_v1:
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

        if not self.__is_v1:
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

        if not self.__is_v1:
            numEvalsInner = self.findChild(QLineEdit, 'numEvalsInner').text()
            if self._isNoneOrWhiteSpace(numEvalsInner):
                err += 'Select number of inner evaluations.\n'
            else:
                try:
                    numEvalsInner = int(numEvalsInner)
                except:
                    err += 'Invalid number of inner evaluations.\n'
        
        fsasList = self.findChild(ListWidgetCustom, 'fsasList')
        fsas = [self.__niaamlFeatureSelectionAlgorithms[fsasList.item(i).text()] for i in range(fsasList.count())]

        ftasList = self.findChild(ListWidgetCustom, 'ftasList')
        ftas = [self.__niaamlFeatureTransformAlgorithms[ftasList.item(i).text()] for i in range(ftasList.count())]

        clsList = self.findChild(ListWidgetCustom, 'classifiersList')
        classifiers = [self.__niaamlClassifiers[clsList.item(i).text()] for i in range(clsList.count())]
        if len(classifiers) == 0:
            err += 'Select at least one classifier.\n'
        
        fitnessFunctionName = self.__niaamlFitnessFunctions[str(self.findChild(QComboBox, 'fitFuncs').currentText())]

        outputFolder = self.findChild(QLineEdit, 'outputFolder').text()
        if self._isNoneOrWhiteSpace(outputFolder):
            err += 'Select an output directory.\n'
        
        if not self._isNoneOrWhiteSpace(err):
            self._parent.errorMessage.setText(err)
            self._parent.errorMessage.show()
            return
        
        if not self.__is_v1:
            self._processWindow = ProcessWindow(
                self._parent,
                ProcessWindowData(
                    True,
                    csvSrc,
                    self.findChild(QCheckBox, 'csv').isChecked(),
                    encoderName,
                    imputerName,
                    optAlgName,
                    optAlgInnerName,
                    popSize,
                    popSizeInner,
                    numEvals,
                    numEvalsInner,
                    fsas,
                    ftas,
                    classifiers,
                    fitnessFunctionName,
                    outputFolder
                    )
                )
        else:
            self._processWindow = ProcessWindow(
                self._parent,
                ProcessWindowData(
                    'v1',
                    csvSrc,
                    self.findChild(QCheckBox, 'csv').isChecked(),
                    encoderName,
                    imputerName,
                    optAlgName=optAlgName,
                    popSize=popSize,
                    numEvals=numEvals,
                    fsas=fsas,
                    ftas=ftas,
                    classifiers=classifiers,
                    fitnessFunctionName=fitnessFunctionName,
                    outputFolder=outputFolder
                    )
                )

        self._processWindow.show()