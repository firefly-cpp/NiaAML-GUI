import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from niaaml_gui.widgets.pipeline_canvas import PipelineCanvas

class CanvasTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pipeline Canvas Test")
        self.setGeometry(100, 100, 1200, 800)

        self.canvas = PipelineCanvas(self)
        self.setCentralWidget(self.canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CanvasTestWindow()
    window.show()
    sys.exit(app.exec())
