
def create_rkSolver(obj_name = 'pySolver'):
    """
    bare FeaturePython with attached solver for reverse kinematic problem
    """

    obj = App.ActiveDocument.addObject('App::FeaturePython', obj_name)
    rkSolver(obj)

    # App.ActiveDocument.recompute()
    return obj

class rkSolver():
    def __init__(self, obj):
        """
        create empty solver object
        all parameters and communication goes via Properties
        """

        self.Type = 'rkSolver'
        obj.Proxy = self


        # properties
        grp = 'solver'

        # model in ref: str
        # e.g 'spreadsheetFooBar'
        obj.addProperty("App::PropertyString", "ModelInRef", grp,
            'the sheet ( or whatsever) that href(reads) model input and gets touched to start recompute')

        # model out ref: str
        # the context&object to get target placement from; e.g. 'GPattach007.Local_CS009'
        obj.addProperty("App::PropertyString", "ModelOutRef", grp,
            'the context&object to get target placement from; e.g Part_foo.LCS_bar')


        # target plc
        obj.addProperty("App::PropertyPlacement", "TargetPlacement", grp,
            'the placement of model tip where it should be moved to by the solver')

        # start vector
        obj.addProperty("App::PropertyPythonObject", "StartVector", grp,
            'initial Value of model input for the solver to start')

        # model in vector
        # access with href() to keep solver out of DAG
        obj.addProperty("App::PropertyPythonObject", "ModelInVector", grp,
            'model input vector as supplied by the solver - read only')

        # model out plc
        obj.addProperty("App::PropertyPythonObject", "ModelOutPlacement", grp,
            'model input vector as supplied by the solver - read only')

        # characteristic length (to scale pos rel to normed quaternion)
        obj.addProperty("App::PropertyDistance", "Clen", grp,
            'characteristic dimension of the target property to align scaling to 0...1 as of rot quaternion components')

        # ============~~~~~~~–-------------------------


    # def onChanged(self, obj, prop):
    #     # self.execute(obj) # triggers endless recalc loop
    #     try:
    #         # prints "<App> Document.cpp(2705): Recursive calling of recompute"
    #         # but result looks fine
    #         App.ActiveDocument.recompute()
    #     except:
    #         print('App.ActiveDocument.recompute() failed')

    def onDocumentRestored(self, obj):
        obj.Proxy = self
        # self.execute(obj)
        # pass

    def execute(self, obj):
        """
        Called on document recompute
        """
        print('Recomputing {0:s} ({1:s})'.format(obj.Name, self.Type))
        #
        surveilland = obj.inspectedObject
        if not surveilland:
            print('no object for inspection selected')
            obj.Label=obj.Name
        else:
            obj.Label='GPinsp_' + surveilland.Label
            paramDict = sync_GPParams(obj, surveilland)
            print ('paramDict:', paramDict)
            prefix='' # valid for singleton links
            for so in paramDict.keys():
                pg_prm = paramDict[so]
                path = prefix + so  #  so.rstrip('.')
                plc = surveilland.getSubObject(path, retType = 3)
                prop = getattr(obj, pg_prm)
                print("checker: so, pg_prm , prop, path, plc:",so, pg_prm , prop, path, plc)
                if plc:
                    # direct assignment of plc does not work
                    setattr(obj, pg_prm, plc.Matrix)
