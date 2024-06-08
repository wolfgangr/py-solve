import FreeCAD

import numpy as np
from scipy.optimize import fsolve
# https://realpython.com/python-pretty-print/
import pprint
import re

def dummy(*args):
    # print(args)
    print("dummy for reverse kinematic solver")
    pprint.pprint(args)




# =Unnamed#pySheet.cpy_res_posTip
def parsePropPath( proppath , default_sheet = 'pySheet'):
    match = re.match(r"^(([\w]+)(#))?(([\w]+)(\.))?([\w]+)$", proppath)
    if not match:
        print(f"canot parse property path: {proppath}")
        return None

    print ("match.groups(): ", match.groups())
    docpath = match.groups()[1]
    sheetpath = match.groups()[4]
    prop_subpath = match.groups()[6]

    if docpath:
        doc = FreeCAD.getDocument(docpath)
    else:
        doc = FreeCAD.ActiveDocument

    if not sheetpath:
        sheetpath = default_sheet
    sheet = doc.getObject(sheetpath)

    return (doc, sheet, prop_subpath)



# wraps acces to FC model via spreadsheet properties
#   to flat python callable format
#   input:  model input, i.e. written to sheet, property outside sheet
#       supposedly a vector i.e. List or tuple
#   output: model output, i.e. read from sheet, may be property or cell
#       supposedly a placement
#   target: target placement to be substracted (or whatever) since solver
#       targets to all over zeros
#  hangon .. can the quaternions be zero at all? better go for euler angles??

class wrapModel:

    def __init__(self, input: str, output: str,
                target: FreeCAD.Placement = None, clen: float =1 ):

        self.iDoc, self.iSheet, self.iPropName = parsePropPath(input)
        self.oDoc, self.oSheet, self.oPropName = parsePropPath(output)
        self.clen = clen # normalize placement to match ~ quaternion components < 1

        if target:  # calc the inverse only once on instantiation
            self.iTarget = target.inverse()
        else:       # zero target inverts to itself
            self.iTarget = FreeCAD.Placement()



    def callModel(self, vect_in):
        # sheet.addProperty('App::PropertyPythonObject', 'D8' )
        # setattr(sheet, 'D8', propD8)
        setattr(self.iSheet, self.iPropName, vect_in)

        self.iDoc.recompute()
        if not self.iDoc == self.oDoc:
            self.oDoc.recompute()

        # propD8 = sheet.getPropertyByName('D8')
        plc  = self.oSheet.getPropertyByName(self.oPropName)

        ## TBD ---- current.multiply(inverse(target))
        # solver approaches all zeroes!
        dPlc = plc.multiply(self.iTarget)

        base = dPlc.Base
        ypr = dPlc.Rotation.getYawPitchRoll()
        rv = list(base / self.clen)
        rv.extend(ypr)
        return rv


# # reverse kinematic solver
# 'solve reverse kinematic placement
# - target placement
# - start vector(List)
# - location to write model input (string of name)
# - location to read model output (string of name)
# - characteristic length (scales offsets down to ~ as rot values)


def solveRevKin(target:FreeCAD.Placement, startVec: list[float],
                    input: str, output: str, cLen:float = 1):
    # print(args)
    print("target, startVec, input, output, cLen:")
    print(target, startVec, input, output, cLen)

    model = wrapModel(input, output, target, cLen)

    solutionInfo=fsolve(model.callModel, startVec, full_output=1)

    pprint.pprint(solutionInfo)

    # pprint.pprint(target, startVec, input, output, cLen)

    # doc = FreeCAD.ActiveDocument

    # solutionInfo=fsolve(nonlinearEquation,initialGuess,full_output=1)





