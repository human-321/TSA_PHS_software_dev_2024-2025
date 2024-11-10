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

def convertPointsToQLines(pointList):
    lineList = []
    #this is a general function to convert our pixel coords to qlines for the q painter to draw
    for i in range(len(pointList)-1):
        point = pointList[i]
        nextPoint = pointList[i+1]
        
        pointGui = PyQt5.QtCore.QPoint(point[0],point[1])
        nextPointGui = PyQt5.QtCore.QPoint(nextPoint[0],nextPoint[1])

        lineList.append(PyQt5.QtCore.QLineF(pointGui,nextPointGui))

    return lineList


#endregion

#region explict functions

def getListOfTrueVerticesForExplict(string,startX,endX):
    output = []
    expression = sympy.sympify(removeSpaces(string))
    func = sympy.lambdify(x,expression)


    # rangeX = math.floor((widthPixel)/xChangePerPixel)
    
    # this is very fuckius wuckius a gagius maggotus something the the ello govna car from the regular show episode 1 season 2 would disapprove of
    # we are doing this to account for function inconitnuitys doesnt't even do that correctly right now but thats is a fix for tomarrow
    # we are basically looping through the values and if there is a inconitniuity we are starting a new sublist
    # when we will inevidently draw this we will loop thorough the sub lists for the qpainter
    verticeList = loopThroughXVals('x',startX,endX)
        
    return verticeList



def loopThroughXVals(expression,startX,endX):
    pureVerticeList = []
    func = sympy.lambdify(x,expression)


    i = startX
    while i < endX:
        xVal = startX + ((i) * xChangePerPixel)
        pureVerticeList.append([xVal,func(xVal)])
        i += 1

    
    return pureVerticeList



# def convertPointToPixelPoint(widthPixel,heightPixel,graphCamCenter,point):

   
#     vertex = point
#     displacmentVector = [vertex[0] - graphCamCenter[0],vertex[1] - graphCamCenter[0]]#numpy.array(graphCamCenter) - numpy.array(vertex)
#     # convert to pixel
#     displacmentVector[0] /= xChangePerPixel
#     displacmentVector[1] /= yChangePerPixel
#     displacmentVector[0] = round(displacmentVector[0])
#     displacmentVector[1] = round(displacmentVector[1])
#     # now add the displacment back
#     center = [round(widthPixel/2),round(heightPixel/2)]
#     point = [center[0] + displacmentVector[0]  , center[1] + displacmentVector[1]]
#     #TODO clamp pixel coords to screen cuz it will probably fuck up Qpainter
#     point[0] = clamp(point[0],0,widthPixel)
#     point[1] = clamp(point[1],0,heightPixel)

    
#     return point

#endregion



print(getListOfTrueVerticesForExplict("x",-5,5))