from PyQt6.QtCore import QThread, pyqtSignal
from niaaml.data import CSVDataReader
from niaaml import Pipeline
from pathlib import Path


class RunThread(QThread):
    ran = pyqtSignal(object)

    def __init__(self, data):
        super().__init__()
        self.__data = data

    def run(self):
        try:
            dataReader = CSVDataReader(
                src=self.__data.csvSrc,
                contains_classes=True,
                has_header=self.__data.csvHasHeader,
            )

            if not self.__data.pipelineSrc:
                self.__data.pipelineSrc = (
                    Path(self.__data.outputFolder) / "niaamlGUIoutput.ppln"
                )

            pipeline = Pipeline.load(self.__data.pipelineSrc)

            x_data = dataReader.get_x()

            predictions = pipeline.run(x_data)

            self.ran.emit(str(predictions))

        except Exception as e:
            import traceback

            traceback.print_exc()
            self.ran.emit(f"ERROR: {str(e)}")
