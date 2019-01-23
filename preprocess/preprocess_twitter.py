import searchtweets
import codecs
import datetime

searchtweets.load_credentials(filename = 'twitter_keys.yaml', yaml_key = 'search_tweets_api', env_overwrite = False)

tickersFile = open('../data/NASDAQ_symbols_twitter/tickers')
tickers = [i[:-1] for i in tickersFile.readlines()]
tickersFile.close()
queryString = ' OR '.join(tickers)
print(len(queryString))

begin = datetime.datetime(2006, 3, 21)
today = datetime.datetime.now()
NUM_REQUESTS = 47
delta = (today-begin)/NUM_REQUESTS

