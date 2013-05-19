import scipy as sc
import pylab as pl
import recallPrecision as rp
prs = sc.rand(15,2) # precision recall point list
labels = ["item " + str(i) for i in range(15)] # labels for the points
rp.plotPrecisionRecallDiagram("footitle", prs, labels)
pl.show()