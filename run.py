import os
from os.path import exists, join, basename, splitext
import numpy as np
import json
from sklearn import svm
from sklearn.utils import shuffle
from google.colab import drive
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.model_selection import train_test_split
import shutil
drive.mount('/content/drive')

working_dir = "drive/MyDrive/T9_Shared_Drive_2022/ProgrammingFiles"
os.chdir(working_dir)

#################################
# run above ONCE during session!! (seperate cell)
#################################


# git_repo_url = 'https://github.com/CMU-Perceptual-Computing-Lab/openpose.git'
# project_name = splitext(basename(git_repo_url))[0]
# if not exists(project_name):
#   # see: https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/949
#   # install new CMake becaue of CUDA10
#   !wget -q https://cmake.org/files/v3.13/cmake-3.13.0-Linux-x86_64.tar.gz
#   !tar xfz cmake-3.13.0-Linux-x86_64.tar.gz --strip-components=1 -C /usr/local
#   # clone openpose
#   !git clone -q --depth 1 $git_repo_url
#   !sed -i 's/execute_process(COMMAND git checkout master WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/execute_process(COMMAND git checkout f019d0dfe86f49d1140961f8c7dec22130c83154 WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/g' openpose/CMakeLists.txt
#   # install system dependencies
#   !apt-get -qq install -y libatlas-base-dev libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev opencl-headers ocl-icd-opencl-dev libviennacl-dev
#   # install python dependencies
#   !pip install -q youtube-dl
#   # build openpose
#   !cd openpose && rm -rf build || true && mkdir build && cd build && cmake .. && make -j`nproc`
#   !cd ..




# Include path to file. Example: Healthy/myvideo.mp4
def runOpenPose(file_path):
  !cd openpose && ./build/examples/openpose/openpose.bin --video $file_path --write_json ../output/ --display 0  --write_video ../openpose.avi
 


# takes in the dict of open pose data
# output a 1d array of the data we want to use
# probably want output as np array
# may have to change around what we put in etc
def selectData(X):
  # IMPORTANT - currently, this just returns all of the numbers in one array
  # based on the desicions of the medical/research team,
  # we will edit this function to just output certain data such as 
  # just certain limbs or angles etc
  output = []
  for dict in X:
    pose = dict['people'][0]['pose_keypoints_2d']
    for i in range(len(pose)):
      if i % 3 == 0:
        output.append(pose[i])
      if i % 3 == 1:
        output.append(pose[i])
  
  return output
  # return data['people'][0]['pose_keypoints_2d']




# function to read and format the Json
# pass in list x and folder for json files
# will populate x with the position data for 100 frames
# this will run in loop over all videos
FRAMES = 100
def ReadJsons(folder_dir,X):
  # get all files in folder take first couple 
  # !!! problem !!!! how do we make sure that we get the files in order
  files = os.listdir(folder_dir)[:FRAMES]
  files.sort()
  x = []
  for F in files:
    # load int a json into dict data
    f = open(folder_dir + "/" + F)
    data = json.load(f)
    x += selectData(data)

  # add this data point to the list of data points
  X.append(np.array(x))
            
  
  
  
  
 
# data collection + running opepose + reading jsons
  
  
  
 
# getting the data
X = []
y = []

# locations of the data folders
Healty_folder = "Healthy"
Sick_folder = "UnHealthy"
  
  
  
# get healthy data points
Healthy_files = os.listdir(Healty_folder)
for vid in Healthy_files:
  # run openpose
  runOpenPose(vid)
  
  # compile the position data and put it in X
  ReadJsons("output", X)
  y.append(1)

  # delete files in ./output to clear for next run of openpose
  !rm -r output
  

# get unhealthy data points
Sick_files = os.listdir(Sick_folder)
for vid in Sick_files:
  # run openpose
  runOpenPose(vid)
  
  # compile the position data
  ReadJsons("output", X)
  y.append(0)

  
  # delete files in ./output to clear for next run of openpose
  !rm -r output
  
  
    
    
    
    
    
    
    
    
    
    
 # ML   
    
    
    
    
# train test split
X, y = shuffle(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# train model    
regr = svm.SVR(kernel = 'rbf')
regr.fit(X_train, y_train)

# predict and accuracy
predY = regr.predict(X_test)
mean_absolute_error(y_test, predY)

# turning score into classification
a = []
for x in predY:
  if x >= .5:
    a.append(1)
    continue
  a.append(0)

isSick = np.array(a)
accuracy_score(y_test, isSick)
