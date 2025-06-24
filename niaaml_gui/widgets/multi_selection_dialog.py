from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton

class MultiSelectDialog(QDialog):
    def __init__(self, title, options):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        for option in options:
            item = QListWidgetItem(option)
            self.listWidget.addItem(item)

        layout.addWidget(self.listWidget)

        btn = QPushButton("OK")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def selected_items(self):
        return [item.text() for item in self.listWidget.selectedItems()]
