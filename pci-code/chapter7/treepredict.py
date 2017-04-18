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
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

# Divides a set on a specific column. Can handle numeric
# or nominal values
def divideset(rows,column,value):
    # Make a function that tells us if a row is in
    # the first group(true) or the second group(false)
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row:row[column] >= value
    else:
        split_function = lambda row:row[column] == value

    sett = [row for row in rows if split_function(row)]
    setf = [row for row in rows if not split_function(row)]
    return (sett, setf)

# Create counts of possible results (the last column of 
# each row is the result)
def uniquecounts(rows):
    results = {}
    for row in rows:
        r = row[-1]
        results.setdefault(r, 0)
        results[r] += 1
    return results

# Probability that a randomly placed item will
# be in the wrong category
def giniimpurity(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2: continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp

# Entropy is the sum of p(x)log(p(x)) across all 
# the different possible results
def entropy(rows):
    from math import log
    log2 = lambda x:log(x)/log(2)
    results = uniquecounts(rows)
    ent = 0.0
    for r in results:
        p = float(results[r]) / len(rows)
        ent -= p * log2(p)
    return ent


def printtree(tree,indent=''):


#def getwidth(tree):

#def getdepth(tree):

#from PIL import Image,ImageDraw

#def drawtree(tree,jpeg='tree.jpg'):
  
#def drawnode(draw,tree,x,y):

#def classify(observation,tree):

#def prune(tree,mingain):

#def mdclassify(observation,tree):

#def variance(rows):

def buildtree(rows,scoref=entropy):
    if len(rows) == 0:
        return decisionnode()

    best_gain = 0.0
    best_criteria = None
    best_sets = None
    current_score = scoref(rows)

    col_count = len(rows[0]) - 1
    for col in range(0, col_count):
        col_values = set()
        for row in rows:
            col_values.add(row[col])

        for value in col_values:
            (set1,set2) = divideset(rows, col, value)
            p = float(len(set1)) / len(rows)
            info_gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
            if best_gain < info_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = info_gain
                best_criteria = (col,value)
                best_sets = (set1,set2)

    if best_gain > 0:
        true_branch = buildtree(best_sets[0], scoref)
        false_branch = buildtree(best_sets[1], scoref)
        return decisionnode(col=best_criteria[0], value=best_criteria[1], tb=true_branch, fb=false_branch)
    else:
        return decisionnode(results=rows)
