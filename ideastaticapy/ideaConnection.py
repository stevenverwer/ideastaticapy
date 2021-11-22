"""
@author: Steven Verwer
@git: https://github.com/stevenverwer
"""

import sys, clr, json
r"C:\Program Files\IDEA StatiCa\StatiCa 21.1"
class Connector:
    def __init__(self,ideaPath=None):
        if not ideaPath:
            from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey
            from winreg import EnumKey, EnumValue, QueryValueEx
            ideaVersions = [r"SOFTWARE\IDEAStatiCa\21.1\IDEAStatiCa\Designer",
                            r"SOFTWARE\IDEAStatiCa\21.0\IDEAStatiCa\Designer",
                            r"SOFTWARE\IDEAStatiCa\20.1\IDEAStatiCa\Designer"]
            aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            found = False
            for each in ideaVersions:
                if found:
                    break
                aKey = each;
                for i in range(1024):
                    try:
                        openedKey = OpenKey(aReg, aKey)
                        val = EnumValue(aKey,i)
                        if val[0] == 'InstallDir64':
                            ideaPath = val[1]
                            found = True
                            break
                    except EnvironmentError:
                        break
        self.ideaPath = ideaPath
        sys.path.append(ideaPath)
    
    def openProject(self,ideaConFilePath):
        clr.AddReference('IdeaStatiCa.Plugin')
        from IdeaStatiCa.Plugin import ConnHiddenClientFactory

        factory = ConnHiddenClientFactory(self.ideaPath)
        ideaConnectionClient = factory.Create()
        
        ideaConnectionClient.OpenProject(ideaConFilePath)
        return ideaConnectionClient
    
    def closeProject(self, ideaConnectionClient):
        ideaConnectionClient.CloseProject()
        pass
    
    def getProjectInfo(self,ideaConnectionClient):
        return ideaConnectionClient.GetProjectInfo()
    
    def getConnections(self,ideaConnectionClient):
        projectInfo = ideaConnectionClient.GetProjectInfo()
        return projectInfo.Connections
    
    def getConnection(self, name, connections):
        if not type(name)==str:
            raise Exception(f"name is {type(name)} while string type is expected.")
        
        for conn in connections:
            if conn.Name == name:
                return conn
        return None
    
    def getMaterialsInProject(self, ideaConnectionClient):
        return ideaConnectionClient.GetMaterialsInProject();
    
    def getCrossSectionsInProject(self, ideaConnectionClient):
        return ideaConnectionClient.GetCrossSectionsInProject();
    
    def getParams(self,connection, ideaConnectionClient) -> dict:
        params_json_string = ideaConnectionClient.GetParametersJSON(connection.Identifier)
        
        if params_json_string:
            return json.loads(params_json_string)
        else:
            return None
    
    def updateParams(self, params, connection, ideaConnectionClient):
        updated_params_json_string = json.dumps(params)
        ideaConnectionClient.ApplyParameters(connection.Identifier, updated_params_json_string)
    
    def getLoadcases(self, ideaConnectionClient, connection) ->list:
        loading_json_string = ideaConnectionClient.GetConnectionLoadingJSON(connection.Identifier)
        return  json.loads(loading_json_string)
    
    def getForcesOnSegments(self, loadcase) ->list:
        return loadcase['forcesOnSegments']
    
    def calculateConnection(self, connection, ideaConnectionClient):
        # calculates the connection and returns brief results.
        briefResults = ideaConnectionClient.Calculate(connection.Identifier)
        return briefResults
    
    def checkResults(self, connection, ideaConnectionClient):
        # 'after calculation' return checkResults.
        # https://idea-statica.github.io/ideastatica-public/docs/latest/api-iom/IdeaRS.OpenModel.Connection.ConnectionCheckRes.html
        checkResults_json_string = ideaConnectionClient.GetCheckResultsJSON(connection.Identifier)
        if checkResults_json_string:
            return json.loads(checkResults_json_string)
        else:
            return None
