#!/usr/bin/python

'''
import pdb
pdb.set_trace()
'''

import random
import numpy as np
from decisionStump import decisionStump

class randomStumpForest:
    
    def buildForest(self, dataVectorTable, dataLabelList, numOfStumps):
        
        self.forest = []
        self.numOfStumps = numOfStumps
        self.sampleDataIndexTable = []

        self.dataVectorTable = dataVectorTable[:]
        self.dataLabelList = dataLabelList[:]
        self.numOfTrainDatas = self.dataVectorTable.shape[0]
        self.numOfDims = self.dataVectorTable.shape[1]

        for index in range(numOfStumps):
            
            sampleDataIndexList = [random.randint(0, self.numOfTrainDatas-1) for i in range(self.numOfTrainDatas)]
            self.sampleDataIndexTable.append( sampleDataIndexList )

            stump = decisionStump()
            stump.buildStump(self.dataVectorTable[sampleDataIndexList, : ], self.dataLabelList[sampleDataIndexList], True)
            self.forest.append(stump)

        return self
    
    def genStumpPredictTable(self, dataVectorTable):
        
        self.stumpPredictTable = []

        for index in range(self.numOfStumps):
            self.stumpPredictTable.append(self.forest[index].predictTable(dataVectorTable))
        
        self.stumpPredictTable = np.array(self.stumpPredictTable)
        self.numOfTestData = dataVectorTable.shape[0]

    def retStumpPredictTable(self):
        return self.stumpPredictTable

    def genForestPredictTable(self, dataVectorTable):

        # gen stump predict table first
        self.genStumpPredictTable(dataVectorTable)
        
        self.forestPredictTable = []

        tmpPredictList = np.array([0.0] * self.numOfTestData)

        for index in range(self.numOfStumps):
            tmpPredictList += self.stumpPredictTable[index]
            self.forestPredictTable.append((tmpPredictList > 0) * 2 - 1)

        self.forestPredictTable = np.array(self.forestPredictTable)

    def retForestPredictTable(self):
        return self.forestPredictTable

if __name__ == '__main__':
    
    dataVectorTable = np.array([[1, 3], [2, 0], [3, 8]])
    dataLabelList = np.array([1, -1, 1])
    
    forest = randomStumpForest()
    forest.buildForest(dataVectorTable, dataLabelList, 2)
    forest.genForestPredictTable(dataVectorTable)
