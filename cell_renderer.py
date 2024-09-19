import sympy
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLineEdit, QSizePolicy, QMenu, QMenuBar, QListWidget, 
                             QAbstractScrollArea)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PIL import Image
import cell_manager
import main


print("sup makai")

def makeWidgetFromCell(cell):
    cellListItem = QHBoxLayout() #ea

    label = QLabel(str(cell_manager.getCellIndex(cell)))

    textEdit = QLineEdit()
    textEdit.setText(cell_manager.getCellContent(cell))


    cellListItem.addWidget(label)
    cellListItem.addWidget(textEdit)
    # textedit = QLabel(cell_manager.getCellContent(cell))
    return textEdit

def clearVBoxLayout(layout: QVBoxLayout):
    for i in reversed(range(  layout.count()  )):
        layout.removeItem(layout.itemAt(i))
