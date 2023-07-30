import math
import pandas as pd
import numpy as np

def angle_deg(x1,y1,x2,y2,x3,y3):
    num = (x1-x2)*(x3-x2)+(y1-y2)*(y3-y2)
    deno = math.sqrt(((x1-x2)**2 + (y1-y2)**2)*((x3-x2)**2 + (y3-y2)**2))
    angle_rad = math.acos(num/deno)
    angle_deg = angle_rad*180/math.pi
    return angle_deg

x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
x6 = 0

list_of_angles = pd.DataFrame({'Frame':[0]})

def find_angle_from_npy(filename,video_num,num1,num2,num3):
    column_head = str(num1) + '_' + str(num2) + '_' + str(num3)
    data = np.load(filename + '.npy')
    for i in range(len(data[video_num])):
        x1 = (data[video_num][i][0][num1])
        y1 = (data[video_num][i][1][num1])
        x2 = (data[video_num][i][0][num2])
        y2 = (data[video_num][i][1][num2])
        x3 = (data[video_num][i][0][num3])
        y3 = (data[video_num][i][1][num3])
        list_of_angles.at[i,column_head] = (str(angle_deg(x1,y1,x2,y2,x3,y3)))
        list_of_angles.at[i,'Frame'] = int(i)
    return list_of_angles

def run(filename,video_num,nums_list):
    for i in range (len(nums_list)):
        angles_csv = find_angle_from_npy(filename, video_num, nums_list[i][0], nums_list[i][1], nums_list[i][2])
    print(angles_csv)
    angles_csv.to_csv('Video' + str(video_num) + "_" + str(filename) + '.csv')



# INPUTS ---------------------------------------------------------------

nums_list = [[1,8,9],[1,8,12],[0,1,2],
            [0,1,5],[9,8,12],[10,9,8],
            [13,12,8],[10,11,22],[13,14,19],
            [9,10,11],[12,13,14],[3,2,1],
            [6,5,1]]
file_list = ['Healthy30F','Unhealthy30F']

for j in file_list:
    data = np.load(j + '.npy')
    for i in range(len(data)):
        run(j, i, nums_list)
    
