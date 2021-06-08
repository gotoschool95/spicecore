import os
import numpy as np
import matplotlib as mlp
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas import Series



depth_data = open('./geo-f2k', 'r')


depth_dom_num = []
depth = []


for line in depth_data:
    if line != '\n':
        line = line.split('\t')
        # print(line)
        depth_dom_num.append(float(line[6][:-1]))
        depth.append((-1) * float(line[4]))

# print(depth_dom_num)
# print(depth)


Array2 = {'dom_num': depth_dom_num, 'depth':depth}
df_run_data = pd.DataFrame(Array2)




##########################################################################################


domlist = list(range(2,62,2))
# print(domlist)
photon = []
usingdepth = []


for i in domlist:
    num = i
    file = 'run_data' + str(num) + '.txt'
    data = open('./sim-output/' + file, 'r')






    hit = []
    string_num = []
    dom_num = []
    time = []
    wavelength = []
    theta1 = []
    pi1 = []
    theta2 = []
    pi2 = []

    for line in data:
        if line != '\n':
            line = line[:-1].split(' ')
            hit.append(line[0])
            string_num.append(float(line[1]))
            dom_num.append(float(line[2]))
            time.append(float(line[3]))
            wavelength.append(float(line[4]))
            theta1.append(float(line[5]))
            pi1.append(float(line[6]))
            theta2.append(float(line[7]))
            pi2.append(float(line[8]))


    # print(theta1)

    Array = {'hit': hit, 'string_num':string_num, 'dom_num':dom_num, 'time':time, 'wavelength':wavelength, 'theta1':theta1, 'pi1':pi1, 'theta2':theta2, 'pi2':pi2}
    run_data = pd.DataFrame(Array)


    run_data = pd.merge(run_data, df_run_data, on = 'dom_num')


    wrong_data = run_data[run_data['dom_num'] != float(num - 1)].index
    # print(len(wrong_data))

    run_data = run_data.drop(wrong_data)



    length = len(run_data)
    photon.append(length)
    usingd = run_data['depth'].tolist()
    usingd = int(usingd[0])
    usingdepth.append(usingd)
    # print(run_data)

    # plt.subplot(211)
    #
    # connect1 = list(zip(pi1,theta1))
    # connectpi1 = []
    # connecttheta1 = []
    #
    # for pi, theta in connect1:
    #     if pi < 0:
    #         connectpi1.append(pi+2*np.pi)
    #         connecttheta1.append(theta)
    #     if pi >= 0:
    #         connectpi1.append(pi)
    #         connecttheta1.append(theta)
    #
    #
    #
    #
    #
    # plt.subplot(211)
    # plt.scatter(connectpi1,connecttheta1,s=1, c = 'blue', alpha = 0.2)
    # plt.xlabel('$\Phi_1$')
    # plt.ylabel('$\Theta_1$')
    # plt.title('< String number : 1 ' + '/' + ' mDom number : ' + str(num) + ' >', fontsize = 20, pad = 15)
    # plt.axis([0, 2*np.pi, 0,np.pi])
    # plt.yticks([0, (1/6)*np.pi, (1/3)*np.pi, (1/2)*np.pi, (2/3)*np.pi, (5/6)*np.pi, np.pi], labels = ['0', '1/6' + '$\pi$', '2/6' + '$\pi$', '3/6' + '$\pi$', '4/6' + '$\pi$', '5/6' + '$\pi$', '$\pi$'])
    # plt.xticks([0,(1/3)*np.pi,(2/3)*np.pi,np.pi,(4/3)*np.pi,(5/3)*np.pi,(6/3)*np.pi], labels = ['0', '1/3' + '$\pi$', '2/3' + '$\pi$', '$\pi$' + ' ' + '&' + ' ' + '-' + '$\pi$', '-' + '2/3' + '$\pi$', '-' + '1/3' + '$\pi$', '0'])
    # plt.axhline(y=(np.pi/2), linestyle='--', color='r', linewidth=1)
    # plt.axvline(x= np.pi, linestyle='--', color='r', linewidth=1)
    # plt.text((1/12)*np.pi, (5/6)*np.pi, r'num = ' + str(length), fontdict={'size': 10, 'color': 'white'})
    # ax = plt.gca()
    # ax.set_facecolor('black')
    #
    #
    #
    #
    #
    # connect2 = list(zip(pi2,theta2))
    # connectpi2 = []
    # connecttheta2 = []
    #
    # for pi, theta in connect2:
    #     if pi < 0:
    #         connectpi2.append(pi+2*np.pi)
    #         connecttheta2.append(theta)
    #     if pi >= 0:
    #         connectpi2.append(pi)
    #         connecttheta2.append(theta)
    #
    #
    #
    # plt.subplot(212)
    # plt.scatter(connectpi2,connecttheta2,s=1, c = 'blue', alpha = 0.2)
    # plt.xlabel('$\Phi_2$')
    # plt.ylabel('$\Theta_2$')
    # plt.axis([0, 2*np.pi, 0,np.pi])
    # plt.yticks([0, (1/6)*np.pi, (1/3)*np.pi, (1/2)*np.pi, (2/3)*np.pi, (5/6)*np.pi, np.pi], labels = ['0', '1/6' + '$\pi$', '2/6' + '$\pi$', '3/6' + '$\pi$', '4/6' + '$\pi$', '5/6' + '$\pi$', '$\pi$'])
    # plt.xticks([0,(1/3)*np.pi,(2/3)*np.pi,np.pi,(4/3)*np.pi,(5/3)*np.pi,(6/3)*np.pi], labels = ['0', '1/3' + '$\pi$', '2/3' + '$\pi$', '$\pi$' + ' ' + '&' + ' ' + '-' + '$\pi$', '-' + '2/3' + '$\pi$', '-' + '1/3' + '$\pi$', '0'])
    # plt.text((1/12)*np.pi, (5/6)*np.pi, r'num = ' + str(length), fontdict={'size': 10, 'color': 'white'})
    # plt.axhline(y=(np.pi/2), linestyle='--', color='r', linewidth=1)
    # plt.axvline(x= np.pi, linestyle='--', color='r', linewidth=1)
    # plt.subplots_adjust(left=0.125,
    #                 bottom=0.1,
    #                 right=0.9,
    #                 top=0.9,
    #                 wspace=0.2,
    #                 hspace=0.35)
    #
    # ax = plt.gca()
    # ax.set_facecolor('black')
    #
    #
    # plt.savefig(file[:-4] + ".png",dpi=200, format="png")
    # plt.show()
    #


