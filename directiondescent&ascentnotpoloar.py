import argparse
import os
import numpy as np
import pandas as pd
import matplotlib as mlp
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import math
plt.style.use('seaborn-whitegrid')
import matplotlib.ticker as ticker

# plt.style.use('dark_background')


def getlines1(data):
    leng=4453
    lines = []
    for i in range(leng):
        line= gyrodata.readline()
        lines.append(line)
    return lines

def getlines2(data):
    leng=389
    lines = []
    for i in range(leng):
        line= picdata.readline()
        lines.append(line)
    return lines

def getdate(line):
    date = line[:17].replace('_','')
    return date


def removedate(lines):
    newlines=[]
    for line in lines:
        line = line[18:]
        newlines.append(line)

    return newlines


def findvalue(index, data):
    i = 0
    datas=[]
    lines=getlines1(data)
    for line in lines:
        # print('%d/%d is done' %(i, len(lines)))
        line = line[18:].split(';')
        values=[]
        for key in index:
            for element in line:
                if key in element:
                    value = int(element.split('   ')[-1])
                    values.append(value)
        datas.append(values)
        i += 1
    return datas



def findunderbar(comp):
    finded="error"
    for jj in range(0,len(comp)):
        if comp[jj] == "_":
            finded=jj
            break
        else:
            continue
    return finded




def ExtractImage(img_filepath):
    '''
    Load an image data file in RAW format and save the image data in a numpy ndarray.
    '''
    H_size = 1312    # horizontal frame size in number of pixels, always 1312
    V_size = 979     # vertical frame size in number of pixels, always 979
    ### Extract image data from .RAW file ###
    npy = np.fromfile(img_filepath, dtype=np.uint16, count=H_size*V_size) # Read RAW data file and save the data in an 1D-array of 16-bit numbers.
    # npy = npy - 3680
    npy = np.reshape(npy, (V_size, H_size), 'C') # Convert the 1D-array to a 2D-array. This is the photo captured by the camera. Note that the second argument value should be (V_size, H_size).
    #npy = npy.reshape(2,V_size//2, 2, H_size//2)
    #npy = npy.reshape(2,V_size//2, 2, H_size//2).mean(-1).mean(1)
    img = npy >> 4 # The elements of the array are 16-bit unsigned integer numbers. In binary format, the leading 12=bit numbers are the pixel value. The last 4-bit numbers are 0000. These four zeros are not actual data. In order to get the actual pixel values, the elements should be shifted to right by 4 bits.

    return img


# pd.set_option('display.max_row', 500)







LEDon = "/home/danim/project/ledon"



# getting gyrodataframe
gyrodata = open('../slow_control/gyro_20191220_22_17_08.txt', 'r')
index = ['Accelerometer X','Accelerometer Y','Accelerometer Z','NORTH','Mag-X','Mag-Y','Mag-Z','Gyroscope X','Gyroscope Y','Gyroscope Z','Inclinometer X','Inclinometer Y','Inclinometer Z','Orientation-X','Orientation-Y','Orientation-Z','Orientation-W']
gyrotime = []
for line in getlines1(gyrodata):
    date1 = getdate(line)
    gyrotime.append(date1)

#no redun
gyrotime = set(gyrotime)
gyrotime = list(gyrotime)
# print(gyrotime)


gyrodata = open('../slow_control/gyro_20191220_22_17_08.txt', 'r')
df = findvalue(index, gyrodata)
gyrodataframe = pd.DataFrame(data=df, columns = index)
gyrodataframe = gyrodataframe[['Accelerometer X','Accelerometer Y','Accelerometer Z','NORTH','Mag-X','Mag-Y','Mag-Z','Gyroscope X','Gyroscope Y','Gyroscope Z','Inclinometer X','Inclinometer Y','Inclinometer Z','Orientation-X','Orientation-Y','Orientation-Z','Orientation-W']]
gyrodataframe.insert(0,'gyrotime',gyrotime)
# print('gyrodataframe',gyrodataframe)








