import argparse
import os
import numpy as np
import pandas as pd
import matplotlib as mlp
import pickle
# import matplotlib.patches.ConnectionPatch as ConnectionPatch
import matplotlib.patches as patches
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import math
plt.style.use('seaborn-whitegrid')
import matplotlib.ticker as ticker


indir1 = "/home/danim/project/ledon"

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



ndArrays1 = {'name': names, 'depth': depths}
namedepth = pd.DataFrame(ndArrays1)
namedepth = namedepth.drop_duplicates('name', keep='first')
namedepth = namedepth[namedepth.depth != '']
namedepth = namedepth[namedepth.depth != '\x00\x00']
namedepth = namedepth[namedepth.depth != '\x00']
namedepth = namedepth.reset_index()
# print('namedepth',namedepth)




# pd.set_option('display.max_row', 500)






#subtract pedestal value 240
pedestal = [325] * (979*1312)
pedestal = np.reshape(pedestal, (979,1312), 'C')
# print(pedestal)



outdir = "./"#args.outdir
infilename = []
lightvalue = []

for ifolder in os.listdir(indir1):
    if ".py" in ifolder:

            continue

    if ".png" in ifolder:

            continue

    for infile in os.listdir(indir1 + "/" + ifolder):

        if ".RAW" in infile:

            filename = indir1 + "/" + ifolder + "/" + infile

            # print(filename)
            depth = ifolder[4:-1]
            image = ExtractImage(filename)     # Extract image data from the RAW file
            image = image - pedestal

            # image = image*npyinit
            light = np.sum(image/(1312*979))
            lightvalue.append(light)
            # print(light)
            infile_name = infile[:10]
            # print(infile_name)
            infilename.append(infile_name)
            # print(filename)
            # print(image)




ndArrays2 = {'name': infilename, 'brightness': lightvalue}
namebrightness = pd.DataFrame(ndArrays2)
# print('namebrightness',namebrightness)



namebrightnessdepth = pd.merge(namebrightness, namedepth, how='inner', on=None)
# print(namebrightnessdepth)
#
# #
#

x = namebrightnessdepth['depth'].tolist()
x = list(map(float, x))
x = [round(i) for i in x] # IceCube geometry
x = [i-10 for i in x] # ice tilt
y = namebrightnessdepth['brightness'].tolist()
# print(len(x))
# print(len(y))

# split = 1000
# ys1 = y[:split]
# ys2 = y[split:]
#
# ys2 = [ i -30 for i in ys2]
# y = ys1 + ys2


yy = []
for line in y:
    a = line/4
    a = a * 1.8
    yy.append(a)







data = open('./up2_405nm.txt', 'r')
x1=[]
y1=[]
for dat in data:
    x1.append(float(dat.split()[1]))
    y1.append(float(dat.split()[5]))

# print(x1)
# print(y1)
x2 = []
for line in x1:
    a = round(line)
    x2.append(a)




ndArrays1 = {'depth': x, 'value1': yy}
forcorrelation1 = pd.DataFrame(ndArrays1)
forcorrelation1 = forcorrelation1.groupby(by =["depth"], as_index=False).mean()
# print("forcorrelation1", forcorrelation1)



#Dust logger
ndArrays2 = {'depth': x2, 'value2': y1}
forcorrelation2 = pd.DataFrame(ndArrays2)
forcorrelation2 = forcorrelation2.groupby(by =["depth"], as_index=False).mean()




correl = pd.merge(forcorrelation1,forcorrelation2, on = 'depth')

# print(correl)

depth = correl["depth"].tolist()
cor_x_sp = correl["value1"].tolist()
cor_y_dl = correl["value2"].tolist()

iris = zip(cor_x_sp, cor_y_dl)

relation = []

for a,b in iris:
    abc = a/b
    relation.append(abc)

# print(relation)

ndArrays3 = {'depth': depth, 'value1': relation}
using = pd.DataFrame(ndArrays3)

print(using)


# y2 = []
# for line in y:
#     a = line/(120000)
#     y2.append(a)
# ####################################################################
# filePath = './spicecoredepth.txt'
# x = [str(i) for i in x]
# with open(filePath, "a") as file:
#     for i in x:
#         file.writelines(i)
#         file.writelines(' ')
#
#
# filePath = './spicecorelightintensity.txt'
# yy = [str(i) for i in yy]
# with open(filePath, "a") as file:
#     for i in yy:
#         file.writelines(i)
#         file.writelines(' ')

###################################################################

# plt.style.use('dark_background')

# print(x)
# print(y)
SMALL_SIZE = 5
MEDIUM_SIZE = 10
BIGGER_SIZE = 20

#
plt.rc('font', size=SMALL_SIZE) # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE) # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE) # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE) # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE) # fontsize of the tick labels
# print(y1)



#plt.figure()

# plt.scatter(x1,y1,c = 'blue',label = "dust logger data")
# plt.scatter(x,yy, c = 'red', label = "camera data")
# # plt.scatter(x,y2, label = "a.u.2 (a.u.1 / 30)")
# # plt.xticks(range(1000,1750,250))/home/danim/project/depthvslightvalue/foricrc.py
# # plt.ylim([1e-5,1.5])
# plt.legend(loc='upper right', fontsize=40)
#
# # [i.set_color("white") for i in plt.gca().get_xticklabels()]
# # [i.set_color("white") for i in plt.gca().get_yticklabels()]
# plt.xlabel('Depth [m]')
# plt.ylabel('Light intensity [a.u.]')
# plt.yscale('log')
# # plt.title("Brightness vs Depth")



fig = plt.figure(figsize=(18.48,9.74), dpi=100)



topRight = fig.add_subplot(4,2,(1,4))
# topRight.set_xlabel('Depth [m]' , fontsize = 45)
topRight.set_ylabel('Light intensity [a.u.]' , fontsize = 40)
# topRight.set_xlabel('Depth [m]' , fontsize = 40)
plt.yscale('log')
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)
topRight.set_title('Camera data vs Dust logger data (under 1200m)', fontsize=50, pad=30)
topRight.set_xlim([1200,1600])
topRight.set_ylim([5,300])
topRight.scatter(x1 , y1 ,
             color = 'blue',  alpha=1 ,
             label = "dust logger data")

topRight.scatter(x, yy,
             s=70, color = 'red' , alpha=1,
             label = "camera data")
topRight.legend(fontsize=20, frameon=True)
topRight.text(1220, 6, "IceCube Preliminary",fontsize = 30,color= 'r' )

plt.subplots_adjust(left=0.125, bottom=0.1,  right=0.9, top=0.9, wspace=0.2, hspace=0.5)


bottom2 = fig.add_subplot(4,2,(5,8))
# bottom2.set_title('Camera data / Dust logger data (under 1200m)', fontsize=30, pad=15)
bottom2.set_xlabel('Depth [m]' , fontsize = 40)
bottom2.set_ylabel('Ratio [a.u.]' , fontsize = 40)
bottom2.axhline(y=1, color='r', linewidth=3, label = "y = 1")
bottom2.text(1400,1.05,'Ratio = 1',color = 'r', fontsize = 20)
bottom2.set_xlim([1200,1600])

plt.xticks(fontsize=35)
plt.yticks(fontsize=35)
# plt.yscale('log')
bottom2.scatter(depth , relation  , alpha=1 , label = "camera data / dust logger data", color = 'black',s=100)
# bottom.legend(fontsize=45)

plt.savefig('CameradatavsDustLoggerdata.png', transparent=True)
plt.show()