###########################################3
# print(photon)
# print(usingdepth)


sp_depth = []
sp_light = []

spicecore_data1 = open('./spicecoredepth.txt', 'r')

for line in spicecore_data1:
        line1 = line.split(' ')
        for line in line1:
            if line != '':
                sp_depth.append(float(line))

spicecore_data2 = open('./spicecorelightintensity.txt', 'r')

for line in spicecore_data2:
        line1 = line.split(' ')
        for line in line1:
            if line != '':
                sp_light.append(float(line))


photon1 = []
for line in photon:
    a = line/40
    photon1.append(a)

usingdepth1 = []
for line in usingdepth:
    a = line - 50
    usingdepth1.append(a)

#data cutting(sim)
usingdepth1 = usingdepth1[7:-5]
photon1 = photon1[7:-5]

#data cutting(sim)


# plt.style.use('dark_background')

plt.figure(figsize=(18.48,9.74), dpi=100)
plt.subplot()
plt.scatter(sp_depth,sp_light, label =  'Spicecore data', s=200) #color = '#81B1D2'
plt.scatter(usingdepth1, photon1, label = 'Simulation data', s=400, c='#ff7f0e') #color = '#FA8174'
plt.errorbar(usingdepth1, photon1, xerr=[30.0 for x in usingdepth1], c='#ff7f0e',elinewidth=5,capsize=5, capthick=3)
plt.title("Simulation data vs Spicecore data", fontsize=50, pad= 30)
plt.yscale('log')
plt.xlabel('Depth [m]', fontsize = 40)
plt.ylabel('Light Intensity [a.u.]', fontsize = 40)
plt.legend(loc='upper right', fontsize=25)
plt.xticks(fontsize=33)
plt.yticks(fontsize=33)
plt.xlim([1250,1700])
plt.ylim([10,200])
plt.text(1360, 100, "IceCube Preliminary",fontsize = 30,color= 'r' )



plt.savefig('SimulationdatavsSPICEcoredata.png', transparent=True)
plt.show()