# getting picdataframe
picdata = open('../slow_control/pic_20191220_22_17_08.txt', 'r')
pictime = []
for line in getlines2(picdata):
    date2 = getdate(line)
    pictime.append(date2)

#no redun
pictime = set(pictime)
pictime = list(pictime)


picdata = open('../slow_control/pic_20191220_22_17_08.txt', 'r')
folder_name = []
foldertime = []
filenumber = []
lines = picdata.readlines()
for line in lines:
    item = line.split("/")
    name = item[item.index("SKKU_Camera_code")+1]
    folder_name.append(name)

    time = item[0]
    time = time[:-3]
    time = time.replace('_','')
    item1 = line.split("1576")
    name2 = item1[1:-1]
    for num in name2:
        num1 = list(num)
        num2 = num1[:6]
        num2 = "".join(num2)
        num2 = "1576"+num2
        foldertime.append(time)
        filenumber.append(num2)
        # print(num2)

# print(folder_name)
# print(len(foldertime))
# print(len(filenumber))

foldertime = [ int(i) for i in foldertime]
filenumber = [ int(i) for i in filenumber]
# pd.set_option('display.max_row', 1200)
ndArrays111 = {'pictime': foldertime, 'file_name':filenumber}
step1 = pd.DataFrame(ndArrays111)

# print('step1', step1)



