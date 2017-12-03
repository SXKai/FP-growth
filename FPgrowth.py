# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:49:24 2017

@author: Q
"""

import numpy as np
def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat
    
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans),0) + 1
    return retDict

class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
    def inc(self,numOccur):
        self.count += numOccur
    def disp(self,ind=1):
        print(' '*ind,self.name,' ',self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet,minSup=1):#生成树
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item,0) + dataSet[trans]
    
#    for key in headerTable.keys():
#        if headerTable[key]<minSup:
#            del(headerTable[key])
#    
    headerTable = {k:v for k,v in headerTable.items() if v>=minSup}        
            
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]
    
    retTree = treeNode('Null Set',0,None)

    for transSet,count in dataSet.items():
        localD = {}
        for tran in transSet:
            if tran in freqItemSet:
                localD[tran] = headerTable[tran][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key = lambda k: k[1],reverse = True)]
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable
            
            
        
def updateTree(items,inTree,headerTable,count):#更新树
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
#        print('this is ',inTree.children[items[0]].name,' items:',items)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::],inTree.children[items[0]],headerTable,count)
        
def updateHeader(nodeToTest,targetNode):#更新头指针
    i = 0
    while(nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
#        print(nodeToTest.name,' ',i)
        i = i+1
    nodeToTest.nodeLink = targetNode
            
    
def ascendTree(leafNode,prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

def findPrefixPath(basePat,treeNode):#寻找条件模式基
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree,headerTable,minSup,preFix,freqItemList):#生成频繁项集
    bigL = [v[0] for v in sorted(headerTable.items(),key=lambda p:p[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat,headerTable[basePat][1])
        myCondTree,myHead = createTree(condPattBases,minSup)
        if myHead != None:
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)
            
          

data = loadSimpDat()
data = createInitSet(data)
tree,header = createTree(data,3)
freqItems = []
mineTree(tree,header,3,set([]),freqItems)
print(freqItems)











