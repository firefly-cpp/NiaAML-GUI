from PyQt6.QtCore import QThread, pyqtSignal
from niaaml.data import CSVDataReader
from niaaml import PipelineOptimizer
import os

def print_pipeline_values(data):
        print("\n Vrednosti, ki se pošiljajo v optimizacijo:\n")
        for key, value in vars(data).items():
                print(f"  {key} = {value}")
        print("\n" + "-" * 60 + "\n")
class OptimizeThread(QThread):
    optimized = pyqtSignal(object)
    progress = pyqtSignal(object)

    def __init__(self, data):
        super().__init__()
        self.__data = data
    
    def run(self):
        dataReader = CSVDataReader(
            src=self.__data.csvSrc,
            has_header=self.__data.csvHasHeader
        )

        fsas = self.__data.fsas.split("\n") if isinstance(self.__data.fsas, str) else self.__data.fsas
        ftas = self.__data.ftas.split("\n") if isinstance(self.__data.ftas, str) else self.__data.ftas
        clfs = self.__data.classifiers.split("\n") if isinstance(self.__data.classifiers, str) else self.__data.classifiers
        optimizer = PipelineOptimizer(
            data=dataReader,
            classifiers=[c.strip() for c in clfs if c.strip()],
            feature_selection_algorithms=[f.strip() for f in fsas if f.strip()],
            feature_transform_algorithms=[f.strip() for f in ftas if f.strip()],
            categorical_features_encoder=self.__data.encoder,
            imputer=self.__data.imputer,         
        )
        optimizer._PipelineOptimizer__logger = HackyLogger(self.progress.emit)
        print_pipeline_values(self.__data)
        if self.__data.isOptimization is True:
            pipeline = optimizer.run(
                self.__data.fitnessFunctionName,
                self.__data.popSize,
                self.__data.popSizeInner,
                self.__data.numEvals,
                self.__data.numEvalsInner,
                self.__data.optAlgName,
                self.__data.optAlgInnerName,
            )
        else:
            pipeline = optimizer.run_v1(
                self.__data.fitnessFunctionName,
                self.__data.popSize,
                self.__data.numEvals,
                self.__data.optAlgName,
            )
        
        pipeline.export(os.path.join(self.__data.outputFolder, "niaamlGUIoutput"))
        pipeline.export_text(os.path.join(self.__data.outputFolder, "niaamlGUIoutput"))
        
        self.optimized.emit(pipeline.to_string())


class HackyLogger:
    def __init__(self, emit_func, **kwargs):
        self.__emit = emit_func

    def log_progress(self, text):
        self.__emit(text)

    def log_pipeline(self, text):
        return

    def log_optimization_error(self, text):
        return
    
    def info(self, msg):
        print("msg", msg)  
