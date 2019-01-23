import quandl
import pandas
import random
import time

def normalize(array, val):
	s, l = min(array), max(array)
	if s == l:
		return [1 for i in array], 1
	return ([(i-s)/(l-s) for i in array], (val-s)/(l-s))

quandl.ApiConfig.api_key = '-6jCuGSa7HdrfzAVLdLi'

tickersFile = open('../data/NASDAQ_symbols_twitter/tickers')
tickers = [i[:-1] for i in tickersFile.readlines()]
tickersFile.close()

DAYS_IN_ADVANCE = 100 

data = pandas.DataFrame(columns = [str(i) for i in range(DAYS_IN_ADVANCE)]+['next', 'updown', 'ticker', 'startdate'])
for i in tickers:
	print('Ticker started: ' + str(i))
	begin = time.time()
	table = quandl.get_table("WIKI/PRICES", qopts = {'columns': ['close']}, ticker = [i])
	dates = quandl.get_table("WIKI/PRICES", qopts = {'columns': ['date']}, ticker = [i])
	# Reverse the table so that oldest comes first, making a proper time series
	table = table.reindex(index=table.index[::-1])
	table = table.reset_index(drop = True)
	dates = dates.reindex(index=dates.index[::-1])
	dates = dates.reset_index(drop = True)

	for j in range(len(table)-DAYS_IN_ADVANCE):
		ten_slice = table[j:j+DAYS_IN_ADVANCE].T
		ten_slice = ten_slice.rename(index = lambda x: j, columns = dict(zip(range(j, j+DAYS_IN_ADVANCE), [str(i) for i in range(DAYS_IN_ADVANCE)])))
		two_columns = pandas.DataFrame(data={'next': [table.at[j+DAYS_IN_ADVANCE, 'close']], 'updown': [1 if table.at[j+DAYS_IN_ADVANCE, 'close'] > table.at[j+DAYS_IN_ADVANCE-1, 'close'] else -1]}, index = [j])
		ten_slice = ten_slice.join(two_columns)
		two_other_columns = pandas.DataFrame(data={'ticker': [i], 'startdate': [dates.iloc[j]['date']]}, index = [j])
		ten_slice = ten_slice.join(two_other_columns)
		(normalized, predicted) = normalize(ten_slice.loc[j].tolist()[:-2], ten_slice.at[j, 'next'])
		for k in range(DAYS_IN_ADVANCE):
			ten_slice.at[j, str(k)] = normalized[k]
		ten_slice.at[j, 'next'] = predicted
		data = data.append(ten_slice)
	end = time.time()
	print('Ticker completed: ' + str(i))
	print('Time elapsed: ' + str(round(end - begin)) + ' seconds')
	print()

print('Shuffling...')
data = data.sample(frac=1, random_state = 12345) # Shuffle the data
data = data.reset_index(drop = True)
print('Shuffled.')
print('Writing to file...')
data.to_csv('../data/NASDAQ_symbols_timeseries.csv')
print('Done!')
