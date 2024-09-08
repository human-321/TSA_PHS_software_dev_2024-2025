import sys
import os
import time
import PyQt5
import cell_manager
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-codespace"
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QSizePolicy, QMenu, QMenuBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject

#region
#colros
mainColor = "#636363"
secondaryColor = "#694c4c"


#endregion



appName = "TSA PHS software devleopment submission"
appIconImageLink = "assets\images\sigma.png"
MinWindowWidth = 500
MinWindowHeight = 500
windowWidth = MinWindowWidth
windowHeight = MinWindowHeight

#if you run this file on the codespace nothing will appear but it will sill work just without visuals
#if you want to see stuff download this locally with it's dependcies and run it




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
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        global topBar
        global graphScreen
        global cellEditorScreen
        topBar = QWidget(self)
        graphScreen = QLabel("#2",self)
        cellEditorScreen = QLabel("#3",self)

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
        
        topBar.setMinimumHeight(int(windowWidth/10))
        editingLayout = QHBoxLayout()
        mainLayout = QVBoxLayout()

        
        editingLayout.addWidget(graphScreen)
        editingLayout.addWidget(cellEditorScreen)
        
        mainLayout.addWidget(topBar,0)
        mainLayout.addLayout(editingLayout,1)
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0,0,0,0)
        
        centralWidget.setLayout(mainLayout)
        


        


class programEventLoopThreadClass(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()

    def run(self):
        cell_manager.bootUpCellManager()
        
        while(True): programEventLoop()

    




def programEventLoop():
    windowWidth = window.size().width()
    windowHeight = window.size().height()
    #str((windowWidth,windowHeight))

    
    
        
   


def startProgram():
    global app
    global window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    programEventLoopThread = QThread()
    programEventLoopWorker = programEventLoopThreadClass()
    programEventLoopWorker.moveToThread(programEventLoopThread)
    programEventLoopThread.started.connect(programEventLoopWorker.run)
    programEventLoopThread.start()

    sys.exit(app.exec_())


    

if __name__ == "__main__": #no idea how this works it just does
    startProgram()


