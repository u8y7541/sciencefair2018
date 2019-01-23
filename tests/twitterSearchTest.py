import searchtweets
import codecs
sandbox_search_args = searchtweets.load_credentials('twitter_keys.yaml', yaml_key = 'search_tweets_api', env_overwrite = False);

rule = searchtweets.gen_rule_payload("NASDAQ", results_per_call = 100)
tweets = searchtweets.collect_results(rule, max_results = 100, result_stream_args = sandbox_search_args)

f = codecs.open('sample_tweets.txt', 'w', 'utf-8') # Supports emojis
for tweet in tweets:
	#print(tweet.all_text + '\n\n')
	f.write(tweet.all_text + '\n')
f.close()

