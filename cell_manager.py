import sympy
from PyQt5 import *

global cellList
cellList = []


def addEmptycell():
    newCell = cell("",len(cellList))
    newCell.setCellContent("")
    newCell = cellList.append(newCell)
    

def bootUpCellManager():
    global cellList 
    cellList = []

def updateCells():
    for item in cellList:
        item.setContentToCellWidgetContent()

class cell:
    def __init__(self,contents,index):
        self.cellContent = contents
        self.cellIndex = index
        self.cellRenderingData = cellRenderData(True)
        self.myCellWidget = None

        cellList.append(self)

    def setContentToCellWidgetContent(self):
        if(self.myCellWidget != None):
            self.cellContent = self.myCellWidget.text()

    def setCellWidget(self,widget):
        self.myCellWidget = widget

    def setCellContent(self,content):
        self.cellContent = content

    
        
        
class cellRenderData:
    def __init__(self,renderCell):
        self.renderCell = renderCell
    

def getCellContent(cell:cell):
    return cell.cellContent

def getCellIndex(cell:cell):
    return cell.cellIndex

def addCellToBottom(contents: str):
   newCell = cell(contents,len(cellList))
   cellList.append(newCell)
   return newCell

