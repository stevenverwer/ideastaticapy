# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:42:33 2021

@author: s.verwer
"""

import pygmo as pg
from ideastaticapy import connection, ideaConnection

class OptimProblem:
    def fitness(self, x):
        parameters = self.parameters
        self.connector.updateParams(parameters, self.connection, self.ideaConnectionClient)
        self.connector.calculateConnection(self.connection, self.ideaConnectionClient)
        self.connector.checkResults(self.connection, self.ideaConnectionClient)
        
    def __init__(self, parameters, connection, ideaConnectionClient, connector):
        self.lb = []
        self.ub = []
        self.nic = 0
        self.nix = 0
        self.parameters = parameters
        self.connection = connection
        self.ideaConnectionClient = ideaConnectionClient
        self.connector = connector
        for parameter in parameters:
            if parameter['Type']=='Float':
                self.lb = self.lb.append(parameter[['lb']])
                self.ub = self.ub.append(parameter['ub'])
                self.nic +=1
        for parameter in parameters:
            if parameter['Type']=='Integer':   
                self.lb = self.lb.append(parameter[['lb']])
                self.ub = self.ub.append(parameter['ub'])
                self.nix +=1
                self.nic +=1

        
        def get_bounds(self):
            return [self.lb, self.ub]
        
        def get_nic(self):
            return self.nic
        
        def get_nix(self):
            return self.nix