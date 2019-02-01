import quandl
import pandas
import csv
import time
import plotly.plotly as py
import plotly.graph_objs as go

quandl.ApiConfig.api_key = '-6jCuGSa7HdrfzAVLdLi'

twitter = pandas.read_csv('../data/twitter/text2.csv')

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

for i in tickers:
	table = quandl.get_table("WIKI/PRICES", qopts = {'columns': ['date', 'close']}, date = {'gte': '2012-01-01'}, ticker = [i])
	table = table.reindex(index = table.index[::-1])
	data = [go.Scatter(x=table['date'], y=table['close'].diff()), go.Scatter(x=tickerDfs[i]['date'], y=tickerDfs[i]['pos']*100)]
	py.plot(data)
	if i == 'AMZN': break
