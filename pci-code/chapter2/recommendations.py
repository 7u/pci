# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
    sum=0
    for item,score in prefs[person1].items():
        if item in prefs[person2]:
            sum=sum+pow(score-prefs[person2][item],2)
    if sum == 0:
        return sum;
    return 1/(1+sqrt(sum))

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,person1,person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    n=len(si)
    if n == 0:
        return 0

    sum1=sum([prefs[person1][item] for item in si])
    sum2=sum([prefs[person2][item] for item in si])
    sqSum1=sum([pow(prefs[person1][item],2) for item in si])
    sqSum2=sum([pow(prefs[person2][item],2) for item in si])

    pSum=sum([prefs[person1][item]*prefs[person2][item] for item in si])

    indp=sqrt((sqSum1-pow(sum1,2)/n)*(sqSum2-pow(sum2,2)/n))
    if indp == 0:
        return 0
    cov=pSum-sum1*sum2/n
    return cov/indp


# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,similarity=sim_distance,n=5):
    scores=[(similarity(prefs,person,other),other) for other in prefs if person != other]
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSum={}
    for other,rankings in prefs.items():
        if other != person:
            sim=similarity(prefs,person,other)
            if sim < 0:
                continue

            for it,score in rankings.items():
                if it not in prefs[person] or prefs[person][it] == 0:
                    totals.setdefault(it, 0)
                    totals[it] += sim * score
                    simSum.setdefault(it, 0)
                    simSum[it] += sim
    recommendations=[(score/simSum[it],it) for it,score in totals.items()]
    recommendations.sort()
    recommendations.reverse()
    return recommendations

def transformPrefs(prefs):
    result={}
    for user in prefs:
        for item in prefs[user]:
            result.setdefault(item,{})
            result[item][user]=prefs[user][item]
    return result

def calculateSimilarItems(prefs,n=10):
    result={}
    items=transformPrefs(prefs)
    c=0
    for it in items:
        c+=1
        if c%100==0: print "%d / %d" % (c,len(items))
        result[it]=topMatches(items,it,sim_distance,n)
    return result

def getRecommendedItems(prefs,itemMatch,user):
    totals={}
    simSum={}
    for it,score in prefs[user].items():
        for (sim,other) in itemMatch[it]: 
            if other not in prefs[user] or prefs[user][other] == 0:
                totals.setdefault(other, 0)
                totals[other] += sim * score
                simSum.setdefault(other, 0)
                simSum[other] += sim
    recommendations=[(score/simSum[it],it) for it,score in totals.items()]
    recommendations.sort()
    recommendations.reverse()
    return recommendations


#def loadMovieLens(path='/data/movielens'):
