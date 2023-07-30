import os
from os.path import exists, join, basename, splitext
import numpy as np
import pandas as pd
import json

from google.colab import drive

drive.mount('/content/drive')

working_dir = "drive/MyDrive/T9_Shared_Drive_2022/OpenPose_Output/"
os.chdir(working_dir)


json_dir = "OpenposeSampleOutput"
NUM_FRAMES = 100 # number of frames we take from the vid
videoList = ['Ashita1', 'Ashita2', 'Em1', 'Em2', 'Em3', 'Em4', 'Jai1', 'Jai2', 'Jai3', 'Jai4', 'Jai5', 'Jai6', 'Jai7', 'Jai8', 'Jue1', 'Jue2', 'Jue3', 'Jue4', 'Kayla1', 'Kayla2', 'Lily1', 'Lily2', 'Lily3'] # list of videos
videoList.sort()



# for each video what person is the one we look at
POI = [0] * 26




  

# loop throguh all jsons in a video
# need to get a list of jsons
# sort them and find first indexis ( ake a list of those)
# for each video we take first 100 frames
# have to fix data for those frames
# Shove them in an arrays



# flips
def fixData(coordsListX, coordsListY):
  xMax = max(coordsListX)
  xMin = min(coordsListX)
  yMax = max(coordsListY)
  yMin = min(coordsListY)
  
  if xMax - xMin > yMax - yMin:
    return coordsListY, coordsListX # flip the two
  else:
    return coordsListX, coordsListY
  


# takes in the keypoint you want and returns the index in the json file for the ccodinate pair
def getIndex(keyPoint):
  return (keyPoint - 1) * 3


# takes in a json file name
# reads it
# fixes what needs fixing
# outputs a array with its relevent info
# videoIndex = int that says what vid it is (needed for POI)
# jsonFile = string name of the json file
def formatJsonData(videoIndex, jsonFile):

  # The dictionary with the data in it
  with open(json_dir + '/' + jsonFile, 'r') as f:
    dataDictionary = json.load(f)

  # print(jsonFile)
  k = dataDictionary['people']
  if len(k) <= 0:
    return [[0]*25] * 2

  dataList = k[0]['pose_keypoints_2d']
  coordsListX = []
  coordsListY = []
  Kpoints = []
  
  for i in range(25):
    x = getIndex(i)
    y = x + 1
    coordsListX.append(dataList[x])
    coordsListY.append(dataList[y])
  
  X, Y = fixData(coordsListX, coordsListY)
  Kpoints.append(np.array(X))
  Kpoints.append(np.array(Y))
  
  
  return Kpoints
  
  
  



  # takes in list of json indecies and then processes those into a 2d array A[frames][info]
# videoIndex = int that says what vid it is (needed for POI)
# jsonStartingPos = at what json in the full list does the vid start (refer to loopVids() to understand)
def proccessVideo(videoIndex, jsonStartingPos):
  jsonFileList = FOLDER[jsonStartingPos : jsonStartingPos + NUM_FRAMES]
  Frames_data = []
  for jsonFile in jsonFileList:
    # print(jsonFile)
    Kpoints = np.array(formatJsonData(videoIndex, jsonFile))
    Frames_data.append(Kpoints)
  
  return Frames_data




# takes in name of folder of jsons (for all vids)
# returns a 4d data[vid][frames][key_point][x/y (0,1)] (4th dimension is either x or y)

# list of video names
data = [] # is the final 4d array 

# open folder
# DRIVE MUST ALREADY BE MOUNTED
FOLDER = os.listdir(json_dir) # the path will be different per person
FOLDER.sort()


# Now, iterate through the videos
for i in range(len(videoList)):
  video = videoList[i]
  # PATH WILL BE DIFFERENT - make sure you change it, also should change Json_list
  startIndex = FOLDER.index(video + "_000000000000" + "_keypoints.json")
  
  vid_data = np.array(proccessVideo(i, startIndex))
  data.append(vid_data)


s = pd.DataFrame(data[1][69])
s
