import PyQt5.QtCore
import PyQt5.QtGui
from PyQt5.QtGui import QPainter, QColor
import sympy
import PyQt5
import math
from sympy import *

global xChangePerPixel
xChangePerPixel = .1
global yChangePerPixel
yChangePerPixel = .1

# global xDetail
# xDetail = 100

x = sympy.symbols('x')

#region useful funcs
def clamp(n,min,max):
    if(n < min): return min
    if(n > max): return max
    return n

def removeSpaces(string):
    output = ""
    for i in range(len(string)):
        if(string[i] != " "): output += string[i]
    return output

def continuityTest(exper,xVal):
    check = sympy.limit(exper,x,xVal)
    return check == exper.subs(x,xVal)

def convertPointsToQPath(pointList):
    print('func 4 start \n')
    guiPointList = []
    path = PyQt5.QtGui.QPainterPath()
    #this is a general function to convert our pixel coords to qlines for the q painter to draw
    for i in range(len(pointList)):
        point = pointList[i]
        pointGui = PyQt5.QtCore.QPoint(point[0],point[1])
        guiPointList.append(pointGui)


    if(guiPointList): # weird ass way of saying the list aint empty
        path.moveTo(guiPointList[0])

        for point in guiPointList[1:]: # weird ass way of saying forgett bout it the first item in the list
            path.lineTo(point)
        
    print('func 5 end \n')
    return path


#endregion

#region explict functions
def explictFunctionGetQPath(string,widthPixel,heightPixel,graphCamCenter):
    return convertPointsToQPath(getListOfDrawListsForAnExplictFunction(string,widthPixel,heightPixel,graphCamCenter))


def getListOfDrawListsForAnExplictFunction(string,widthPixel,heightPixel,graphCamCenter):
    print('func 1 start \n')
    output = []
    expression = sympy.sympify(string)
    func = sympy.lambdify(x,expression)

    startX = graphCamCenter[0] - (widthPixel/2) * xChangePerPixel
    endX = graphCamCenter[0] + (widthPixel/2) * xChangePerPixel

    # rangeX = math.floor((widthPixel)/xChangePerPixel)
    
    # this is very fuckius wuckius a gagius maggotus something the the ello govna car from the regular show episode 1 season 2 would disapprove of
    # we are doing this to account for function inconitnuitys doesnt't even do that correctly right now but thats is a fix for tomarrow
    # we are basically looping through the values and if there is a inconitniuity we are starting a new sublist
    # when we will inevidently draw this we will loop thorough the sub lists for the qpainter
    verticeList = []
    for j in range(0,widthPixel+1,1):
        result = loopThroughXVals(expression,j,widthPixel,graphCamCenter)

        if(result[1] == widthPixel):
            verticeList  = result[0]
            break
        else:
            verticeList.append(result[0])
            j += result[1]
        
    #convert from magical mathmatical fantasy land coords to pixel coords
    for k in range(0,len(verticeList)-1,1):
        result = convertPointToPixelPoint(widthPixel,heightPixel,graphCamCenter,verticeList[k])

        output.append(result)

    print('func 1 end \n')
    return output



def loopThroughXVals(expression,startIndex,widthPixel,graphCamCenter):
    print('func 2 start \n')
    pureVerticeList = []
    startX = graphCamCenter[0] - (widthPixel/2) * xChangePerPixel
    func = sympy.lambdify(x,expression)

    for i in range(startIndex,widthPixel+1,1):
        xVal = startX + ((i) * xChangePerPixel)
        if(continuityTest(expression,xVal)):
            pureVerticeList.append([xVal,func(xVal)])
        else:
            return [pureVerticeList,i]
    print('func 2 end \n')
    return [pureVerticeList,i]

def convertPointToPixelPoint(widthPixel,heightPixel,graphCamCenter,point):
    print('func 3 start \n')
   
    vertex = point
    displacmentVector = [vertex[0] - graphCamCenter[0],vertex[1] - graphCamCenter[0]]#numpy.array(graphCamCenter) - numpy.array(vertex)
    # convert to pixel
    displacmentVector[0] /= xChangePerPixel
    displacmentVector[1] /= yChangePerPixel
    displacmentVector[0] = round(displacmentVector[0])
    displacmentVector[1] = round(displacmentVector[1])

    # now add the displacment back
    center = [round(widthPixel/2),round(heightPixel/2)]
    point = [center[0] + displacmentVector[0]  , center[1] - displacmentVector[1]]
    #TODO clamp pixel coords to screen cuz it will probably fuck up Qpainter
    point[0] = clamp(point[0],0,widthPixel)
    point[1] = clamp(point[1],0,heightPixel)

    print('func 3 end \n')
    return point

#endregion