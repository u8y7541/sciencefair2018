import quandl
quandl.ApiConfig.api_key = "-6jCuGSa7HdrfzAVLdLi"
google = quandl.get_table("WIKI/PRICES", ticker = ['GOOG'])
print(google.head())
print(type(google))
