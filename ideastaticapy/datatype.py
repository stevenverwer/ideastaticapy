# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:51:38 2021

@author: s.verwer
"""

class paramList(list):
    '''
    paramlist is a list of dictionaries. These dictionaries contain at least a
    name. For a standard parameter the standard keys are: value, type,
    lowerbound (lb) and upperbound (ub). lb and ub are only for optimization.
    A parameter can also refer to a category such as a BoltGrade with an
    integer.
    '''
    def __init__(self, *args):
        super().__init__(self, *args)
        self.categorieDicts = [
            {'name':'boltGrade', 'value':['4.6', '4.8', '5.8', '8.8', '9.8', '10.9', '12.9']},
            {'name':'boltSize', 'value':['M12', 'M16', 'M20', 'M22', 'M24', 'M27',
                                         'M30', 'M36', 'M39', 'M42', 'M48', 'M52']}
            ]
        
    def _getKey(self,lst,key,name):
        return next((d[key] for d in lst if d['name'] == name), None)
    def __getKey__(self,key,name):
        return  self._getKey(self,key,name)

    def __updateKey__(self,key,name,val):
        idx = self.__getIndex__(name)
        self[idx][key] = val
    
    def _getIndex(self,lst,name):
        return next((self.index(d) for d in lst if d['name'] == name), None)
    def __getIndex__(self,name):
        return self._getIndex(self,name)
    
    def _getDict(self,lst,name): 
        return next((d for d in lst if d['name'] == name), None)
    def __getDict__(self,name): 
        return self._getDict(self,name)
    
    def getCategoryItem(self,name):
        d = self.getDict(name)
        if not d['category']:
            return None
        categorieList = self._getKey(self.categorieDicts,'value',d['category'])
        if not categorieList:
            return None
        if not isinstance(d['value'], int):
            raise Exception(f"{d['value']} is not an integer")
        if (d['value']<0) or (d['value']>=len(categorieList)):
            raise Exception(f"{d['value']} does not point to a categoryItem")
        return categorieList[d['value']]
    
    def getIntFromCategoryItem(self, category, categoryItem):
        categorieList = self._getKey(self.categorieDicts, 'value', category)
        if not categorieList:
            return None
        return next(( categorieList.index(d) for d in categorieList if d == categoryItem), None)
    
    def getValue(self, name):
        if not self.getCategory(name):
            return self.getValueKey(name)
        return self.getCategoryItem(name)
    
    def getCategory(self, name): return self.__getKey__(key='category', name=name)
    def getValueKey(self, name): return self.__getKey__(key='value', name=name)
    def getType(self, name): return self.__getKey__(key='type', name=name)
    def getLb(self, name): return self.__getKey__(key='lb', name=name)
    def getUb(self, name): return self.__getKey__(key='ub', name=name)
    
    def updateValue(self,name,val): self.__updateKey__('value',name,val)
    def updateLb(self,name,val): self.__updateKey__('lb',name,val)
    def updateUb(self,name,val): self.__updateKey__('ub',name,val)