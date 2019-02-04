# This program first finds an average positive, negative and
# neutral score for each company for each day based on the
# Twitter data gathered by preprocess_twitter_website_2.py.
# Then, it loops through the stock data from
# preprocess_nasdaq.py and matches the hundred days of
# stock data in each sample in this file to a corresponding
# hundred days of positive, negative, and neutral average
# Twitter sentiment scores. It then saves the combined data
# to a CSV (Comma Separated Value) file.

import pandas
import csv
import time

twitter = pandas.read_csv('../data/twitter/text2.csv')
stock = pandas.read_csv('../data/NASDAQ_symbols_timeseries.csv')
tot_length = len(stock.index)

tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA', 'YHOO', 'MSFT', 'EBAY', 'FB', 'TWTR']
tickerDfs = {i:pandas.DataFrame(columns = ['date', 'pos', 'neu', 'neg']) for i in tickers}

numTweets = 0
scores = {'pos': 0, 'neu': 0, 'neg': 0}
currentTicker = ''
date = ''

for (index, row) in twitter.iterrows():
	if row['ticker'] != currentTicker:
		if date != '':
			toAppend = {}
			toAppend['date'] = date
			toAppend['pos'] = scores['pos']/numTweets
			toAppend['neu'] = scores['neu']/numTweets
			toAppend['neg'] = scores['neg']/numTweets
			tickerDfs[currentTicker] = tickerDfs[currentTicker].append(toAppend, ignore_index = True)

		scores = {'pos': 0, 'neu': 0, 'neg': 0}
		date = row['date']
		currentTicker = row['ticker']
		numTweets = 0
	scores['pos'] += row['pos']
	scores['neu'] += row['neu']
	scores['neg'] += row['neg']
	numTweets += 1

DAYS_IN_ADVANCE = 100

csvfile = open('../data/twitter/paired_stock_twitter.csv', 'w', newline = '')
writer = csv.writer(csvfile)

sentiment_list = []
for i in range(DAYS_IN_ADVANCE):
	sentiment_list += ['pos_'+str(i), 'neu_'+str(i), 'neg_'+str(i)]

tickers = [i.lower() for i in tickers]

writer.writerow([i for i in range(DAYS_IN_ADVANCE)] + sentiment_list + ['next', 'updown', 'ticker', 'startdate'])
print('Starting...')
startTime = time.time()
for (index, row) in stock.iterrows():
	if row['ticker'] not in tickers:
		continue
	if int(row['startdate'][:4]) < 2012:
		continue
	toWrite = []
	for i in range(DAYS_IN_ADVANCE):
		toWrite.append(row[str(i)])

	rowNumber = 0
	for (index2, row2) in tickerDfs[row['ticker'].upper()].iterrows():
		if row2['date'] == row['startdate']:
			rowNumber = 1
		if rowNumber == 0: continue
		toWrite.append(row2['pos'])
		toWrite.append(row2['neu'])
		toWrite.append(row2['neg'])
		rowNumber += 1
		if rowNumber > DAYS_IN_ADVANCE:
			break
	if rowNumber != DAYS_IN_ADVANCE + 1:
		continue
	
	toWrite.append(row['next'])
	toWrite.append(row['updown'])
	toWrite.append(row['ticker'])
	toWrite.append(row['startdate'])
	
	writer.writerow(toWrite)

	print(str(round(100*index/tot_length, 2)) + '% done... (' + str(round(time.time() - startTime)) + ' seconds elapsed)') 

	if index == 1000:
		break

print('Completed!')
print('Closing files...')
csvfile.close()
print('All files closed.')
