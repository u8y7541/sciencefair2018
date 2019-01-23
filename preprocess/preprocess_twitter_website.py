from bs4 import BeautifulSoup
import requests
import datetime
import time

now = datetime.date.today()
start = datetime.date(2012, 1, 1)
currentDay = datetime.date(2012, 1, 1)
day = datetime.timedelta(days = 1)

#tickersFile = open('../data/NASDAQ_symbols_twitter/tickers')
#tickers = [i[:-1].upper() for i in tickersFile.readlines()]
#tickersFile.close()

tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA', 'YHOO', 'MSFT', 'EBAY', 'FB', 'TWTR']

fileHandles = {}
for ticker in tickers:
	fileHandles[ticker] = open('../data/twitter/'+ticker, 'w')

startTime = time.time()
while currentDay != now:
	for ticker in tickers:
		since = currentDay.isoformat()
		until = (currentDay+day).isoformat()
		requestStr = 'https://mobile.twitter.com/search?q='+ticker
		requestStr += '+since%3A' + since
		requestStr += '+until%3A' + until
		requestStr += '&s=typd&x=0&y=0'

		search = requests.get(requestStr)
		soup = BeautifulSoup(search.text, 'lxml')
	
		tweets = soup.find_all("div", class_ = "tweet-text")
		ids = [tweet['data-id'] for tweet in tweets]

		fileHandles[ticker].write('\n'.join(ids)+'\n')
	
	currentDay+=day
	percentDone = 100 * (currentDay-start) / (now-start)
	print(str(round(percentDone, 2)) + '% done... (' + str(round(time.time() - startTime, 2)) + ' seconds elapsed)', flush = True)

print('\nCompletely done! Closing files...')
for ticker in tickers:
	fileHandles[ticker].close()
print('All files closed.')
