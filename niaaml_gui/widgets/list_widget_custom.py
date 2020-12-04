from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget

class ListWidgetCustom(QListWidget):
    def __init__(self, items, target, name, *args, **kwargs):
        super(QListWidget, self).__init__(*args, **kwargs)
        self.__items = items
        self.__target = target

        for k in self.__items:
            self.addItem(k)

        self.sortItems(QtCore.Qt.AscendingOrder)
        self.itemClicked.connect(self.__clicked)
        self.setObjectName(name)

    def setTarget(self, value):
        self.__target = value

    def __clicked(self,item):
        if self.__target is not None:
            self.__target.addItem(item.text())
            self.takeItem(self.row(item))
            self.__target.sortItems(QtCore.Qt.AscendingOrder)