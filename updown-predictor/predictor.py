import tensorflow as tf
import pandas
import numpy as np
import shutil

tf.logging.set_verbosity(tf.logging.INFO)

# Read data
df = pandas.read_csv('../data/NASDAQ_symbols_timeseries_missingpairing.csv')
# Drop "next" column because we only want to predict if the stock moves up or down, as well as unneeded columns
df.drop(['next', 'ticker', 'startdate'], axis = 1, inplace = True)

DAYS_IN_ADVANCE = 100

# Moving average over each sample
df['avg'] = sum([df[str(i)] for i in range(DAYS_IN_ADVANCE)])/DAYS_IN_ADVANCE
# 2-day moving average
for i in range(DAYS_IN_ADVANCE-1):
	df['moving-avg-'+str(i)] = (df[str(i)]+df[str(i+1)])/2

df['updown'] = (df['updown'] + 1)/2

np.random.seed(1234)
msk = np.random.rand(len(df)) < 0.8
train, test = df[msk], df[~msk]

featcols = {str(i): tf.feature_column.numeric_column(str(i)) for i in list(range(DAYS_IN_ADVANCE))+['avg']+['moving-avg-'+str(i) for i in range(DAYS_IN_ADVANCE-1)]}

def make_input_fn(which, num_epochs):
	if which == 'train':
		data = train
		batch_size = 128
	else:
		data = test
		batch_size = len(test)
	return tf.estimator.inputs.pandas_input_fn(
			x = data[list(featcols.keys())],
			y = data['updown'],
			batch_size = batch_size,
			num_epochs = num_epochs,
			shuffle = True,
			queue_capacity = 1000,
			num_threads = 1
			)

train_epochs = 1 # TODO Change this
train_fn, test_fn = make_input_fn('train', train_epochs), make_input_fn('test', 1)

# DNN Regressor
def train_and_evaluate(output_dir, num_train_steps):
	myopt = tf.train.AdamOptimizer(learning_rate = 0.0005) # note the learning rate
	estimator = tf.estimator.DNNRegressor(
				model_dir = output_dir, 
				hidden_units = [64, 32, 16],
				dropout = 0.1,
				feature_columns = featcols.values(),
				optimizer = myopt)

	#Add rmse evaluation metric
	def rmse(labels, predictions):
		pred_values = tf.cast(predictions['predictions'],tf.float64)
		return {'rmse': tf.metrics.root_mean_squared_error(labels, pred_values)}
	estimator = tf.contrib.estimator.add_metrics(estimator,rmse)
	
	train_spec=tf.estimator.TrainSpec(
			input_fn = train_fn,
			max_steps = num_train_steps)
	eval_spec=tf.estimator.EvalSpec(
			input_fn = test_fn,
			steps = None,
			start_delay_secs = 1, # start evaluating after N seconds
			throttle_secs = 10,  # evaluate every N seconds
			)
	tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)

shutil.rmtree('./outdir', ignore_errors = True)
train_and_evaluate('./outdir', num_train_steps = (100 * len(train)) / 128)
