"""
@author: Steven Verwer
@git: https://github.com/stevenverwer
"""

class Component:
    def updateIdeaParameters(self, **kw):
        output = {}
        for key, parameter in kw.items():
            if key in self.__dict__.keys():
                parameter['value'] = self.__getattribute__(key)
                output[key] = parameter
        return output



class Assembly:
    def updateIdeaParameters(self, params):
        if not isinstance(params, list):
            raise Exception(f"{params} is not a list.")
        if len(params)!=len(self.parameters):
            raise Exception(f"{params} is length {len(params)} while {len(self.parameters)} is expected.")
        for idx in range(len(self.parameters)-1):
            self.parameters[idx]['value'] = params[idx]



class Material:
    def __init__(self, name='S355'):
        self.name = name
    pass



class Bolt: # inheritance
    def __init__(self, size, grade, shearInThread):
        from ideastaticapy.datatype import paramList
        self.parameters = paramList()
        boltGrade = self.parameters.getIntFromCategoryItem('boltGrade', grade)
        boltSize = self.parameters.getIntFromCategoryItem('boltSize', size)
        self.parameters.extend([
            {'name': 'boltGrade','value': boltGrade, 'lb': 0, 'ub': 6, 'type': 'int', 'category':'boltGrade'},
            {'name': 'boltSize','value': boltSize, 'lb': 0, 'ub': 11, 'type': 'int', 'category':'boltSize'},
            {'name': 'boltShearInThread','value': shearInThread, 'lb': 0, 'ub': 1, 'type': 'int', 'category':None}
            ])


class BoltAssembly(Assembly):
    def __init__(self):
        from .datatype import paramList
        from math import inf
        self.rows=[]
        self.cols=[]
        self.connectedParts = []
        self.parameters = paramList()
        self.parameters.extend([
            {'name': 'Nx','value': None, 'lb': 1, 'ub': 100, 'type': 'int', 'category':None},
            {'name': 'Ny','value': None, 'lb': 1, 'ub': 100, 'type': 'int', 'category':None},
            {'name': 'xOffset','value': None, 'lb': 0, 'ub': inf, 'type': 'float', 'category':None},
            {'name': 'yOffset','value': None, 'lb': 0, 'ub': inf, 'type': 'float', 'category':None},
            {'name': 'px','value': None, 'lb': 0, 'ub': inf, 'type': 'float', 'category':None},
            {'name': 'py','value': None, 'lb': 0, 'ub': inf, 'type': 'float', 'category':None},
            {'name': 'boltGrade','value': None, 'lb': 0, 'ub': 6, 'type': 'int', 'category':'boltGrade'},
            {'name': 'boltSize','value': None, 'lb': 0, 'ub': 11, 'type': 'int', 'category':'boltSize'},
            {'name': 'boltShearInThread','value': None, 'lb': 0, 'ub': 1, 'type': 'int', 'category':None}
            ])
        pass
    
    def bolt(self,*args):
        paramNames = ['boltSize', 'boltGrade' 'boltShearInThread']
        for arg in args:
            if isinstance(arg, Bolt):
                for name in paramNames:
                    idx1 = self.parameters.__getIndex__(name)
                    idx2 = Bolt.parameters.__getIndex__(name)
                    self.parameters[idx1] = Bolt.parameters[idx2]
                return
            boltParams = [ self.parameters.__getDict__(name) for name in paramNames ]
        return boltParams
    
    def updateParameters(self,params):
        super().updateParameters(params)
        
        # changes to boltAssembly
        self.updatePositions()
        
    
    def updatePositions(self):
        Nx          = self.parameters.getValue('Nx')
        Ny          = self.parameters.getValue('Ny')
        xOffset     = self.parameters.getValue('xOffset')
        yOffset     = self.parameters.getValue('yOffset')
        px          = self.parameters.getValue('px')
        py          = self.parameters.getValue('py')
        
        x_min       = -.5*(Nx-1) * px + xOffset
        y_min       = -.5*(Ny-1) * py + yOffset
        positions   = []
        for nx in range(Nx):
            x_pos = x_min + px * (nx-1)
            
            for ny in range(Ny):
                y_pos = y_min + py * (ny-1)
                
                positions.append([x_pos, y_pos])
        
        self.__clearBoltGrid__()
        self.appendPositions(positions)
        pass
    
    def __clearBoltGrid__(self):
        self.rows = []; self.cols=[]
    
    def appendPositions(self,positions):
        for position in positions:
            self.rows.append(self.__row__(position))
            self.cols.append(self.__col__(position))
        pass
    
    def __row__(self,position) -> dict:
        return {'value':position[0],'count':1}
    
    def __col__(self,position) -> dict:
        return {'value':position[1],'count':1}
    
    def __dict__(self):
        boltSize        = self.parameters.getValue('boltSize')
        boltGrade       = self.parameters.getValue('boltGrade')
        shearInThread   = self.parameters.getValue('boltshearInThread')
        return {
            'length':0,
            'anchorTypeData': 0,
            'anchorTypeSize': 0.0,
            'angles': [
                    [{'value': 0.0, 'count': 8}]
                ],
            'boltInteraction': 0,
            'cols': [self.cols],
            'colsGridType': 0,
            'colsNegative': None,
            'colsPosition': 0,
            'colsSymmetry': 0,
            'coordinateSystem': 0,
            'counts': [6, 8],
            'itemId': '8d5b4b8d-ad80-4b67-a8ec-43d708d1ad12',
            'name': f'M{boltSize} {boltGrade}',
            'polarInput': 0,
            'polarPosition': 0,
            'positions': None,
            'radii': [
                [{'value': 0.08, 'count': 1}, {'value': 0.04, 'count': 1}]
                ],
            'rows': [self.rows],
            'rowsGridType': 0,
            'rowsNegative': None,
            'rowsPosition': 0,
            'shearInThread': shearInThread,
            'tableId': '1f37540f-605f-4d95-b5c5-16d9d47d90cc'
            }
    
    def updateIdeaParameter(self, ideaParameter):
        ideaParameter['value'] = self.__dict__()
        return ideaParameter



class Plate(Component):
    def __init__(self, thickness, material):
        self.thickness = thickness
        if isinstance(material, Material):
            self.material = material
        else:
            raise Exception(f"{material} is not instance {Material}.")



class StiffenerPlate(Plate):
    def __init__(self, thickness, material, B1=0.1, B2=0.1, H1=0.1, H2=0.1):
        super().__init__(thickness, material)
        self.B1 = B1
        self.B2 = B2
        self.H1 = H1
        self.H2 = H2

    def setOffset(self, xOffset=0, yOffset=0):
        self.xOffset = xOffset
        self.yOffset = yOffset



class NegativeVolume(Component):
    def __init__(self, ex=0, ey=0, ez=0):
        self.ex = ex
        self.ey = ey
        self.ez = ez



class Weld(Component):
    def __init__(self, material, thickness):
        if isinstance(material, Material):
            self.material = material
        else:
            raise Exception(f"{material} is not instance {Material}.")
        self.thickness = thickness



class Workplane(Component):
    def __init__(self,x=0, y=0, z=0, rotx=0, roty=0, rotz=0):
        self.x
        self.y = y
        self.z = z
        self.rotx = rotx
        self.roty = roty
        self.rotz = rotz


    

        

    

    



