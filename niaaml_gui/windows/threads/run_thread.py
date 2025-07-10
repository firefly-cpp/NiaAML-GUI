from PyQt6.QtCore import QThread, pyqtSignal
from niaaml.data import CSVDataReader
from niaaml import Pipeline


class RunThread(QThread):
    ran = pyqtSignal(object)

    def __init__(self, data):
        super().__init__()
        self.__data = data
    
    def run(self):
        dataReader = CSVDataReader(
            src=self.__data.csvSrc,
            contains_classes=False,
            has_header=self.__data.csvHasHeader,
        )
        #self.__data.pipelineSrc = "C:\\Users\\Aljaž\\Desktop\\NiaAMLnewUI"
        #pipeline = Pipeline.load(self.__data.pipelineSrc)
        self.__data.csvHasHeader = True
        pipeline = Pipeline.load("C:\\Users\\Aljaž\\Desktop\\NiaAMLnewUI\\niaamlGUIoutput.ppln")
        predictions = pipeline.run(dataReader.get_x())
        self.ran.emit(str(predictions))
