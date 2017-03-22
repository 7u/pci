#from PIL import Image,ImageDraw

def readfile(filename):
  lines=[line for line in file(filename)]
  
  # First line is the column titles
  colnames=lines[0].strip().split('\t')[1:]
  rownames=[]
  data=[]
  for line in lines[1:]:
    p=line.strip().split('\t')
    # First column in each row is the rowname
    rownames.append(p[0])
    # The data for this row is the remainder of the row
    data.append([float(x) for x in p[1:]])
  return rownames,colnames,data

from math import sqrt

def pearson(v1,v2):
    sum1=sum(v1)
    sum2=sum(v2)
    sqSum1=sum([pow(v,2) for v in v1])
    sqSum2=sum([pow(v,2) for v in v2])

    n=len(v1)
    pSum=sum([v1[i]*v2[i] for i in range(n)])

    indp=sqrt((sqSum1-pow(sum1,2)/n)*(sqSum2-pow(sum2,2)/n))
    if indp == 0:
        return 0
    cov=pSum-sum1*sum2/n
    return 1-cov/indp

class biCluster:
  def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
      self.vec=vec
      self.left=left
      self.right=right
      self.distance=distance
      self.id=id

def hcluster(rows,distance=pearson):
    distances={}
    currentClustId=-1
    cluster=[biCluster(rows[i],id=i) for i in range(len(rows))]

    while len(cluster) > 1:
        lowestPair=(0,1)
        closest=distance(cluster[0].vec,cluster[1].vec)
        for i in range(len(cluster)):
            for j in range(i+1,len(cluster)):
                if (cluster[i].id,cluster[j].id) not in distances:
                    distances[(cluster[i].id,cluster[j].id)]=distance(cluster[i].vec,cluster[j].vec)
                
                d=distances[(cluster[i].id,cluster[j].id)]
                if d < closest:
                    closest=d
                    lowestPair=(i,j)

        mergeVec=[(cluster[lowestPair[0]].vec[i]+cluster[lowestPair[1]].vec[i])/2 for i in range(len(rows[0]))]
        newCluster=biCluster(mergeVec,cluster[lowestPair[0]],cluster[lowestPair[1]],closest,currentClustId)
        currentClustId-=1
        del cluster[lowestPair[1]]
        del cluster[lowestPair[0]]
        cluster.append(newCluster)
    
    return cluster[0]

def printclust(clust,labels=None,n=0):
  # indent to make a hierarchy layout
  for i in range(n): print ' ',
  if clust.id<0:
    # negative id means that this is branch
    print '-'
  else:
    # positive id means that this is an endpoint
    if labels==None: print clust.id
    else: print labels[clust.id]

  # now print the right and left branches
  if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
  if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)

#def getheight(clust):

#def getdepth(clust):

#def drawdendrogram(clust,labels,jpeg='clusters.jpg'):

#def drawnode(draw,clust,x,y,scaling,labels):

def rotateMatrix(data):
    newData=[]
    for i in range(len(data[0])):
        newRow=[data[j][i] for j in range(len(data))]
        newData.append(newRow)
    return newData

#import random

#def kcluster(rows,distance=pearson,k=4):

#def tanamoto(v1,v2):

#def scaledown(data,distance=pearson,rate=0.01):

#def draw2d(data,labels,jpeg='mds2d.jpg'):
