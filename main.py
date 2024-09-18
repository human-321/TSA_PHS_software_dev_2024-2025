import sys
import os
import time
import math
import PyQt5
import cell_manager
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-codespace"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLineEdit, QSizePolicy, QMenu, QMenuBar, QListWidget, 
                             QAbstractScrollArea)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject

#region
#colros
mainColor = "#636363"
secondaryColor = "#694c4c"


#dependices pyqt5 sympy pylatex latex2sympy  ?aspose-tex-net

#endregion

#region


#TODO -------------------     look at https://docs.aspose.com/tex/python-net/latex-to-image/  ---------------------


print("\n\n\n\n\n")
appName = "TSA PHS software devleopment submission"
appIconImageLink = "assets\images\sigma.png"
MinWindowWidth = 500
MinWindowHeight = 500
windowWidth = MinWindowWidth
windowHeight = MinWindowHeight
graphScreenWidthPercent = .5
#endregion

#if you run this file on the codespace nothing will appear but it will sill work just without visuals
#if you want to see stuff download this locally with it's dependcies and run it

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
        self.guiworker = guiUpdateLoopThreadClass()

        self.guiUpdateLoopThread  = QThread()

        self.setupForeverThread(self.guiworker, self.guiUpdateLoopThread)

        #endregion


    def setupForeverThread(self, paramworker, paramthread): 
        



        paramworker.moveToThread(paramthread) #this is fine

        paramthread.started.connect(paramworker.run)
        paramthread.start()

        


#ui
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

        global topBar
        global graphScreen
        global graphScreenIndex
        global cellEditorScreen
        topBar = QWidget(self)
        graphScreen = QLabel("#2",self)
        cellEditorScreen = QListWidget(self)

        #CSS
        #region
        topBar.setStyleSheet("background-color: " + mainColor + ";"
                             "border-style: outset;"
                            "border-width: 2px;"
                            "border-color: " + secondaryColor + ";")
        
        graphScreen.setStyleSheet("background-color: " + mainColor + ";"
                             "border-style: outset;"
                            "border-width: 2px;"
                            "border-color: " + secondaryColor + ";")
        
        cellEditorScreen.setStyleSheet("background-color: " + mainColor + ";"
                             "border-style: outset;"
                            "border-width: 2px;"
                            "border-color: " + secondaryColor + ";")
        #endregion
        
        topBar.setMinimumHeight(int(windowWidth/10))
        cellEditorScreen.setMinimumWidth(0)
        self.editingLayout = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        graphScreen.setFixedWidth(round(windowWidth*graphScreenWidthPercent))
        
        self.editingLayout.addWidget(graphScreen)
        self.editingLayout.addWidget(cellEditorScreen)
        
        self.mainLayout.addWidget(topBar,0)
        self.mainLayout.addLayout(self.editingLayout,1)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        
        self.centralWidget.setLayout(self.mainLayout)
        


#main logic loop 
#region

class programEventLoopThreadClass(QObject):

    def run(self):
        cell_manager.bootUpCellManager()
        
        programEventLoop()   

def programEventLoop():
    cell_manager.bootUpCellManager()
    t=0

    while(True):
        #sigma
        t += 1


    
    
#endregion   
   
# update UI loop 
#region

class guiUpdateLoopThreadClass(QObject):
    
    def run(self):
        
        guiUpdateEventLoop()

def guiUpdateEventLoop():

    while(True): 
        #round(windowWidth*graphScreenWidthPercent)

        if(window.editingLayout):
            graphlayout = window.editingLayout.itemAt(0)

            graphlayout.widget().setFixedWidth(round(window.width()*graphScreenWidthPercent))


        #str((windowWidth,windowHeight))

    
    
#endregion   
   


def startProgram():
    global app
    global window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    global threadManager
    threadManager = threadController()

    sys.exit(app.exec_())


if __name__ == "__main__": #no idea how this works it just does
    startProgram()


