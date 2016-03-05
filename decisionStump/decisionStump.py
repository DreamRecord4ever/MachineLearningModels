#!/usr/bin/python

'''
import pdb
pdb.set_trace()
'''
        
from collections import Counter
import numpy as np

class decisionStump:
    
    def __init__(self):
        
        self.isRootNode = False
        self.leftChild = None
        self.rightChild = None

    def buildStump(self, dataVectorTable, dataLabelList, isRootNode):
        
        self.isRootNode = isRootNode
        self.dataVectorTable = dataVectorTable[:]
        self.dataLabelList = dataLabelList[:]
        self.numOfDatas = self.dataVectorTable.shape[0]
        self.numOfDims = self.dataVectorTable.shape[1]
        self.impurity = self.computeGini(self.dataLabelList)
        
        if self.isRootNode == True:
            
            # pick the best decision stump => dim, theta
            self.pickBestDecisionStump()

            # split to 2 parts
            leftChildDataIndexList = []
            rightChildDataIndexList = []

            for dataVectorIndex in range(self.numOfDatas):
                
                if dataVectorTable[dataVectorIndex][self.dim] <= self.theta:
                    leftChildDataIndexList.append(dataVectorIndex)
                else:
                    rightChildDataIndexList.append(dataVectorIndex)

            # recursion
            self.leftChild = decisionStump()
            self.leftChild.buildStump(dataVectorTable[leftChildDataIndexList, : ], dataLabelList[leftChildDataIndexList], False)
            self.rightChild = decisionStump()
            self.rightChild.buildStump(dataVectorTable[rightChildDataIndexList, : ], dataLabelList[rightChildDataIndexList], False)

        return self

    def pickBestDecisionStump(self):

        dimSmallestWeightedGiniList = []
        dimSmallestWeightedGiniThetaList = []

        for dim in range(self.numOfDims):
        
            dataList = self.dataVectorTable[:, dim:dim+1].ravel()
            labelList = self.dataLabelList[:]
            
            sortedDataLabelList = sorted(zip(dataList, labelList), key = lambda x: x[0])

            dataList = np.array([dataLabel[0] for dataLabel in sortedDataLabelList])
            labelList = np.array([dataLabel[1] for dataLabel in sortedDataLabelList])

            # threshold List
            tempDataList = np.roll(dataList, -1)
            thetaList = (dataList + tempDataList) / 2.0
            thetaList = thetaList[:-1]

            thetaWeightedGiniList = []
            
            for i in range(len(thetaList)):
                
                thetaWeightedGiniList.append(self.computeWeightedGini(labelList[i+1:], labelList[:i+1]))

            dimSmallestWeightedGini = min(thetaWeightedGiniList)
            dimSmallestWeightedGiniList.append(dimSmallestWeightedGini)
            dimSmallestWeightedGiniThetaList.append( thetaList[thetaWeightedGiniList.index(dimSmallestWeightedGini)] )

        self.dim = dimSmallestWeightedGiniList.index( min(dimSmallestWeightedGiniList) )
        self.theta = dimSmallestWeightedGiniThetaList[ self.dim ]

    def computeWeightedGini(self, leftDataLabelList, rightDataLabelList):
        
        return  len(leftDataLabelList) * self.computeGini(leftDataLabelList) + len(rightDataLabelList) * self.computeGini(rightDataLabelList)

    def computeGini(self, dataLabelList):
        
        labels = list(set(dataLabelList))

        return 1.0 - sum([((dataLabelList == label).sum() / float(dataLabelList.size))**2 for label in labels])

    def retImpurity(self):
        return self.impurity

    def predict(self, dataVector):
        
        # if leaf node => return constant function: majority of yn
        if self.isRootNode == False:
            return Counter(self.dataLabelList).most_common()[0][0]
        elif dataVector[self.dim] <= self.theta:
            return self.leftChild.predict(dataVector)
        else:
            return self.rightChild.predict(dataVector)

    def predictTable(self, dataVectorTable):
        
        returnList = []

        for dataVector in dataVectorTable:
            returnList.append(self.predict(dataVector))

        return returnList

    def printStump(self):
        
        print '(Dim, Theta) = ( ', self.dim, ', ', self.theta, ')'

if __name__ == '__main__':
    
    dataVectorTable = np.array([[1, 3], [2, 0], [3, 8]])
    dataLabelList = np.array([1, -1, 1])
    
    stump = decisionStump()
    stump.buildStump(dataVectorTable, dataLabelList, True)

    stump.printStump()
    print stump.predictTable(dataVectorTable)
