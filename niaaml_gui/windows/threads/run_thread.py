from PyQt5 import QtCore
from niaaml.data import CSVDataReader
from niaaml import Pipeline

class RunThread(QtCore.QThread):

    ran = QtCore.pyqtSignal(object)

    def __init__(self, data):
        QtCore.QThread.__init__(self)
        self.__data = data
    
    def run(self):
        dataReader = CSVDataReader(src=self.__data.csvSrc, contains_classes=False, has_header=self.__data.csvHasHeader)
        pipeline = Pipeline.load(self.__data.pipelineSrc)
        predictions = pipeline.run(dataReader.get_x())
        self.ran.emit(str(predictions))