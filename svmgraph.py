import numpy as np
from sklearn import svm
from sklearn.utils import shuffle
from PIL import Image
from os import listdir
import os
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

# from google.colab import drive

# drive.mount('/content/drive')

# working_dir = "drive/MyDrive/T9_Shared_Drive_2022/RawData"
# os.chdir(working_dir)

# this is the number of frames per data point we want (we proccesed many diff one)
num = "30"





size = 200, 200

# Training True

# get the path/directory
Tfolder_dir = "SimImg" + num 
Ffolder_dir = "UnSimImg" + num
# Tfolder_dir = "Unhealthy30F_output_2022-07-27_18:48:18"
# Ffolder_dir = "Healthy30F_output_2022-07-27_18:48:13"


TList = listdir(Tfolder_dir)
FList = listdir(Ffolder_dir)

# to keep data balanced this is the ammount of data points per catagory
k = min(len(TList), len(FList))


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
X = X.reshape((nsamples,nx*ny))

# test train split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40, stratify=y)


# checking that its all balanced
k = 0
for i in y_test:
  k += i

print(k)
print(len(y_test))






svc = svm.SVC(kernel = 'rbf')
svc.fit(X_train, y_train)



# predict and accuracy

predY = svc.predict(X_test)

accuracy_score(y_test, predY)


confusion_matrix(y_test, predY)
