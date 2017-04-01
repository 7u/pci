my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

class decisionnode:

# Divides a set on a specific column. Can handle numeric
# or nominal values
def divideset(rows,column,value):

# Create counts of possible results (the last column of 
# each row is the result)
def uniquecounts(rows):

# Probability that a randomly placed item will
# be in the wrong category
def giniimpurity(rows):

# Entropy is the sum of p(x)log(p(x)) across all 
# the different possible results
def entropy(rows):


def printtree(tree,indent=''):

def getwidth(tree):

def getdepth(tree):

from PIL import Image,ImageDraw

def drawtree(tree,jpeg='tree.jpg'):
  
def drawnode(draw,tree,x,y):

def classify(observation,tree):

def prune(tree,mingain):

def mdclassify(observation,tree):

def variance(rows):

def buildtree(rows,scoref=entropy):
