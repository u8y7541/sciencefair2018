# This program loops through the stock data from
# preprocess_nasdaq.py. For each sample, it performs simple
# linear regression on the 100 days of data to get the 101st
# day. It then adds to the closeness and directional RMSEs.
# Finally, it finalizes the RMSE calculations and displays
# the RMSEs.

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

csvfile = open('../data/NASDAQ_symbols_timeseries.csv')
tot_lines = len(csvfile.readlines())
csvfile.seek(0)
reader = csv.reader(csvfile)
next(reader)

DAYS_IN_ADVANCE = 100

index = 0
rmse = np.float64(0)
rmse_dir = np.float64(0)
for row in reader:
	numbers = [float(i) for i in row[1:DAYS_IN_ADVANCE+1]]
	m, b = linear_regression(np.array(range(100)), np.array(numbers))
	val = 100*m + b
	diff = val - np.float64(row[DAYS_IN_ADVANCE+1])
	rmse += diff**2
	
	direction = (0 if diff<0 else 1)
	expected = (0 if row[DAYS_IN_ADVANCE]<row[DAYS_IN_ADVANCE+1] else 1)
	rmse_dir += (direction-expected)**2
	
	index += 1
	if index % 10000 == 0:
		print(str(round(100*index/tot_lines)) + '% done')

print('Closeness RMSE: ' + str((rmse/index)**0.5))
print('Directional RMSE: ' + str((rmse_dir/index)**0.5))
