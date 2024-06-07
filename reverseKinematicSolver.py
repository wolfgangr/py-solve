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


# # reverse kinematic solver
# 'solve reverse kinematic placement
# - target placement
# - start vector(List)
# - location to write model input (string of name)
# - location to read model output (string of name)
# - characteristic length (scales offsets down to ~ as rot values)

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

    return (sheet, prop_subpath)




class wrapModel:

    def __init(self, input: str, output: str):
        # self.input = input
        # self.output = output

        self.doc = FreeCAD.ActiveDocument
        self.inputProperty  = sheet.getPropertyByName(input)
        self.outputProperty = sheet.getPropertyByName(output)




def solveRevKin(*args):
    # print(args)
    print("real dummy for reverse kinematic solver")
    pprint.pprint(args)

    doc = FreeCAD.ActiveDocument


# propD8 = sheet.getPropertyByName('D8')
# sheet.addProperty('App::PropertyPythonObject', 'D8' )
# setattr(sheet, 'D8', propD8)
# >>> doc.recompute()
# hm .... das geht nicht bzw. bleibt da nicht ....
# muß wohl aus dem sheet raus....

