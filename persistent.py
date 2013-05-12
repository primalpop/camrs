import pandas as pd
import numpy as np
import math

#For indexing the movie rating from the user dictionary
RATING = 0

class AutoVivification(dict):
	#Ref: http://stackoverflow.com/questions/651794/whats-the-best-way-to-initialize-a-dict-of-dicts-in-python
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def main():
	df = pd.read_csv('test_LDOS-CoMoDa.csv', na_values=['-1'])
	#df = pd.read_csv('LDOS-CoMoDa.csv', na_values=['-1'])
	#Replacement of missing values using the mean of the available values.
	for c in df.columns:
		mean = df[c].mean()
		df[c].fillna(mean)		
	#Storing in a dictionary	
	udb = AutoVivification() #data-store for [userid][itemid]
	mdb = {} #moviedatabase
	"""
	users = {userid: {itemid: rating, age,sex,city,country, c1, c2, ................, c12}}
	items = {itemid: {director, a1, a2, a3, g1, g2, g3, budget, lang, country}}
	"""
	#rows 2-19 user and contextual attributes
	#19-30 movie attributes
	for rows in df.values:
		udb[rows[0]][rows[1]] = rows[2:19]
		mdb[rows[1]] = rows[19:]

	#print sim_euclidean(udb, 254, 15)
	#print sim_pearson(udb, 15, 195)
	#print top_matches(udb, 15)
	print get_recommendations(udb, 15)

# Returns a distance-based similarity score for user1 and user2
def sim_euclidean(udb, user1, user2):
	sim = {}    
#	import pdb; pdb.set_trace()
	for item in udb[user1]:
		if item in udb[user2]:
			sim[item] = 1

	if len(sim) == 0: return 0 #No similarities
	dist = 0.0

	for item in sim:
		dist += pow((udb[user1][item][0] - udb[user2][item][0]),2)
	
	return 1/(1 + math.sqrt(dist))		


# Returns the Pearson correlation coefficient for person1 and person2
def sim_pearson(prefs, person1, person2):
	sim = {}
	for item in prefs[person1]:
		if item in prefs[person2]:
			sim[item] = 1

	n = len(sim)		
	if n == 0: return 0 #No similarities
#	import pdb; pdb.set_trace()
	#Sum of ratings 
	sum1 = sum([prefs[person1][item][RATING] for item in sim]) 
	sum2 = sum([prefs[person2][item][RATING] for item in sim])  
	#Sum of ratings squared
	sumSq1 = sum([(prefs[person1][item][RATING]) ** 2 for item in sim])
	sumSq2 = sum([(prefs[person2][item][RATING]) ** 2 for item in sim])
	#Sum of product of ratings
	sumProd = sum([(prefs[person1][item][RATING])*(prefs[person2][item][RATING]) for item in sim])

	num=(n*sumProd)-(sum1*sum2)
	den=math.sqrt((n*sumSq1 - sum1**2)*(n*sumSq2 - sum2**2))
	if den==0: return 0
	r=num/den
	return r	

# Returns the best matches for person from the udb dictionary.
# Number of results and similarity function are optional params.
def top_matches(udb, person, n=25, similarity_measure=sim_euclidean):
	scores = [(similarity_measure(udb,person,otherPerson),otherPerson) for otherPerson in udb if otherPerson!= person]	
	scores.sort()
	scores.reverse()
	return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings	
def get_recommendations(prefs, person, similarity=sim_euclidean):
	totals = {}
	simSum = {}
#	import pdb; pdb.set_trace()
	for other in prefs:
		if other == person: continue
		sim = similarity(prefs, person, other)
		if sim <= 0: continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item][RATING] == 0:
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item][RATING] * sim
				#Similarity sums
				simSum.setdefault(item, 0)
				simSum[item] += sim		
#	import pdb; pdb.set_trace()	
	rankings = [(total/simSum[item], item) for item,total in totals.items()]
	removed_items = [4325, 2423, 2009, 218, 228, 4319]
	#Testing: Checking if ratings match with that in dataset
"""	for (x, y) in rankings:
		for item in removed_items:
			if item == y:
				print (x, y)				
"""				
	rankings.sort()
	rankings.reverse() 	
	return rankings	

if __name__ == "__main__":
	main()	


