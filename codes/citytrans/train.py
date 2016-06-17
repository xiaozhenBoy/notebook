import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
import sys

train_file = sys.argv[1]
test_file = sys.argv[2]
out_file = sys.argv[3]

train_x = np.loadtxt(train_file)

test = np.loadtxt(test_file)

train = train_x
test = test[:, 1:]

train_x = train[:, 2:]

train_y = train[:, 0]

print train_x.shape, train_y.shape

print test.shape

min_max_scaler = preprocessing.MinMaxScaler()

min_max_scaler.fit(train_x)

train_x_scaler = min_max_scaler.transform(train_x)
test_scaler = min_max_scaler.transform(test)

regtool = RandomForestRegressor(n_estimators=100, max_depth=10)
regtool.fit(train_x_scaler, train_y)

test_y_pre = regtool.predict(test_scaler)

fout = open(out_file, 'w')

for val in test_y_pre:
    fout.write('%0.6f\n' % val)
fout.close()
