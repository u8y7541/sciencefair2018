import tensorflow as tf
import numpy as np

a = tf.constant([1, 2, 3], shape=(3,))
b = tf.constant([2, 3, 4], shape=(3,))
c = tf.add(a, b)

sess = tf.Session()
result = sess.run(c)
print(result)