# mix date
pictime = [ int(i) for i in pictime]
pictime = sorted(pictime)
pictime = [ str(i) for i in pictime]
# print(pictime)
b = gyrodataframe['gyrotime'].values.tolist()
gyrotime.remove('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# print(gyrotime)
gyrotime = [ int(i) for i in gyrotime]
gyrotime = sorted(gyrotime)
gyrotime = [ str(i) for i in gyrotime]
# print(gyrotime)

# print(len(b))
mix = pictime + gyrotime
mixdate = [ int(i) for i in mix]
mixdate = sorted(mixdate)
mixdate = [ str(i) for i in mixdate]

# print(mixdate)





indexes1 = []
indexes2 = []
for picdate in pictime:
    index1 = mixdate.index(picdate)
    # print(index1)
    indexes1.append(index1)

for gyrodate in gyrotime:
    index2 = mixdate.index(gyrodate)
    # print(index)
    indexes2.append(index2)

indexes1 = sorted(indexes1)
indexes2 = sorted(indexes2)
# print(len(pictime))
# print(indexes1)
# print(indexes2)
# print(len(mixdate))
neededindex = []
for index1 in indexes1:
    bin = []
    for index2 in indexes2:
        if index2 > index1:
            bin.append(index2)
    index = min(bin)
    neededindex.append(index)

# print(neededindex)


indexgyrotime = []
for index in neededindex:
        date = mixdate[index]
        indexgyrotime.append(date)


# pd.set_option('display.max_row', 500)
pictime = [ int(i) for i in pictime]
pictime = sorted(pictime)




ndArrays3 = {'pictime': pictime, 'gyrotime':indexgyrotime}
merge1 = pd.DataFrame(ndArrays3)


# print('merge1', merge1)




gyrodataframe.dropna()

gyrodataframeorix = gyrodataframe['Inclinometer X'].tolist()
gyrodataframeoriy = gyrodataframe['Inclinometer Y'].tolist()
gyrodataframeoriz = gyrodataframe['Inclinometer Z'].tolist()
#
gyrodataframeorix = gyrodataframeorix[:-1]
gyrodataframeoriy = gyrodataframeoriy[:-1]
gyrodataframeoriz = gyrodataframeoriz[:-1]
# print(gyrodataframeorix)


ndArrays4 = {'gyrotime': gyrotime, 'Inclinometer X':gyrodataframeorix, 'Inclinometer Y':gyrodataframeoriy, 'Inclinometer Z':gyrodataframeoriz}
merge2 = pd.DataFrame(ndArrays4)
# print('merge2', merge2)







step2 = pd.merge(merge1,merge2, on = 'gyrotime')
# print('step2', step2)





# pd.set_option('display.max_row', 1200)
filenameangle = pd.merge(step2 ,step1, on = 'pictime')
# del filenameangle['Orientation-X']
# del filenameangle['Orientation-Y']
# del filenameangle['Orientation-Z']
print('filenameangle', filenameangle)

##########################################################################


indir1 = "/home/danim/project/ledon"

indir2 = "/home/danim/project/slow_control/depth1576895991.18422.log"

depth1576895991=[]
depth1576895991name=[]
depth1576895991depth=[]
f = open(indir2, 'r')
lines = f.readlines()
for line in lines:
    depth1576895991.append(line)
    depth1576895991name.append(line[:10])
    nospaceline = line.split(' ')
    nospaceline = nospaceline[1:]
    nospaceline = '\n'.join(nospaceline)
    depth1576895991depth.append(nospaceline[:-1])

f.close()

indir3 = "/home/danim/project/slow_control/depth1576903412.99612.log"

depth1576903412=[]
depth1576903412name=[]
depth1576903412depth=[]
f = open(indir3, 'r')
lines = f.readlines()
for line in lines:
    depth1576903412.append(line)
    depth1576903412name.append(line[:10])
    nospaceline = line.split(' ')
    nospaceline = nospaceline[1:]
    nospaceline = '\n'.join(nospaceline)
    depth1576903412depth.append(nospaceline[:-1])

f.close()

indir4 = "/home/danim/project/slow_control/depth1576906949.923334.log"

depth1576906949=[]
depth1576906949name=[]
depth1576906949depth=[]
f = open(indir4, 'r')
lines = f.readlines()
for line in lines:
    depth1576906949.append(line)
    depth1576906949name.append(line[:10])
    nospaceline = line.split(' ')
    nospaceline = nospaceline[1:]
    nospaceline = '\n'.join(nospaceline)
    depth1576906949depth.append(nospaceline[:-1])

f.close()

names = depth1576895991name + depth1576903412name + depth1576906949name
depths = depth1576895991depth + depth1576903412depth + depth1576906949depth

names = [int(i) for i in names]

ndArrays1 = {'file_name': names, 'depth': depths}
namedepth = pd.DataFrame(ndArrays1)
namedepth = namedepth.drop_duplicates('file_name', keep='first')
namedepth = namedepth[namedepth.depth != '']
namedepth = namedepth[namedepth.depth != '\x00\x00']
namedepth = namedepth[namedepth.depth != '\x00']
namedepth = namedepth.reset_index()
# print('namedepth',namedepth)




# pd.set_option('display.max_row', 500)





# pd.set_option('display.max_row', 1200)

final = pd.merge(filenameangle, namedepth, on = 'file_name')
# print('final',final)





ori = final['Inclinometer Z'].tolist()
depth = final['depth'].tolist()
depth = [float(i) for i in depth]



a = list(zip(ori,depth))

b = []
for i,j in a:
    if i > 250:
        if j > 750:
            i = i - 360
            b.append([i,j])
        else:
            b.append([i,j])

    else:
        b.append([i,j])



# print(b[0])
b = np.array(b)
b= b.T
print(len(b))

ori = b[0]
depth = b[1]



ori_down = ori[:622]
ori_up = ori[622:]

# print('ori_down', ori_down)
# print('ori_up', ori_up)

depth_down = depth[:622]
depth_up = depth[622:]

# print('depth_down', depth_down)
# print('depth_up', depth_up)

# plt.style.use(['dark_background'])
plt.figure(figsize=(18.48,9.74), dpi=100)
# plt.figure()
plt.scatter(depth_down,ori_down, color='r', linewidth=4, label = 'Descent')
plt.scatter(depth_up,ori_up, color='b', linewidth=4, label = 'Ascent')
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)
plt.xlabel('Depth [m]', fontsize=40)
plt.ylabel('Orientation [deg]', fontsize=40)
plt.title("Depth  vs  Orientation", fontsize=50,pad=30)
plt.legend(fontsize = 25,frameon=True)
plt.text(0, -100, "IceCube Preliminary",fontsize = 30,color= 'r' )

plt.savefig('CameraOrientation(notpolar).png', transparent=True)
plt.show()
