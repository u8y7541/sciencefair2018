import csv
import numpy as np

# Adapted from https://www.geeksforgeeks.org/linear-regression-python-implementation/
def linear_regression(x, y):
	n = np.size(x)
	m_x, m_y = np.mean(x), np.mean(y)

	SS_xy = np.sum(y*x) - n*m_y*m_x
	SS_xx = np.sum(x*x) - n*m_x*m_x

	m = SS_xy / SS_xx
	b = m_y - m*m_x
	
	return (m, b)

csvfile = open('../data/NASDAQ_symbols_timeseries_missingpairing.csv')
tot_lines = len(csvfile.readlines())
csvfile.seek(0)
reader = csv.reader(csvfile)
next(reader)

DAYS_IN_ADVANCE = 100

index = 0
rmse = np.float64(0)
for row in reader:
	numbers = [float(i) for i in row[1:DAYS_IN_ADVANCE+1]]
	m, b = linear_regression(np.array(range(100)), np.array(numbers))
	diff = 100*m + b - np.float64(row[DAYS_IN_ADVANCE+1])
	rmse += (100*m + b - np.float64(row[DAYS_IN_ADVANCE+1]))**2
	
	index += 1
	if index % 10000 == 0:
		print(str(round(100*index/tot_lines)) + '% done')

print((rmse/index)**0.5)
