import os
from os.path import exists, join, basename, splitext
import numpy as np
import pandas as pd
import json


# from google.colab import drive

# drive.mount('/content/drive')

# working_dir = "drive/MyDrive/T9_Shared_Drive_2022/OpenPose_Output/SaanviFiles"
# os.chdir(working_dir)

def numOfFrames(i):
  if i == NUM_OF_VIDEOS - 1:
    return len(FOLDER) - FOLDER.index(videoList[i] + "_000000000000" + "_keypoints.json")
  return FOLDER.index(videoList[i+1] + "_000000000000" + "_keypoints.json") - FOLDER.index(videoList[i] + "_000000000000" + "_keypoints.json")

def addingStartingIndices():
  NUM_OF_PIECES = 0
  for i in range(NUM_OF_VIDEOS):
    frames = numOfFrames(i)
    starting = FOLDER.index(videoList[i] + "_000000000000" + "_keypoints.json")
    current = starting
    while current + NUM_FRAMES <= starting + frames:
      startingIndices.append(current)
      #print(current)
      current += NUM_FRAMES
      NUM_OF_PIECES += 1
  #print(startingIndices)
  return NUM_OF_PIECES


json_dir = "Saanvi4Frames"
NUM_FRAMES = 30 # number of frames per video clip (done to maximize # of data points)
# this code was run for 30, 50, and 100 for each set of data
# it turned out that 30 ended up working the best
videoList = ["4_1", "4_2", "4_3"] # list of video names, not including stuff like .mov or .mp4
NUM_OF_VIDEOS = len(videoList)
videoList.sort()



# for each video what person is the one we look at
POI = [0] * 26




  

# loop throguh all jsons in a video
# need to get a list of jsons
# sort them and find first indexis ( ake a list of those)
# for each video we take first 100 frames
# have to fix data for those frames
# Shove them in an arrays




# OpenPose, for whatever reason, seems to randomly flip some frames such that
# the x and y coordinates are swapped. This method checks if the frame coordinates
# are wider than taller, and if so, assumes that the frame was flipped, and flips it back.
def fixData(coordsListX, coordsListY):
  xMax = max(coordsListX)
  xMin = min(coordsListX)
  yMax = max(coordsListY)
  yMin = min(coordsListY)
  
  if xMax - xMin > yMax - yMin:
    return coordsListY, coordsListX # flip the two
  else:
    return coordsListX, coordsListY
  


# takes in the keypoint you want and returns the x-index in the json file for the ccodinate pair
def getIndex(keyPoint):
  return (keyPoint - 1) * 3


# takes in a json file name
# reads it
# fixes what needs fixing
# outputs a array with its relevent info
# videoIndex = int that says what vid it is (needed for POI)
# jsonFile = string name of the json file
def formatJsonData(jsonFile):

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
  
  for i in range(1,26):
    x = getIndex(i)
    y = x + 1
    coordsListX.append(dataList[x])
    coordsListY.append(dataList[y])
  
  X, Y = fixData(coordsListX, coordsListY) # to get it in the right order
  Kpoints.append(np.array(X))
  Kpoints.append(np.array(Y))

  
  return Kpoints
  
  
  



  # takes in list of json indecies and then processes those into a 2d array A[frames][info]
# videoIndex = int that says what vid it is (needed for POI)
# jsonStartingPos = at what json in the full list does the vid start (refer to loopVids() to understand)
def proccessVideo(jsonStartingPos):
  jsonFileList = FOLDER[jsonStartingPos : jsonStartingPos + NUM_FRAMES]
  Frames_data = []
  for jsonFile in jsonFileList:
    # print(jsonFile)
    Kpoints = np.array(formatJsonData(jsonFile))
    Frames_data.append(Kpoints)
  
  return Frames_data


# takes in name of folder of jsons (for all vids)
# returns a 4d data[vid][frames][x/y (0,1)][key_point] (3th dimension is either x or y)

# list of video names
data = [] # is the final 4d array 
startingIndices = []

# open folder
# DRIVE MUST ALREADY BE MOUNTED
FOLDER = os.listdir(json_dir) # the path will be different per person
FOLDER.sort()

NUM_OF_PIECES = addingStartingIndices()

#print(startingIndices)

# Now, iterate through the videos
for i in range(NUM_OF_PIECES):
  # PATH WILL BE DIFFERENT - make sure you change it, also should change Json_list
  vid_data = np.array(proccessVideo(startingIndices[i]))
  data.append(vid_data)

#print(data[0][0])
print(len(data))
print(len(data[0]))
print(len(data[1]))
print(data[0][0])
np.save('Saanvi4_30F', data) # saves file with all the data to drive
