import PyQt5.QtGui
from PyQt5.QtGui import QPainter, QColor
import sympy
import PyQt5
import numpy
import math
from sympy import *

global xChangePerPixel
xChangePerPixel = .1
global yChangePerPixel
yChangePerPixel = .1

# global xDetail
# xDetail = 100

x = sympy.symbols('x')



def removeSpaces(string):
    output = ""
    for i in range(len(string)):
        if(string[i] != " "): output += string[i]
    return output

def continuityTest(exper,xVal):
    check = sympy.limit(exper,x,xVal)
    return check == exper.subs(x,xVal)


def getListOfDrawListsForAnExplictFunction(string,widthPixel,heightPixel,graphCamCenter):
    output = []
    expression = sympy.sympify(removeSpaces(string))
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
    for k in range(0,len(verticeList),1):
        result = convertPointToPixelPoint(widthPixel,heightPixel,graphCamCenter,verticeList[k])

        output.append(result)


    return output



def loopThroughXVals(expression,startIndex,widthPixel,graphCamCenter):
    pureVerticeList = []
    startX = graphCamCenter[0] - (widthPixel/2) * xChangePerPixel
    func = sympy.lambdify(x,expression)

    for i in range(startIndex,widthPixel+1,1):
        xVal = startX + ((i) * xChangePerPixel)
        if(continuityTest(expression,xVal)):
            pureVerticeList.append([xVal,func(xVal)])
        else:
            return [pureVerticeList,i]
    
    return [pureVerticeList,i]

def convertPointToPixelPoint(widthPixel,heightPixel,graphCamCenter,point):

   
    vertex = point
    displacmentVector = [graphCamCenter[0] - vertex[0] , graphCamCenter[1] - vertex[1]]#numpy.array(graphCamCenter) - numpy.array(vertex)
    # convert to pixel
    displacmentVector[0] /= xChangePerPixel
    displacmentVector[1] /= yChangePerPixel
    displacmentVector[0] = round(displacmentVector[0])
    displacmentVector[1] = round(displacmentVector[1])
    # now add the displacment back
    center = [round(widthPixel/2),round(heightPixel/2)]
    point = [center[0] + displacmentVector[0]  , center[1] - displacmentVector[1]]
    #TODO clamp pixel coords to screen cuz it will probably fuck up Qpainter
        

    
    return point


print('\n\n\n\n\n')
print(getListOfDrawListsForAnExplictFunction("1/x",25,25,[0,0]))
# print(loopThroughXVals(sympy.sympify("1/x"),0,50,[0,0]))
print('\n\n\n\n\n')
