import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import statsmodels.api as sm

def main():
	#missing value - ? 
	df = pd.read_csv('LDOS-CoMoDa.csv', na_values=['-1'])
	df.columns = ['userID',
 'itemID',
 'rating',
 'age',
 'sex',
 'city',
 'country',
 'time',
 'daytype',
 'season',
 'location',
 'weather',
 'social',
 'endEmo',
 'dominantEmo',
 'mood',
 'physical',
 'decision',
 'interaction',
 'director',
 'movieCountry',
 'movieLanguage',
 'movieYear',
 'genre1',
 'genre2',
 'genre3',
 'actor1',
 'actor2',
 'actor3',
 'budget']

#	print pd.crosstab(df['mood'], df['rating'])
	#histograms for various context information
#	df['social'].hist()
#	pl.show()

	print df.head()

	train_cols = df.columns[11:15]
	print train_cols
	

if __name__ == "__main__":
	main()