#!/usr/bin/python

'''
import pdb
pdb.set_trace()
'''

import random
import numpy as np
from decisionTree import decisionTree

class randomForest:
    
    def buildForest(self, dataVectorTable, dataLabelList, numOfTrees):
        
        self.forest = []
        self.numOfTrees = numOfTrees
        self.sampleDataIndexTable = []

        self.dataVectorTable = dataVectorTable[:]
        self.dataLabelList = dataLabelList[:]
        self.numOfTrainDatas = self.dataVectorTable.shape[0]
        self.numOfDims = self.dataVectorTable.shape[1]

        for index in range(numOfTrees):
            
            sampleDataIndexList = [random.randint(0, self.numOfTrainDatas-1) for i in range(self.numOfTrainDatas)]
            self.sampleDataIndexTable.append( sampleDataIndexList )

            tree = decisionTree()
            tree.buildTree(self.dataVectorTable[sampleDataIndexList, : ], self.dataLabelList[sampleDataIndexList])
            self.forest.append(tree)

        return self
    
    def genTreePredictTable(self, dataVectorTable):
        
        self.treePredictTable = []

        for index in range(self.numOfTrees):
            self.treePredictTable.append(self.forest[index].predictTable(dataVectorTable))
        
        self.treePredictTable = np.array(self.treePredictTable)
        self.numOfTestData = dataVectorTable.shape[0]

    def retTreePredictTable(self):
        return self.treePredictTable

    def genForestPredictTable(self, dataVectorTable):

        # gen tree predict table first
        self.genTreePredictTable(dataVectorTable)
        
        self.forestPredictTable = []

        tmpPredictList = np.array([0.0] * self.numOfTestData)

        for index in range(self.numOfTrees):
            tmpPredictList += self.treePredictTable[index]
            self.forestPredictTable.append((tmpPredictList > 0) * 2 - 1)

        self.forestPredictTable = np.array(self.forestPredictTable)

    def retForestPredictTable(self):
        return self.forestPredictTable

if __name__ == '__main__':
    
    dataVectorTable = np.array([[1, 3], [2, 0], [3, 8]])
    dataLabelList = np.array([1, -1, 1])
    
    forest = randomForest()
    forest.buildForest(dataVectorTable, dataLabelList, 2)
    forest.genForestPredictTable(dataVectorTable)
