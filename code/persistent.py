import pandas as pd
import numpy as np
import math
import pdb

#For indexing the movie rating from the user dictionary
RATING = 0
OPTIMUM = 4.0

class AutoVivification(dict):
	#Ref: http://stackoverflow.com/questions/651794/whats-the-best-way-to-initialize-a-dict-of-dicts-in-python
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def shuffle(df):
	#Randomizes the dataframe
	#Reference: http://stackoverflow.com/questions/13395725/efficient-way-of-doing-permutations-with-pandas-over-a-large-dataframe
	ind = df.index
	sampler = np.random.permutation(df.shape[0])
	new_vals = df.take(sampler).values
	df = pd.DataFrame(new_vals, index=ind)
	return df            

def buildUserProfile(filename):
	"""
	Builds a dictionary of User Profiles by parsing through the file
	{user1: c1, c2, c5, c6}
	"""
	pass

def remove_for_testing(udb, user):
	limit = int(len(udb[user])/3.0)
	import copy;
	temp_udb, i = copy.deepcopy(udb), 0
	for movie in udb[user]:
		del(temp_udb[user][movie])
		i += 1
		if i > limit: break
	return temp_udb


def main(user=15, filters=None):
	df = pd.read_csv('../datasets/LDOS-CoMoDa.csv', na_values=['-1'])
	#df = shuffle(df)
	#Replacement of missing values using the mean of the available values.
	for c in df.columns:
		mean = df[c].mean()
		df[c].fillna(mean)		
	#Storing in a dictionary	
	N = df.shape[0] #Number of training samples
	train_len = int(N * 2/3.0)
	udb = AutoVivification() #data-store for [userid][itemid] for training
	mdb = {} #moviedatabase
	"""
	users = {userid: {itemid: rating, age,sex,city,country, c1, c2, ................, c12}}
	items = {itemid: {director, a1, a2, a3, g1, g2, g3, budget, lang, country}}
	"""
	#rows 2-19 user and contextual attributes
	#19-30 movie attributes
	count = 0
	for rows in df.values:
		if rows[0] == user:
			count += 1 #No of ratings for the specific user
		udb[rows[0]][rows[1]] = rows[2:19]
		mdb[rows[1]] = rows[19:]

	udb = remove_for_testing(udb, user, count)	
	


	#print sim_euclidean(udb, 254, 15)
	#print sim_pearson(udb, 15, 195)
	#print top_matches(udb, 15)
	#recs =  get_recommendations(udb, 15)
	#print precision(15, recs, test_udb)
	#print recall(15, recs, test_udb)
	#filters = [(15, 1), (16, 2)]
	#profiles = {15: [14, 15, 16]}
	#print contextual_filter(udb, profiles, user, recs, filters)

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
	#Testing: Checking if ratings match with that in dataset
	rankings.sort()
	rankings.reverse() 	
	return rankings

def contextual_filter(udb, profiles, user, recommendations, filters):
	"""
	Profiles: User Profile built based on Information gain of Contextual attributes
	Recommendations: Generated by Collaborative Filtering
	Filters: User entered Contextual Attributes	
	"""
	print len(recommendations)
	filtered_recs = []
	for rating, movie in recommendations:
		if rating >= OPTIMUM:
			for context, value in filters:
				if context in profiles[user]:
					avg = round(findAvgContext(movie, context, udb))	
					if avg == value and (rating, movie) not in filtered_recs:
						filtered_recs.append((rating, movie))
	return len(filtered_recs)				

def findAvgContext(movie, context, udb):
	sumOfContext = 0
	count = 0
#	pdb.set_trace()
	for user in udb:
		if udb[user][movie][context] != {} and udb[user][movie][RATING] >= OPTIMUM:
			sumOfContext += udb[user][movie][context]
			count += 1		
	return sumOfContext/count			

def precision(user, recommendations, udb):
#	pdb.set_trace()
	all = len(recommendations)
	tp = 0
	for (x, y) in recommendations:
		for movie in udb[user].keys():
			if movie == y:
				tp += 1
				if udb[user][movie][RATING] == x:
					tp += 2
	#print tp, all				
	return tp/all

def recall(user, recommendations, udb):
	#pdb.set_trace()
	tp = 0
	good_movies = 0
	for movie in udb[user].keys():
		if udb[user][movie][RATING] >= 4:
				good_movies += 1		
		for (x, y) in recommendations:
			if movie == y:
				tp += 1
			
	#print tp, good_movies				
	return tp/good_movies			

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 2:
		user = eval(sys.argv[1]) #Userid, Default: 15
		filters = eval(sys.argv[2]) #List of Contextual Filters: [(c1, v1), (c2, v2)], Default: None
		main(user, filters)
	main()		
