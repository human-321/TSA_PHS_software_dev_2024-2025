import sympy

global cellList
cellList = []


def addEmptycell():
    newCell = cell("",len(cellList))
    newCell.setCellContent("x^2")
    newCell = cellList.append(newCell)
    

def bootUpCellManager():
    global cellList 
    cellList = []
    addEmptycell()


class cell:
    def __init__(self,contents,index):
        self.cellContent = contents
        self.cellIndex = index
        self.cellRenderingData = cellRenderData(True)

    def setCellContent(self,content):
        self.cellContent = content

    
        
        
class cellRenderData:
    def __init__(self,renderCell):
        self.renderCell = renderCell
    

def getCellContent(cell):
    return cell.cellContent

def getCellIndex(cell):
    return cell.cellIndex

def addCellToBottom(contents: str):
   newCell = cell(contents,len(cellList))
   cellList.append(newCell)
   return newCell
