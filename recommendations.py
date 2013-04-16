import pdb

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
def sim_euclidean(prefs, person1, person2):

	sim = {}
	for item in prefs[person1]:
		if item in prefs[person2]:
			sim[item] = 1

	if len(sim) == 0: return 0 #No similarities
	dist = 0.0
#	pdb.set_trace()
	for item in sim:
		dist += pow((prefs[person1][item] - prefs[person2][item]),2)

	return 1/(1 + dist)

# Returns the Pearson correlation coefficient for person1 and person2
def sim_pearson(prefs, person1, person2):
	sim = {}
	for item in prefs[person1]:
		if item in prefs[person2]:
			sim[item] = 1

	n = len(sim)		
	if n == 0: return 0 #No similarities

	sum1 = sum([prefs[person1][item] for item in sim])
	sum2 = sum([prefs[person2][item] for item in sim])

	sumSq1 = sum([pow(prefs[person1][item], 2) for item in sim])
	sumSq2 = sum([pow(prefs[person2][item], 2) for item in sim])

	sumProd = sum([prefs[person1][item]*prefs[person2][item] for item in sim])

	num=sumProd-(sum1*sum2/n)
	den=sqrt((sumSq1-pow(sum1,2)/n)*(sumSq2-pow(sum2,2)/n))
	if den==0: return 0
	r=num/den
	
	return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def top_matches(prefs, person, n=5, similarity_measure=sim_pearson):
	scores = [(similarity_measure(prefs,person,person2),person2) for person2 in prefs if person2 != person]	
	scores.sort()
	scores.reverse()
	return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings

def get_recommendations(prefs, person, similarity=sim_pearson):

	totals = {}
	simSum = {}

	for other in prefs:
		if other == person: continue
		sim = similarity(prefs, person, other)
		if sim <= 0: continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item] * sim
				#Similarity sums
				simSum.setdefault(item, 0)
				simSum[item] += sim		
		
	rankings = [(total/simSum[item], item) for item,total in totals.items()] 	

	return rankings