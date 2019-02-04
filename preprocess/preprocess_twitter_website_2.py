# This program loops through all dates from the beginning
# of 2012, and for each date it loops through each of 9
# tickers (these were chosen because they are mentioned
# frequently on Twitter). For each of the tickers, it
# finds the Tweets about that ticker on that day, then
# saves these Tweets along with their sentiment scores in
# a CSV (Comma Separated Value) file.

from bs4 import BeautifulSoup
import requests
import datetime
import time
import csv
from vaderSentiment import vaderSentiment

now = datetime.date.today()
start = datetime.date(2012, 1, 1)
currentDay = datetime.date(2012, 1, 1)
day = datetime.timedelta(days = 1)

tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA', 'YHOO', 'MSFT', 'EBAY', 'FB', 'TWTR']

csvFile = open('../data/twitter/text2.csv', 'w', encoding = 'utf-8', newline = '')
writer = csv.writer(csvFile)
writer.writerow(['text', 'id', 'pos', 'neu', 'neg', 'date', 'ticker'])

analyzer = vaderSentiment.SentimentIntensityAnalyzer()

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
		texts = [(''.join(tweet.findAll(text=True))).strip() for tweet in tweets]
		scores = [analyzer.polarity_scores(text) for text in texts]

		for i in range(len(tweets)):
			writer.writerow([texts[i], ids[i], scores[i]['pos'], scores[i]['neu'], scores[i]['neg'], str(currentDay), ticker])
	
	currentDay+=day
	percentDone = 100 * (currentDay-start) / (now-start)
	print(str(round(percentDone, 2)) + '% done... (' + str(round(time.time() - startTime, 2)) + ' seconds elapsed)', flush = True)

print('\nCompletely done! Closing files...')
csvFile.close()
print('All files closed.')
