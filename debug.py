import pandas as pd
import numpy as np

class AutoVivification(dict):
	#Ref: http://stackoverflow.com/questions/651794/whats-the-best-way-to-initialize-a-dict-of-dicts-in-python
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

df = pd.read_csv('LDOS-CoMoDa.csv', na_values=['-1'])
udb = AutoVivification() #data-store for [userid][itemid]
for rows in df.values:
		udb[rows[0]][rows[1]] = rows[2:19]

movies = {} #number of ratings per user
users = {} #number of items per user
for row in df.values:
	if users.has_key(row[0]):
		users[row[0]] += 1
	else:
		users[row[0]] = 1	
	if movies.has_key(row[1]):
		movies[row[1]] += 1
	else: 
		movies[row[1]] = 1
print len(users.keys()), len(movies.keys())

import operator
import pylab as pl
sorted_users = sorted(users.iteritems(), key=operator.itemgetter(1), reverse=True)
sorted_movies = sorted(movies.iteritems(), key=operator.itemgetter(1), reverse=True)
#print sorted_users
u = [x for (x,y) in sorted_users]
r = [y for (x,y) in sorted_users]
pl.bar(movies.keys(), movies.values())
pl.show()