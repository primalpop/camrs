import csv as csv
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier

import pdb

train=csv.reader(open('datasets/train.csv','rb')) #open file
headerx=train.next()

x=[]
for row in train:
	for i in range(len(row)):
		if row[i] == '-1':
			row[i] = 1
		else:
			row[i] = eval(row[i])	
	x.append(row)
	#pdb.set_trace()
x=np.array(x)

category=csv.reader(open('datasets/target.csv','rb')) #open file
headery=category.next()

y=[]
for row in category:
	for i in range(len(row)):
		if row[i] == '-1':
			row[i] = 1
		else:
			row[i] = eval(row[i])
	y.append(row)
y=np.array(y)

clf=LinearSVC()
clf = clf.fit(x,y)

test=csv.reader(open('datasets/test.csv','rb'))
headert=test.next()
new=[]
for row in test:
	new.append(row)
new=np.array(new).astype(np.float)

#resultset=clf.predict(new).astype(np.float)
#print resultset
#np.savetxt('results.csv',resultset,delimiter=",")

cR = chi2(x, y)

# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=250,
                              compute_importances=True,
                              random_state=0)

forest.fit(x, y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print "Feature ranking:"

for f in xrange(10):
    print "%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]])
 
# Plot the feature importances of the forest
import pylab as pl
pl.figure()
pl.title("Feature importances")
#pl.bar(xrange(10), importances[indices],
#       color="r", yerr=std[indices], align="center")
pl.xticks(xrange(10), indices)
pl.xlim([-1, 10])
pl.show() 