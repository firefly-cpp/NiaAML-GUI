from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ResultsWidget(QWidget):
    def __init__(self, parent=None, results_data=None, pipeline_settings=None):
        super().__init__(parent)
        self.setObjectName("resultsView")
        self._parent = parent
        self.results_data = results_data or {}
        self.pipeline_settings = pipeline_settings or {}
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        layout = QVBoxLayout()

        title = QLabel("Optimization Results")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # stats table
        table = QTableWidget(4, 2)
        table.setHorizontalHeaderLabels(["Metric", "Value"])
        table.setFixedHeight(table.verticalHeader().length() + table.horizontalHeader().height())
        # table.resizeColumnsToContents()
        # table.resizeRowsToContents()

        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)        
        total_width = sum([table.columnWidth(i) for i in range(table.columnCount())])
        total_width += table.verticalHeader().width()
        total_width += 2 * table.frameWidth() #edges
        table.setMaximumWidth(total_width)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #005f85;
                color: white;
                border: 1px solid #001D85;
                gridline-color: #001D85;
            }
            QHeaderView::section {
                background-color: #001D85;
                color: white;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #008569;
                color: white;
            }
        """)
        metrics = [
            ("Accuracy", results_data.get("accuracy", 0.0)),
            ("Precision", results_data.get("precision", 0.0)),
            ("F1-score", results_data.get("f1_score", 0.0)),
            ("Cohen's Kappa", results_data.get("kappa", 0.0)),
        ]
        for row, (label, value) in enumerate(metrics):
            table.setItem(row, 0, QTableWidgetItem(label))
            table.setItem(row, 1, QTableWidgetItem(f"{value:.4f}"))

        layout.addWidget(table)
        # graph
        fig = Figure()
        fig = Figure(facecolor="#005f85")
        
        canvas = FigureCanvas(fig)
        canvas.setObjectName("graphCanvas")
          
        ax = fig.add_subplot(111)
        ax.set_facecolor("#005f85")  
        ax.bar(["Accuracy", "Precision", "F1", "Kappa"], [0.4634, 0.4478, 0.4339, 0.174])
        ax.tick_params(colors="white")  # bela besedila na osi
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        
        layout.addWidget(canvas)
        
        # pipeline settings table
        if pipeline_settings:
            pipeline_table = QTableWidget(len(pipeline_settings), 2)
            pipeline_table.setHorizontalHeaderLabels(["Parameter", "Value"])
            for row, (key, value) in enumerate(pipeline_settings.items()):
                pipeline_table.setItem(row, 0, QTableWidgetItem(str(key)))
                pipeline_table.setItem(row, 1, QTableWidgetItem(str(value)))

            pipeline_table.resizeColumnsToContents()  # <- ključna vrstica
            pipeline_table.resizeRowsToContents()

            pipeline_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            pipeline_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            total_width = sum([pipeline_table.columnWidth(i) for i in range(pipeline_table.columnCount())])
            total_width += pipeline_table.verticalHeader().width()
            total_width += 2 * pipeline_table.frameWidth()
            pipeline_table.setMaximumWidth(total_width)

            pipeline_table.setStyleSheet("""
                QTableWidget {
                    background-color: #005f85;
                    color: white;
                    border: 1px solid #001D85;
                    gridline-color: #001D85;
                }
                QHeaderView::section {
                    background-color: #001D85;
                    color: white;
                    font-weight: bold;
                }
                QTableWidget::item:selected {
                    background-color: #008569;
                    color: white;
                }
            """)

            layout.addWidget(pipeline_table)
        
        back_btn = QPushButton("Back to main view")
        back_btn.clicked.connect(self.__goBack)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def __goBack(self):
        if self._parent:
            from niaaml_gui.widgets import OptimizationWidget
            self._parent.setCentralWidget(OptimizationWidget(self._parent))
