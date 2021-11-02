"""
@author: Steven Verwer
@git: https://github.com/stevenverwer
"""

class Component:
    def updateParameters(self, **kw):
        output = {}
        for key, parameter in kw.items():
            if key in self.__dict__.keys():
                parameter['value'] = self.__getattribute__(key)
                output[key] = parameter
        return output



class Assembly:
    pass



class Material:
    def __init__(self, name='S355'):
        self.name = name
    pass



class Bolt: # inheritance
    def __init__(self, size=16, grade='8.8', shearInThread=True):
        self.size = size
        self.grade = grade
        self.shearInThread = shearInThread



class BoltAssembly(Assembly):
    def __init__(self):
        self.rows=[]
        self.cols=[]
        pass
    
    def setBolt(self,bolt):
        if isinstance(bolt, Bolt):
            self.size  = bolt.size
            self.grade = bolt.grade
            self.shearInThread = bolt.shearInThread
        else:
            raise Exception(f"{bolt} is not instance {Bolt}.")
    
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
            'name': f'M{self.size} {self.grade}',
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
            'shearInThread': self.shearInThread,
            'tableId': '1f37540f-605f-4d95-b5c5-16d9d47d90cc'
            }
    
    def updateParameter(self, parameter):
        parameter['value'] = self.__dict__()
        return parameter



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
    
    

if __name__ == "__main__":
    boltList = [[-60,  45 ],
                [-60, -45 ],
                [ 60,  45 ],
                [ 60, -45 ]]
    bolt1 = Bolt(16, '8.8')
    boltAssembly1 = BoltAssembly()
    boltAssembly1.setBolt(bolt1)
    boltAssembly1.appendPositions(boltList)
    
    
    
    