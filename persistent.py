import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import statsmodels.api as sm

class AutoVivification(dict):
	#Ref: http://stackoverflow.com/questions/651794/whats-the-best-way-to-initialize-a-dict-of-dicts-in-python
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def insert(mdb, user, item, attrs):
	for rows in df.values:
		mdb[rows[0]][rows[1]] = rows[2:19]

def main():
	df = pd.read_csv('LDOS-CoMoDa.csv', na_values=['-1'])
	udb = AutoVivification() #data-store for [userid][itemid]
	mdb = {} #moviedatabase
	"""
	users = {userid: {itemid: rating, age,sex,city,country, c1, c2, ................, c12}}
	items = {itemid: {director, a1, a2, a3, g1, g2, g3, budget, lang, country}}
	"""
	for rows in df.values:
		udb[rows[0]][rows[1]] = rows[2:19]
		mdb[rows[1]] = rows[19:]
		
# Returns a distance-based similarity score for person1 and person2
def sim_euclidean(udb, user1, user2):
	sim = {}    
	for item in udb[user1]:
		if item in udb[user2]:
			sim[item] = 1

	if len(sim) == 0: return 0 #No similarities
	dist = 0.0
#	pdb.set_trace()
	for item in sim:
		dist += pow((udb[user1][item][0] - udb[user2][item][0]),2)

	return 1/(1 + dist)		

