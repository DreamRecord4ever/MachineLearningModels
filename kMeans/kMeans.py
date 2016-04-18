#!/usr/bin/python

import random
import numpy as np

class kMeans:
    
    def cluster(self, vectorTable, k):
        
        self.k = k
        self.vectorTable = np.array(vectorTable)
        self.dataSize = self.vectorTable.shape[0]

        self.centerTable = vectorTable[random.sample(range(0, self.dataSize), self.k)]
        self.centerSetTable = []
        
        while True:

            # determine new sets based on new center
            oldCenterSetTable = self.centerSetTable[:]
            vectorCenterDistTable = np.array([[0.0] * self.k] * self.dataSize)

            for centerIndex in xrange(self.k):
                vectorCenterDistTable[:, centerIndex] = np.sum((self.vectorTable - self.centerTable[centerIndex])**2, axis=1)

            self.centerSetTable = [[] for i in range(self.k)]
            for vectorIndex in xrange(self.dataSize):
                nearestCenter = np.argmin(vectorCenterDistTable[vectorIndex])
                self.centerSetTable[nearestCenter].append(vectorIndex)
            
            # determine new center based on new sets
            self.centerTable = []
            for centerIndex in xrange(self.k):
                self.centerTable.append(np.sum(self.vectorTable[self.centerSetTable[centerIndex]], axis=0) / float(len(self.centerSetTable[centerIndex])))

            self.centerTable = np.array(self.centerTable)

            if np.array_equal(oldCenterSetTable, self.centerSetTable):
                break

    def computeErrorRate(self):

        Ein = 0.0
        for centerIndex in xrange(self.k):
            Ein += np.sum(np.sum((self.vectorTable[self.centerSetTable[centerIndex]] - self.centerTable[centerIndex])**2, axis=1)) / float(self.dataSize)

        return Ein

    def retNumOfClusters(self):
        return self.k
    
    def retVectorTable(self):
        return self.vectorTable

    def retDataSize(self):
        return self.dataSize

    def retCenterTable(self):
        return self.centerTable

    def retCenterSetTable(self):
        return self.centerSetTable

if __name__ == '__main__':
    
    vectorTable = np.array([[50, 50], [100, 100], [-50, -50], [-100, -100]])

    kMeansModel = kMeans()

    for k in xrange(2, 6, 2):

        kMeansModel.cluster(vectorTable, k)

        print 'k = ', k
        print 'centers:'
        print kMeansModel.retCenterTable()
        print 'errorRate = ', kMeansModel.computeErrorRate()
