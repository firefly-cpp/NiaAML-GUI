from PyQt5 import QtCore
from niaaml.data import CSVDataReader
from niaaml import PipelineOptimizer
import os
import sys

class OptimizeThread(QtCore.QThread):

    optimized = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)

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
            categorical_features_encoder=self.__data.encoder,
            imputer=self.__data.imputer
        )
        optimizer._PipelineOptimizer__logger = HackyLogger(self.progress.emit)

        if self.__data.isOptimization is True:
            pipeline = optimizer.run(self.__data.fitnessFunctionName, self.__data.popSize, self.__data.popSizeInner, self.__data.numEvals, self.__data.numEvalsInner, self.__data.optAlgName, self.__data.optAlgInnerName)
        else:
            pipeline = optimizer.run_v1(self.__data.fitnessFunctionName, self.__data.popSize, self.__data.numEvals, self.__data.optAlgName)

        pipeline.export(os.path.join(self.__data.outputFolder, 'niaamlGUIoutput'))
        pipeline.export_text(os.path.join(self.__data.outputFolder, 'niaamlGUIoutput'))
        self.optimized.emit(pipeline.to_string())

class HackyLogger:
    def __init__(self, emit_func,  **kwargs):
        self.__emit = emit_func

    def log_progress(self, text):
        self.__emit(text)

    def log_pipeline(self, text):
        return

    def log_optimization_error(self, text):
        return
