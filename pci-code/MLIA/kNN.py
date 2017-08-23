from numpy import *
import operator

def createDataset():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inx, dataset, labels, k):
    datasetSize = dataset.shape[0]
    diffmat = tile(inx, (datasetSize, 1)) - dataset
    diffsq = diffmat ** 2
    diffsum = diffsq.sum(axis=1)
    distmat = diffsum ** 0.5
    sortedDistIndice = distmat.argsort()

    matches = {}
    for i in range(k):
        label = labels[sortedDistIndice[i]]
        matches[label] = matches.get(label, 0) + 1

    sortedmatches = sorted(matches.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedmatches[0][0]

def file2matrix(filename):
    fr = open(filename)
    nline = len(fr.readlines())
    returnMat = zeros((nline, 3))
    labels = []

    index = 0
    fr = open(filename)
    for line in fr.readlines():
        cols = line.strip().split('\t')
        returnMat[index,:] = cols[0:3]
        labels.append(cols[-1])
        index += 1
    return returnMat, labels
