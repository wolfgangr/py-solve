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

    return (doc, sheet, prop_subpath)



# wraps acces to FC model via spreadsheet properties
#    to flat python callable format
#   input:  model input, i.e. written to sheet, property outside sheet
#       supposedly a vector i.e. List or tuple
#   output: model output, i.e. read from sheet, may be property or cell
#       supposedly a placement

class wrapModel:

    def __init(self, input: str, output: str, clen=1):

        self.idoc, self.iSheet, self.iPropName = parsePropPath(input)
        self.odoc, self.oSheet, self.oPropName = parsePropPath(output)
        self.clen = clen # normalize placement to match ~ quaternion components < 1


    def callModel(vect_in):
        # sheet.addProperty('App::PropertyPythonObject', 'D8' )
        # setattr(sheet, 'D8', propD8)
        setattr(self.isheet, self.iPropName, vect_in)

        self.idoc.recompute()
        if self.idoc not == self.odoc:
            self.odoc.recompute()

        # propD8 = sheet.getPropertyByName('D8')
        plc  = self.osheet.getPropertyByName(self.oPropName)
        base = plc.Base
        rotq = plc.Rotation.Q
        rv = list(base / self.clen)
        rv.extend(rotq)
        return rv




def solveRevKin(*args):
    # print(args)
    print("real dummy for reverse kinematic solver")
    pprint.pprint(args)

    doc = FreeCAD.ActiveDocument



# hm .... das geht nicht bzw. bleibt da nicht ....
# muß wohl aus dem sheet raus....

