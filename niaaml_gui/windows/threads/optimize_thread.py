from PyQt5 import QtCore
from niaaml.data import CSVDataReader
from niaaml import PipelineOptimizer
import os

class OptimizeThread(QtCore.QThread):

    optimized = QtCore.pyqtSignal(object)

    def __init__(self, data):
        QtCore.QThread.__init__(self)
        self.__data = data
    
    def run(self):
        dataReader = CSVDataReader(src=self.__data.csvSrc, has_header=self.__data.csvHasHeader)
        optimizer = PipelineOptimizer(
            data=dataReader,
            feature_selection_algorithms=self.__data.fsas,
            feature_transform_algorithm=self.__data.ftas,
            classifiers=self.__data.classifiers,
            categorical_features_encoder=self.__data.encoder
        )
        pipeline = optimizer.run(self.__data.fitnessFunctionName, self.__data.popSize, self.__data.popSizeInner, self.__data.numEvals, self.__data.numEvalsInner, self.__data.optAlgName, self.__data.optAlgInnerName)
        pipeline.export(os.path.join(self.__data.outputFolder, 'niaamlGUIoutput'))
        pipeline.export_text(os.path.join(self.__data.outputFolder, 'niaamlGUIoutput'))
        self.optimized.emit(pipeline.to_string())