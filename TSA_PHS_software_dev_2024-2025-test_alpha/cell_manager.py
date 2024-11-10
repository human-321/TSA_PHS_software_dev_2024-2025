import sympy
from PyQt5 import *

global cellList
cellList = []


def addEmptycell():
    newCell = cell("",len(cellList))
    newCell.setCellContent("")
    newCell = cellList.append(newCell)
    return newCell
    

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

    def getCellContent(self):
        return self.cellContent
    
    def getCellIndex(self):
        try: self.cellIndex = cellList.index(self)
        except: pass
        return self.cellIndex
    
    def setRenderCell(self,render):
        self.cellRenderingData.renderCell = render

    def getRenderCell(self):
        return self.cellRenderingData.renderCell

        
        
class cellRenderData:
    def __init__(self,renderCell):
        self.renderCell = renderCell
        self.renderColor =  '#ff0000'
    

def getCellContent(cell:cell):
    return cell.cellContent

def getCellIndex(cell:cell):
    return cell.cellIndex

def addCellToBottom(contents: str):
   newCell = cell(contents,len(cellList))
   cellList.append(newCell)
   return newCell


def checkIfGraphNeedUpdating():
    needUpdating = False


    for j in cellList:
        original_content = j.getCellContent()
        j.setContentToCellWidgetContent()
        new_content = j.getCellContent()

        if not original_content == new_content: needUpdating = True

    return needUpdating


def deleteCell(cell:cell):
    try:
        updateCells()
        cellList.pop(cell.getCellIndex())
        # del cell.cellRenderingData
        # del cell

    except:
        pass
