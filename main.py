import sys
import os
import time
import math
import PyQt5
import PyQt5.Qt
import cell_grapher
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import cell_manager
from cell_manager import cell as cellClass
import cell_renderer
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-codespace"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLineEdit, QSizePolicy, QMenu, QMenuBar, QListWidget, 
                             QScrollArea,QGroupBox)
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy.plotting import plot
import sympy
from sympy import *

#if you run this file on the codespace nothing will appear but it will sill work just without visuals
#if you want to see stuff download this locally with it's dependcies and run it

#colors
#region
#colros
mainColor = "#636363"
secondaryColor = "#694c4c"


#dependices pyqt5 sympy numpy matplotlib

#endregion

#decalre vars
#region


#TODO -------------------     look at https://docs.aspose.com/tex/python-net/latex-to-image/  ---------------------


print("\n\n\n\n\n")
appName = "TSA PHS software devleopment submission"
appIconImageLink = "assets\images\sigma.png"
MinWindowWidth = 1500
MinWindowHeight = 500
windowWidth = MinWindowWidth
windowHeight = MinWindowHeight
graphScreenWidthPercent = .5

cellEditorScreenItemHeight = 25

#threadcontroller class
class threadController():

    def __init__(self):

        #setup logic threac
        #region
        self.worker = programEventLoopThreadClass()

        self.programEventLoopThread  = QThread()

        self.setupForeverThread(self.worker, self.programEventLoopThread)

        #endregion


        #setup gui thread
        #region
        self.guiWorker = guiUpdateLoopThreadClass()

        self.guiUpdateLoopThread  = QThread()

        self.setupForeverThread(self.guiWorker, self.guiUpdateLoopThread)

        #endregion

    def setupForeverThread(self, paramworker, paramthread): 
        paramworker.moveToThread(paramthread) #this is fine

        paramthread.started.connect(paramworker.run)
        paramthread.start()

class addCellToCellEditorSignalEmitter(QObject):
    addCellToCellEditorSignal = pyqtSignal(cellClass)



global addCellToCellEditorSignalEmitterId
addCellToCellEditorSignalEmitterId = addCellToCellEditorSignalEmitter()





class cellWidgetManager(QObject):


    def __init__(self):
        super().__init__()
        self.myCellWidgets = []
        self.myCellWidgetsObjects = []
    

    def addCellToCellEditorScreen(self,cell : cellClass):
        
        cellWidgetLineEdit = QLineEdit()
        cellWidgetLineEdit.setText(cell_manager.getCellContent(cell))
        cellWidgetLineEdit.setFixedHeight(cellEditorScreenItemHeight)
        cell.setCellWidget(cellWidgetLineEdit)

        cellEditorScreen.addWidget(cellWidgetLineEdit)
        self.myCellWidgets.append(cellWidgetLineEdit)

        
        self.myCellWidgets.append(cellWidget())

    

class cellWidget(QObject):
    def __init__(self):
        pass


#endregion


#useful funcs
#region
def makeCellToLineEdit(cell):
    newLineEdit = QLineEdit()
    newLineEdit.setText(cell_manager.getCellContent(cell))
    return newLineEdit

def clearLayout(layout):
    for i in reversed(range(layout.count())):
        layout.removeItem(layout.itemAt(i))

#endregion




