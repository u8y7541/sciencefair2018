import csv
import datetime
import twitter
from vaderSentiment import vaderSentiment

tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA', 'YHOO', 'MSFT', 'EBAY', 'FB', 'TWTR']
fileHandles = {}
for ticker in tickers:
	fileHandles[ticker] = open('../data/twitter/'+ticker)

csvFile = open('../data/twitter/text.csv', 'w', encoding = 'utf-8', newline = '')
writer = csv.writer(csvFile)
writer.writerow(['text', 'pos', 'neu', 'neg', 'date', 'ticker'])

api = twitter.Api(consumer_key = 'z7aG3y8yZ4KKiOLgfwNG0mLIP',
		consumer_secret = 'p8IEyJlbumuy30yC65iMwmflo9awf6CUOIxxfQxUSJA4FFUfvi',
		access_token_key = '745635687781720065-dHxnhIdE9MWy6PIXYnf45tl6xx4EqOm',
		access_token_secret = 'bmQ1303lG4HbC7rH7dfo7JkrPT9vdDgTPzXZ8xM60qybZ')

analyzer = vaderSentiment.SentimentIntensityAnalyzer()

for ticker in tickers:
	while True: 
		tweetID = fileHandles[ticker].readline()
		if tweetID == '': break
		if tweetID[-1] == '\n': tweetID = tweetID[:-1]

		status = api.GetStatus(tweetID).AsDict()
		date = datetime.datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S %z %Y').date().isoformat()
		score = analyzer.polarity_scores(status['text'])

		writer.writerow([status['text'], score['pos'], score['neu'], score['neg'], date, ticker])

csvFile.close()
for ticker in tickers:
	fileHandles[ticker].close()
