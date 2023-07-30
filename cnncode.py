import numpy as np
from sklearn import svm
from sklearn.utils import shuffle
from PIL import Image
from os import listdir
import os
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

from tensorflow import keras
from keras.datasets import mnist

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.utils import to_categorical

# drive mounting to folders

from google.colab import drive

drive.mount('/content/drive')

working_dir = "drive/MyDrive/T9_Shared_Drive_2022/RawData"
os.chdir(working_dir)

num = "30"

size = 200, 200

# Training True

# get the path/directory
Tfolder_dir = "SimImg" + num 
Ffolder_dir = "UnSimImg" + num



TList = listdir(Tfolder_dir)
FList = listdir(Ffolder_dir)

# to keep data balanced this is the ammount of data points per catagory
k = min(len(TList), len(FList


tags = []
loaded_images = list()
for filename in TList[:k]:
  # load image
  img_data = Image.open(Tfolder_dir + '/' + filename)
  gs_image = img_data.convert(mode='L')
  gs_image = gs_image.resize(size, Image.ANTIALIAS)
  ImgArray = np.array(gs_image)
	# store loaded image
  loaded_images.append(ImgArray)
  tags.append(1)



# Training false

# get the path/directory
for filename in FList[:k]:
  # load image
  img_data = Image.open(Ffolder_dir + '/' + filename)
  gs_image = img_data.convert(mode='L')
  gs_image = gs_image.resize(size, Image.ANTIALIAS)
  ImgArray = np.array(gs_image)
	# store loaded image
  loaded_images.append(ImgArray)
  tags.append(0)


# put arrays into numpy and shuffle it
X = np.array(loaded_images)
y = np.array(tags)

X, y = shuffle(X, y)


nsamples, nx, ny = X.shape

#test train split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=40, stratify=y)

			
# k = 0
# for i in y_test:
#   k += i

# print(k)
# print(len(y_test))

def baseline_model(inputShape = (200,200,1)):
	# create model
	model = Sequential()
	model.add(Conv2D(32, (5, 5), input_shape=inputShape, activation='relu'))
	model.add(MaxPooling2D())
	model.add(Flatten())
	model.add(Dense(1, activation='relu'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
  
def fitting_model(model, x, y, epoch):
    model.fit(x,y, shuffle = True, epochs = epoch)

			

			
			
			
model = baseline_model()
fitting_model(model, X_train, y_train, epoch = 1)


# predict and accuracy
predY = model.predict(X_test)




accuracy_score(y_test, predY)

confusion_matrix(y_test, predY)
