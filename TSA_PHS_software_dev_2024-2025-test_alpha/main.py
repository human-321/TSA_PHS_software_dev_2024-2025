import sys
import os
import time

import math
import random
import PyQt5
import PyQt5.Qt
import PyQt5.QtRemoteObjects
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import cell_manager
from cell_manager import cell as cellClass
# from  Qt import AlignmentFlag
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-codespace"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLineEdit, QSizePolicy , QScrollArea,QGroupBox, QLabel)
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QSize
import numpy
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
# from sympy import *
from matplotlib.figure import Figure
from numpy import *
#Qt.AlignmentFlag
#if you run this file on the codespace nothing will appear but it will sill work just without visuals
#if you want to see stuff download this locally with it's dependcies and run it



#colors

#region
#colros
cellRandomColors = ['#ff0d05','#fcba03','#f605fa','#05e1fa','#05fa67','#070800','#d9fa05','#5bfa13']

mainColor = "#636363"
secondaryColor = "#694c4c"

graphScreenColor = '#faf5f5'

cellTextColor = '#ebaba7'
cellTextBorderColor = '#4f2e2b'
cellTextEditAreaBorderColor = secondaryColor

# button
addCellButtonBorderColor = mainColor

#dependices pyqt5 numpy matplotlib

#endregion

#decalre vars
#region


#TODO -------------------     look at https://docs.aspose.com/tex/python-net/latex-to-image/  ---------------------


start = time.time()
print("\n\n\n\n\n")
appName = "TSA PHS software devleopment submission"
appIconImageLink = "assets\images\sigma.png"
MinWindowWidth = 1500
MinWindowHeight = 500
windowWidth = MinWindowWidth
windowHeight = MinWindowHeight
graphScreenWidthPercent = .5

cellEditorScreenItemHeight = 25

def clamp(minimum,maximum,val):
    return max(min(val,maximum),minimum)


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

class updateGraphSignalEmitter(QObject):
    updateGraphSignal = pyqtSignal()

global updateGraphSignalEmitterId
updateGraphSignalEmitterId = updateGraphSignalEmitter()


class cellWidgetManager(QObject):


    def __init__(self):
        super().__init__()
        self.myCellWidgets = []
        # self.myCellWidgetsObjects = []
        
    

    def addCellToCellEditorScreen(self,cell : cellClass):
        
        

        
        self.myCellWidgets.append(cellWidget(cell,self))




