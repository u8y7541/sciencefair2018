import tensorflow as tf
import quandl
import pandas
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

def normalize(arr, val):
	s, l = min(arr), max(arr)
	if s == l:
		return [1 for i in array], 1
	return ([(i-s)/(l-s) for i in arr], (val-s)/(l-s), s, l) 

quandl.ApiConfig.api_key = '-6jCuGSa7HdrfzAVLdLi'

tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA', 'YHOO', 'MSFT', 'EBAY', 'FB', 'TWTR']

DAYS_IN_ADVANCE = 100

feature_names = [str(i) for i in list(range(DAYS_IN_ADVANCE))+['avg']+['moving-avg-'+str(i) for i in range(DAYS_IN_ADVANCE-1)]]
featcols = {i: tf.feature_column.numeric_column(i) for i in feature_names}
estimator_next = tf.estimator.DNNClassifier(model_dir = '../next-predictor/outdir_good_tr3', feature_columns = featcols.values(), hidden_units = [64, 32, 16], warm_start_from = '../next-predictor/outdir_good_tr3')

for i in tickers:
	to_predict = dict(zip(feature_names, [np.array([]) for i in range(len(feature_names))]))
	sl_list = []
	table = quandl.get_table("WIKI/PRICES", qopts = {'columns': ['close', 'date']}, ticker = [i], date = {'gte': '2012-01-01'})

	for j in range(len(table)-DAYS_IN_ADVANCE):
		hundred_slice = table[j:j+DAYS_IN_ADVANCE]['close']
		(normalized, predicted, s, l) = normalize(hundred_slice, table.at[j+DAYS_IN_ADVANCE, 'close'])
		sl_list.append((s, l))

		for k in range(DAYS_IN_ADVANCE):
			to_predict[str(k)] = np.append(to_predict[str(k)], normalized[k])
			if k != DAYS_IN_ADVANCE-1:
				to_predict['moving-avg-'+str(k)] = np.append(to_predict['moving-avg-'+str(k)], (normalized[k]+normalized[k+1])/2)
		to_predict['avg'] = np.append(to_predict['avg'], np.mean(normalized))

	predict_input_fn = tf.estimator.inputs.numpy_input_fn(x=to_predict, num_epochs=1, shuffle=False)
	predictions = [i['logits'][0] for i in list(estimator_next.predict(input_fn = predict_input_fn))]
	predictions = [predictions[j]*(sl_list[j][1]-sl_list[j][0]) + sl_list[j][0] for j in range(len(predictions))]
	data = [go.Scatter(x=table[DAYS_IN_ADVANCE:]['date'], y=table[DAYS_IN_ADVANCE:]['close']), go.Scatter(x=table[DAYS_IN_ADVANCE:]['date'], y=predictions)]
	py.plot(data, filename = i)
