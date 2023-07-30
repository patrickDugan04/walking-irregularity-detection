import math
import pandas as pd
import numpy as np

def angle_deg(x1,y1,x2,y2,x3,y3):
    # (x1,y1) - one end
    # (x2,y2) - pivot
    # (x3,y3) - other end 
    num = (x1-x2)*(x3-x2)+(y1-y2)*(y3-y2)
    deno = math.sqrt(((x1-x2)**2 + (y1-y2)**2)*((x3-x2)**2 + (y3-y2)**2))
    angle_rad = math.acos(num/deno)
    angle_deg = angle_rad*180/math.pi
    return angle_deg

#def angle_deg(angle_rad):
#    angle_deg = 
#    return angle_deg

x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
x6 = 0

list_of_angles = pd.DataFrame({'Frame':[0],'Data':[0]})

def find_angle_from_npy(filename,video_num,num1,num2,num3):
    data = np.load(filename + '.npy')
    for i in range(len(data[video_num])):
        x1 = (data[video_num][i][0][num1])
        y1 = (data[video_num][i][1][num1])
        x2 = (data[video_num][i][0][num2])
        y2 = (data[video_num][i][1][num2])
        x3 = (data[video_num][i][0][num3])
        y3 = (data[video_num][i][1][num3])
        list_of_angles.loc[i] = (str(angle_deg(x1,y1,x2,y2,x3,y3)))
        list_of_angles.at[i,'Frame'] = int(i)
    print(list_of_angles)
    return list_of_angles

import matplotlib.pyplot as plt

def anglegraph(filename,video_num,pt1,pt2,pt3):
    df = find_angle_from_npy(filename,video_num,pt1,pt2,pt3)
    print(df)
    print(df.loc[:,'Frame'], df.loc[:,'Data'])
    df.to_csv('output/' + str(filename) + '_angle' + '.csv', sep=',')
    new = pd.read_csv('output/' + str(filename) + '_angle' + '.csv')
    scatter_plot = plt.figure()
    axes1 = scatter_plot.add_subplot(1,1,1)
    axes1.scatter(x=new.loc[:,'Frame'], y=new.loc[:,'Data'])
    axes1.set_title('Scatterplot')
    axes1.set_xlabel('Frame')
    axes1.set_ylabel('Data')
    plt.savefig('output/' + str(filename) + ".jpg")
    plt.show()
    
