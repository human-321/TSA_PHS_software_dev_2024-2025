import sympy




def addEmptycell():
    newCell = cell(len(cellList))
    newCell.setCellContent("x^2")
    newCell = cellList.append(newCell)
    

def bootUpCellManager():
    global cellList
    cellList = []
    addEmptycell()


class cell:
    def __init__(self,index):
        self.cellContent = ""
        self.cellIndex = index
        self.cellRenderingData = cellRenderData(True)

    def setCellContent(self,content):
        self.cellContent = content
        
        
class cellRenderData:
    def __init__(self,renderCell):
        self.renderCell = renderCell
    