class cellWidget(QObject):

    def __init__(self,cell:cellClass,trueParent:cellWidgetManager):
        self.trueParent = trueParent
        super().__init__()
        self.lineEditStyle = 'color: {0}; border: 2px solid {1};'.format(cellTextColor,cellTextBorderColor)
        self.cellEditHolder = QHBoxLayout()
        self.settingsShow = False

        self.myCell = cell
        

        # delete button

        #region
        self.cellWidgetDeleteButton = QPushButton()
        #  𝕏  ✗
        self.cellWidgetDeleteButton.setText("✗")
        self.cellWidgetDeleteButton.setFont(QFont('Times',15))
        self.cellWidgetDeleteButton.setFixedHeight(cellEditorScreenItemHeight)

        self.cellWidgetDeleteButton.clicked.connect(self.deleteMyself)

        

        #endregion



        #cell settings panel
        #region
        self.cellSettingsButton = QPushButton()
        # S  ⋮
        self.cellSettingsButton.setText('{0}⋮{0}'.format(''))
        self.cellSettingsButton.setFont(QFont('Times',25))
        self.cellSettingsButton.setFixedHeight(cellEditorScreenItemHeight)


        self.cellSettingsButton.clicked.connect(self.cellSettingsClicked)


        self.cellSettingsEditPanel = cellSettingsEditPanel(self)
        #endregion



        # line edit
        #region
        self.cellWidgetLineEdit = QLineEdit()
        self.cellWidgetLineEdit.setText(cell_manager.getCellContent(cell))
        self.cellWidgetLineEdit.setFixedHeight(cellEditorScreenItemHeight)
        self.cellWidgetLineEdit.setStyleSheet(self.lineEditStyle)

        cell.setCellWidget(self.cellWidgetLineEdit)
        #endregion


        #hack solution
        self.deleteList = [self.cellWidgetLineEdit,self.cellWidgetDeleteButton,self.cellEditHolder,self.cellSettingsEditPanel,self.cellSettingsButton,self]

        


        #layout shit
        #region
        self.cellEditHolder.addWidget(self.cellWidgetDeleteButton, alignment=PyQt5.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.cellEditHolder.addWidget(self.cellSettingsButton, alignment=PyQt5.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.cellEditHolder.addWidget(self.cellWidgetLineEdit)

        self.cellEditHolder.setContentsMargins(0,0,0,0)
        self.cellEditHolder.setSpacing(1)

        #endregion
        cellEditorScreen.addLayout(self.cellEditHolder)



    def cellSettingsClicked(self):
        self.settingsShow = not self.settingsShow
        if(self.settingsShow): self.cellSettingsEditPanel.open()
        else: self.cellSettingsEditPanel.close()
    
    def deleteMyself(self):
        
        


        try:cellEditorScreen.removeItem(cellEditorScreen.indexOf(self.cellEditHolder))
        except: pass

        for thing in self.deleteList:  thing.deleteLater()
        
        cell_manager.deleteCell(self.myCell)
        cellWidgetManagerId.myCellWidgets.pop(cellWidgetManagerId.myCellWidgets.index(self))
        

        updateGraphSignalEmitterId.updateGraphSignal.emit()
        # self.deleteLater()


class cellSettingsEditPanel(QWidget):
    def __init__(self,cellWidgetInstance : cellWidget):
        super().__init__()
        self.sizeMin = [300,100]
        self.setMinimumSize(QSize( self.sizeMin[0] , self.sizeMin[1] )   )
        self.widgetOwner = cellWidgetInstance

        self.settingsMainLayout = QVBoxLayout()
        # bullshit that is needed to get settings to scroll that doesn't even work
        #region
        self.settingsGroupBox = QGroupBox()
        self.settingsScroll = QScrollArea()

        self.settingsGroupBox.setLayout(self.settingsMainLayout)
        self.settingsScroll.setWidget(self.settingsGroupBox)
        self.settingsScroll.setWidgetResizable(True)
        self.settingsScroll.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.settingsMainLayout.sizeHint
        #endregion
        


        # some other bullshit that is needed in order to actually have the settings to scroll for whatever reason
        #region
        policy = QSizePolicy.Policy.Expanding
        # self.settingsGroupBox.setSizePolicy(policy,policy)
        self.settingsScroll.setSizePolicy(policy,policy)
        # self.setSizePolicy(policy,policy)
        # self.
        self.setLayout(QHBoxLayout(self))
        self.layout().addWidget(self.settingsScroll)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        #endregion



        #check box
        #region

        self.settingsGraphCellLayout = QHBoxLayout()
        self.settingsGraphCellLabel = QLabel()
        self.settingsGraphCellLabel.setText('graph this cell')
        self.settingsGraphCellCheckBox = PyQt5.QtWidgets.QCheckBox()

        self.settingsGraphCellCheckBox.setChecked(self.widgetOwner.myCell.cellRenderingData.renderCell)
        self.settingsGraphCellCheckBox.clicked.connect(self.settingsGraphCellCheckBoxCLicked)

        self.settingsGraphCellLayout.addWidget(self.settingsGraphCellLabel,alignment=Qt.AlignmentFlag.AlignLeft)
        self.settingsGraphCellLayout.addWidget(self.settingsGraphCellCheckBox,alignment=Qt.AlignmentFlag.AlignLeft)

        self.settingsGraphCellLayout.setSpacing(0)
        self.settingsGraphCellLayout.setContentsMargins(0,0,0,0)
        self.settingsGraphCellLayout.setStretch(0,1)
        self.settingsGraphCellLayout.setStretch(1,2)
        self.settingsMainLayout.addLayout(self.settingsGraphCellLayout)


        #endregion

        #color enter
        #region

        self.settingsCellRenderColorLayout = QHBoxLayout()
        self.settingsCellRenderColorLabel = QLabel()
        self.settingsCellRenderColorLabel.setText('cell render color')
        self.settingsCellRenderColorTextEdit = QLineEdit()

        # self.settingsGraphCellCheckBox.setChecked(self.widgetOwner.myCell.cellRenderingData.renderCell)
        self.settingsCellRenderColorTextEdit.setText(self.widgetOwner.myCell.cellRenderingData.renderColor)
        #TODO add color editing

        self.settingsCellRenderColorLayout.addWidget(self.settingsCellRenderColorLabel,alignment=Qt.AlignmentFlag.AlignLeft)
        self.settingsCellRenderColorLayout.addWidget(self.settingsCellRenderColorTextEdit,alignment=Qt.AlignmentFlag.AlignLeft)

        self.settingsCellRenderColorLayout.setSpacing(0)
        self.settingsCellRenderColorLayout.setContentsMargins(0,0,0,0)
        self.settingsCellRenderColorLayout.setStretch(0,1)
        self.settingsCellRenderColorLayout.setStretch(1,2)
        self.settingsMainLayout.addLayout(self.settingsCellRenderColorLayout)




        #endregion

    def settingsCellRenderColorTextEditUpdate(self):
        self.widgetOwner.myCell.cellRenderingData.renderColor = self.settingsCellRenderColorTextEdit.text()
        self.updateGraph()

    def settingsGraphCellCheckBoxCLicked(self):
        self.widgetOwner.myCell.setRenderCell(self.settingsGraphCellCheckBox.isChecked())
        self.updateGraph()

    def updateGraph(self): #It takes too damn long to type something i use constantly
        updateGraphSignalEmitterId.updateGraphSignal.emit()

    def open(self):
        try: self.setWindowTitle('cell ' + str(self.widgetOwner.myCell.getCellIndex() + 1) + " settings editor")
        except: pass
        self.show()

    def close(self):
        self.hide()

    def closeEvent(self,event):
        self.widgetOwner.settingsShow = False
        event.accept()



#endregion


#useful stuff
#region
# def is_valid_python(code):
#     try:
#         ast.parse(code)
#         return True
#     except SyntaxError:
#         return False

def makeCellToLineEdit(cell):

    newLineEdit = QLineEdit()
    newLineEdit.setText(cell_manager.getCellContent(cell))
    return newLineEdit

def clearLayout(layout):
    for i in reversed(range(layout.count())):
        layout.removeItem(layout.itemAt(i))


#endregion




#ui
class graphCanvas(FigureCanvas):
    def __init__(self,parent=None):
        self.xRange = 20
        self.yRange = 13
        self.graphCamCenter = [0,0]
        self.detail = 250
        self.changeTolerance = .99
        self.limitStep = .1

        self.Dpi = 100
        self.fig = Figure(figsize=(5,4),dpi=self.Dpi)
        self.ax = self.fig.add_subplot()

        super().__init__(self.fig)
        self.setParent(parent)

        self.reset_axies()


    def reset_axies(self):
        self.ax.cla()
        self.fig.set_facecolor(graphScreenColor)
        self.ax.set_facecolor(graphScreenColor)
        self.ax.set_xlim(-self.xRange/2  + self.graphCamCenter[0],self.xRange/2  + self.graphCamCenter[0])
        self.ax.set_ylim(-self.yRange/2 + self.graphCamCenter[1],self.yRange/2 + self.graphCamCenter[1])
        self.ax.grid()
        self.ax.axhline(y=0,color = '#030303')
        self.ax.axvline(x=0,color = '#030303')
        

    # def panGraph(self,event):




    def funcValFromString(self,funcString,x):
        
        return eval(funcString)



    def drawPlot(self,func,renderSettings: cell_manager.cellRenderData):
        
        # collection = cell_grapher.getListOfTrueVerticesForExplict(func,int(self.ax.get_xbound()[0]),int(self.ax.get_xbound()[1]))
        try:
            original_input_vals = numpy.linspace(-self.xRange/2 + self.graphCamCenter[0],self.xRange/2 + self.graphCamCenter[0],self.detail)
            step = self.xRange/self.detail

            input_vals = []
            output_vals = []

            current_output_list = []
            current_input_list = []
            
            for i in original_input_vals:


                isValid = False
                #basic incontinuity
                try:
                    val = self.funcValFromString(func,i)
                    isValid = True
                except:
                    isValid = False

                #semi discontinouty test
                try:
                    leftSide = (self.funcValFromString(func,i-step))
                    rightSide = (self.funcValFromString(func,i+step ))
                    scuffedLimit = (leftSide + rightSide)/2
                    if abs(val - scuffedLimit) > self.changeTolerance:
                        isValid = False
                except:
                    isValid = False
                
                
                if not isValid:
                    #make a new draw batch
                    output_vals.append(current_output_list)
                    input_vals.append(current_input_list)
                    current_output_list = []
                    current_input_list = []
                else:
                    #add to current batch
                    current_output_list.append(val)
                    current_input_list.append(i)

            output_vals.append(current_output_list)
            input_vals.append(current_input_list)

            for j in range(len(output_vals)):
                self.ax.plot(input_vals[j],output_vals[j],renderSettings.renderColor)
            



        except:
            pass
            # print('fucka you')

    
    def redrawAllCells(self):
        self.reset_axies()
        cell_manager.updateCells()

        for i in cellWidgetManagerId.myCellWidgets:
            i = i.myCell
            if(i.getCellContent() != '' and i.getRenderCell()):
                self.drawCell(i)
                # print(str(i.getCellIndex())+ " " + str(i.myCellWidget.text()))
            

        self.fig.canvas.draw()





    def drawCell(self,cell):
        func = cell.getCellContent()
        self.drawPlot(func,cell.cellRenderingData)

        
    def updateSize(self):
        pass


        


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

        self.timer = PyQt5.QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(graphScreen.redrawAllCells)
        self.timer.start()

    def initUI(self):

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        #region setup
        global topBar
        global graphScreen
        global cellEditorScreen
        
        topBar = QHBoxLayout(self)
        graphScreen = graphCanvas(self)
        

        self.cellEditorScreenWrapper = QGroupBox()
        cellEditorScreen = QVBoxLayout()
        self.cellEditorScroll = QScrollArea()

        self.cellEditorScreenWrapper.setLayout(cellEditorScreen)

        self.cellEditorScreenWrapper.setStyleSheet('border: 1px solid ' + cellTextEditAreaBorderColor +';')

        self.cellEditorScroll.setWidgetResizable(True)
        self.cellEditorScroll.setWidget(self.cellEditorScreenWrapper)
        cellEditorScreen.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
        self.addEmptyCellComplete()

        #button to add more cells
        self.addCellButton = QPushButton()
        self.addCellButton.setFixedHeight(int(windowHeight/10))
        self.addCellButton.setText('Add Cell')
        # self.addCellButton.setStyleSheet('border: 1px solid ' + addCellButtonBorderColor + ';')

        self.addCellButton.clicked.connect(self.addEmptyCellComplete)

        topBar.addWidget(self.addCellButton, alignment=PyQt5.QtCore.Qt.AlignmentFlag.AlignRight)

        #endregion

        
        #region finsih up


        self.editingLayout = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        policy = QSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        otherPolicy = QSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.cellEditorScroll.setSizePolicy(otherPolicy)
        

        self.editingLayout.addWidget(graphScreen)
        self.editingLayout.addWidget(self.cellEditorScroll)
        
        #make the sizing not stupid
        self.editingLayout.setSpacing(0)
        self.editingLayout.setContentsMargins(0,0,0,0)
        
        #Qt.AlignmentFlag.AlignTop
        self.mainLayout.addLayout(topBar,0)
        self.mainLayout.addLayout(self.editingLayout,1)

        self.editingLayout.setStretch(0, int(graphScreenWidthPercent*100))
        self.editingLayout.setStretch(1, int((1-graphScreenWidthPercent)*100))

        #make the sizing not stupid 2 electric boogaloo
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainLayout.setSpacing(0)
        #endregion

        self.centralWidget.setLayout(self.mainLayout)


    def addEmptyCellComplete(self):
        temp2 = cellClass('',0)
        temp2.getCellIndex() # funny enough this updates the index
        temp2.cellRenderingData.renderColor = cellRandomColors[random.randint(0,len(cellRandomColors) - 1)]
        cellWidgetManagerId.addCellToCellEditorScreen(temp2)


#main logic loop 
#region

class programEventLoopThreadClass(QObject):



    def run(self):
        cell_manager.bootUpCellManager()
        
        programEventLoop(self)   

def programEventLoop(orignator):
    pass
    # global seconds
    # seconds = 0
    # while(True):
    #     time.sleep(.01)
    #     seconds = time.time() - start
    #     # cell_manager.updateCells()






#endregion   
   
# update UI loop 
#region


class guiUpdateLoopThreadClass(QObject):
    def __init__(self):
        super().__init__()
        self.addCellToCellEditorCommuncator = addCellToCellEditorSignalEmitter()
        self.updateGraphCommuncator = updateGraphSignalEmitterId

    def emitSignalToAddCellToCellEditor(self,cell):
        self.addCellToCellEditorCommuncator.addCellToCellEditorSignal.emit(cell)

    def emitSignalUpdateGraph(self):
        self.updateGraphCommuncator.updateGraphSignal.emit()


    def run(self):
        
        self.guiUpdateEventLoop()


    def guiUpdateEventLoop(self): # i may be the orignator but ... he is the duplicator -coachwilkes 2024
        pass
        # while(True): 
        #     time.sleep(.1)
        #     # if(cell_manager.checkIfGraphNeedUpdating()): self.emitSignalUpdateGraph()

        

    
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
    
    updateGraphSignalEmitterId.updateGraphSignal.connect(graphScreen.redrawAllCells)
    updateGraphSignalEmitterId.updateGraphSignal.emit()

    window.show()
    
    # updateGraphSignalEmitterId.updateGraphSignal.connect(graphScreen.func)
    
    

    sys.exit(app.exec_())


if __name__ == "__main__": #no idea how this works it just does
    startProgram()