#ui
class graphCanvas(QLabel):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        #settings
        self.backgroundColor = QColor( 255, 255, 255, 255)
        self.axisThickness = 20
        
        #region fuck me
        self.pixmap = QPixmap(QSize(10000,10000))  
        self.painter = QPainter(self.pixmap)
        self.last_size = QSize()

        self.pixmap.fill(self.backgroundColor)
        self.setScaledContents(True)  # Enable scaling
        self.update_pixmap()
        #endregion


    def update_pixmap(self):
        self.pixmap.fill(self.backgroundColor)
        width = self.pixmap.width()
        height = self.pixmap.height()
        center = [int(width/2),int(height/2)]
        
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(10)   
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setBrush(QBrush(Qt.GlobalColor.black,Qt.BrushStyle.SolidPattern))
        self.painter.setPen(pen)
        self.painter.drawRect(0,center[1],width,self.axisThickness)
        self.painter.drawRect(center[0],0,self.axisThickness,height)

        


        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)  # Keep aspect ratio
        self.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        # Update pixmap when the label is resized
        if self.size() != self.last_size:
            self.update_pixmap()
            self.last_size = self.size()
    
        super().resizeEvent(event)

    
 



    

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(MinWindowWidth )
        self.setMinimumHeight(MinWindowHeight)
        self.setStyleSheet("background-color: " + mainColor + ";")

        self.setWindowTitle(appName)
        self.setGeometry(0,0,windowWidth,windowHeight) # the first 2 argurements are the pos of the top left corner of the window
        self.setWindowIcon(QIcon(appIconImageLink))

        

        self.initUI()

    def initUI(self):

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        #region setup
        global topBar
        global graphScreen
        global cellEditorScreen
        
        topBar = QWidget(self)
        graphScreen = graphCanvas()
        

        self.cellEditorScreenWrapper = QGroupBox()
        cellEditorScreen = QVBoxLayout()
        self.cellEditorScroll = QScrollArea()

        self.cellEditorScreenWrapper.setLayout(cellEditorScreen)
        self.cellEditorScroll.setWidgetResizable(True)
        self.cellEditorScroll.setWidget(self.cellEditorScreenWrapper)
        cellEditorScreen.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
        temp1 = cellClass("sin(x)",0)
        cellWidgetManagerId.addCellToCellEditorScreen(temp1)
        #endregion


        #CSS
        #region
        topBar.setStyleSheet("background-color: " + mainColor + ";"
                             "border-style: outset;"
                            "border-width: 2px;"
                            "border-color: " + secondaryColor + ";")
        
        # graphScreen.setStyleSheet("background-color: " + mainColor + ";"
        #                      "border-style: outset;"
        #                     "border-width: 2px;"
        #                     "border-color: " + secondaryColor + ";")
        

        #endregion
        
        #region finsih up


        topBar.setFixedHeight(int(windowHeight/10))
        

        self.editingLayout = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        # graphScreen.setFixedWidth(round(windowWidth*graphScreenWidthPercent))

        
        policy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        graphScreen.setSizePolicy(policy)


        
        self.editingLayout.addWidget(graphScreen)
        self.editingLayout.addWidget(self.cellEditorScroll)
        
        
        #make the sizing not stupid
        self.editingLayout.setSpacing(0)
        self.editingLayout.setContentsMargins(0,0,0,0)
        
        #Qt.AlignmentFlag.AlignTop
        self.mainLayout.addWidget(topBar,0)
        self.mainLayout.addLayout(self.editingLayout,1)

        self.mainLayout.setStretch(0, int(graphScreenWidthPercent*100))
        self.mainLayout.setStretch(1, int((1-graphScreenWidthPercent)*100))

        #make the sizing not stupid 2 electric boogaloo
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainLayout.setSpacing(0)
        #endregion

        self.centralWidget.setLayout(self.mainLayout)




#main logic loop 
#region

class programEventLoopThreadClass(QObject):



    def run(self):
        cell_manager.bootUpCellManager()
        
        programEventLoop(self)   

def programEventLoop(orignator):
    while(True):
        cell_manager.updateCells()






#endregion   
   
# update UI loop 
#region

class guiUpdateLoopThreadClass(QObject):
    def __init__(self):
        super().__init__()
        self.addCellToCellEditorCommuncator = addCellToCellEditorSignalEmitter()

    def emitSignalToAddCellToCellEditor(self,cell):
        self.addCellToCellEditorCommuncator.addCellToCellEditorSignal.emit(cell)


    def run(self):
        
        guiUpdateEventLoop(self)


def guiUpdateEventLoop(orignator): # i may be the orignator but ... he is the duplicator -coachwilkes 2024
    
    while(True): 
        pass

        

    
#endregion   
   


def startProgram():
    global app
    global window
    global cellWidgetManagerId
    cellWidgetManagerId = cellWidgetManager()
    app = None
    window = None

    addCellToCellEditorSignalEmitterId.addCellToCellEditorSignal.connect(cellWidgetManagerId.addCellToCellEditorScreen)

    global threadManager
    threadManager = threadController()

    app = QApplication(sys.argv)
    window = MainWindow()
    

    window.show()
    
    
    
    

    sys.exit(app.exec_())


if __name__ == "__main__": #no idea how this works it just does
    startProgram()

