import os, h5py
import numpy as np
import tensorflow as tf
import cv2

def extract_data(path):
    labels = []
    data = []
    numOfItems = 0
    for i, label in enumerate(sorted(os.listdir(path))):
        if (label == '.DS_Store'): # Gets rid of problem on MacOS
            pass
        else:
            for j, filename in enumerate(os.listdir(os.path.join(path, label))):
                image = cv2.imread(os.path.join(path, label, filename))
                image = cv2.resize(image, (64, 64))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                data.append(image)
                labels.append(i-1)
                numOfItems += 1
    data = np.array(data)
    labels = tf.keras.utils.to_categorical(labels, num_classes=None, dtype='float32') # One-hot; this seems to work
    return (data.reshape(numOfItems, 1, 64, 64), np.array(labels))

def normalize(trainX, testX):
    # Int to float
	train_norm = trainX.astype('float32')
	test_norm = testX.astype('float32')
    # Normalize between 0 and 1
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0
	return train_norm, test_norm

def plot_images(xval, yval):
    from matplotlib import pyplot as plt
    for i in range(9): # Plots 1st 9 images
        plt.subplot(330 + 1 + i)
        plt.imshow(xval[i], cmap=plt.get_cmap('gray'))
    plt.show()
    print('XY SHAPE: X=%s, y=%s' % (xval.shape, yval.shape))
    # cv2.imshow('abc', data[0]); cv2.waitKey(0); cv2.destroyAllWindows() # cv2 implementation - show the image at data[0]

# These two are for making predictions
def extract_data_predict(path):
    data = []
    image = cv2.imread(path)
    image = cv2.resize(image, (64, 64))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data.append(image)
    data = np.array(data)
    return (data.reshape(1, 1, 64, 64))

def normalize_predict(arr):
    # Int to float
	norm = arr.astype('float32')
	norm = norm / 255.0
	return norm


# train_path = '../data/train' # TODO: CHANGE LATER TO ACTUAL TRAINING SET
# test_path = '../data/test'
#
# # Call preprocessing functions
# print('Extracting Train...')
# (trainX, trainY) = extract_data(train_path)
# print('Extracting Test...')
# (testX, testY) = extract_data(test_path)
# print('Normalizing...')
# trainX, testX = normalize(trainX, testX)
# print('Saving...')
#
# with h5py.File('../data/compressed/trainX.h5', 'w') as f:
#     f.create_dataset('trainX', data=trainX, compression='gzip', compression_opts=9)
# with h5py.File('../data/compressed/testX.h5', 'w') as f:
#     f.create_dataset('testX', data=testX, compression='gzip', compression_opts=9)
# with h5py.File('../data/compressed/trainY.h5', 'w') as f:
#     f.create_dataset('trainY', data=trainY, compression='gzip', compression_opts=9)
# with h5py.File('../data/compressed/testY.h5', 'w') as f:
#     f.create_dataset('testY', data=testY, compression='gzip', compression_opts=9)
