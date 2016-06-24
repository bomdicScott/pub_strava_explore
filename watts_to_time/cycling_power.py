from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from random import randint
import csv
import numpy as np
import json
import math

CrEff = 0.00330
CwA = 0.3397
temperature_c = 25
altitude_m = 0


def get_power_watts(pSpeedKmph, pWindSpeedKmph, pWeight, pBikeWeight, pGeoGradePtc):
    pSpeedKmph = float(pSpeedKmph)
    pWindSpeedKmph = float(pWindSpeedKmph)
    pWeight = float(pWeight)
    pBikeWeight = float(pBikeWeight)
    pGeoGradePtc = float(pGeoGradePtc)
    slope = math.atan(pGeoGradePtc*0.01)
    CrDyn = 0.1 * math.cos(slope)
    Frg = (
         9.81 * (pBikeWeight + pWeight) * 
         (
          CrEff * math.cos(slope) + math.sin(slope)
         )
        )
    Ka = (
        176.5 * 
        math.exp(-altitude_m * .0001253) * 
        CwA / (273.0 + temperature_c)
       )
    total_speed_kmph = pSpeedKmph + pWindSpeedKmph
    power = (
             1.025 * 
             (pSpeedKmph * 0.27778) *
             (
              Ka * (total_speed_kmph * 0.27778)**2
              + Frg 
              + (pSpeedKmph * 0.27778) * CrDyn
             )
            )
    return power

# calculate speed from power, weight, bike_weight and grade
def get_speed_mps(pPower, pWeight, pBikeWeight, pGeoGradePtc):
    wind_kmph = 0
    pPower = float(pPower)
    pWeight = float(pWeight)
    pBikeWeight = float(pBikeWeight)
    pGeoGradePtc = float(pGeoGradePtc)
    slope = math.atan(pGeoGradePtc*0.01)
    CrDyn = 0.1 * math.cos(slope)
    Frg = (
           9.81 * (pBikeWeight + pWeight) * 
           (
            CrEff * math.cos(slope) + math.sin(slope)
           )
          )
    Ka = (
          176.5 * 
          math.exp(-altitude_m * .0001253) * 
          CwA / (273.0 + temperature_c)
         )
    # print("slope:{}, Frg:{}, Ka:{}".format(slope, Frg, Ka))
    cardB = (
             (3.0*Frg - 4.0*wind_kmph*CrDyn) / (9.0*Ka) 
             -
             math.pow(CrDyn, 2.0) / (9.0*math.pow(Ka, 2.0)) 
             -
             (wind_kmph*wind_kmph)/9.0
            )
    cardA = (
             -1.0 *
             (
              (math.pow(CrDyn, 3.0) - math.pow(wind_kmph, 3.0)) / 27.0
              + 
              wind_kmph * 
              (5.0*wind_kmph*CrDyn + 4.0*math.pow(CrDyn, 2.0) / Ka - 6.0*Frg) / 
              (18.0 * Ka)
              - 
              pPower / (2.0*Ka*1.03)
              - 
              CrDyn*Frg / (6.0*math.pow(Ka, 2.0))
             )
            )
    # cardB = 52.6070947916983
    # cardA = 405.132421124689

    # print("cardB:{}, cardA:{}".format(cardB, cardA))
    sqrt = math.pow(cardA, 2.0) + math.pow(cardB, 3.0)
    #print("sqrt:{}".format(sqrt))
    # print("sqrt:{}, ire:{}".format(sqrt, ire))
    Vms = -1;
    if (sqrt >= 0):
        ire = cardA-math.sqrt(sqrt)
        if ire < 0:
            Vms = (
                   math.pow(cardA+math.sqrt(sqrt),1.0/3.0) - math.pow(-ire,1.0/3.0)
                  )
        else:
            Vms = (
                   math.pow(cardA+math.sqrt(sqrt),1.0/3.0) + math.pow(ire,1.0/3.0)
                  )        
    else:
        Vms = (
               2.0*math.sqrt(-cardB) * 
               math.cos(
                        math.acos(
                                  cardA/math.sqrt(math.pow(-cardB,3.0))
                                 )/3.0
                       )
              )
    # print("Vms1:{}".format(Vms))
    Vms -= 2.0*wind_kmph/3.0 + CrDyn/(3.0*Ka)
    # print("Vms2:{}".format(Vms))
    return Vms

if __name__ == "__main__":
    speed_kmph = 20
    wind_speed_kmph = 0
    weight_kg = 75
    bike_weight_kg = 10
    geo_grade_ptc = 6
    watts = get_power_watts(speed_kmph, wind_speed_kmph, weight_kg, bike_weight_kg, geo_grade_ptc)

    print("watts:{}".format(watts))

    speed_list = np.arange(5, 50, 1)
    incline_list = np.arange(-4, 15, 1)

    power_table = np.zeros((len(speed_list), len(incline_list)))

    for s in range(len(speed_list)):
        for i in range(len(incline_list)):
            speed_kmph = speed_list[s]
            geo_grade_ptc = incline_list[i]
            power_table[s,i] = get_power_watts(speed_kmph, wind_speed_kmph, weight_kg, bike_weight_kg, geo_grade_ptc)

    '''
    s = get_speed_kmph(200, weight_kg, bike_weight_kg, 6)
    print("s:{}".format(s))
    '''

    # plot
    f_idx = 0
    #print(power_table)
    S, I = np.meshgrid(speed_list, incline_list)
    #print(speed_list)
    #print(incline_list)
    #print(S)
    #print(I)
    #print(S.shape)
    P = np.transpose(power_table)
    #print(P)
    fig = plt.figure(f_idx)
    f_idx += 1
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(S, I, P, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    #surf = ax.plot_wireframe(S, I, P)
    ax.set_xlabel('speed(kmph)')
    #ax.set_xlim(-40, 40)
    ax.set_ylabel('incline(%)')
    #ax.set_ylim(-40, 40)
    ax.set_zlabel('power(W)')
    #ax.set_zlim(-100, 100)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)


    fig = plt.figure(f_idx)
    f_idx += 1
    ax = fig.add_subplot(111)

    power_list_plot = np.arange(100, 400, 50)

    for p in range(len(power_list_plot)):
        print("power_list_plot[p]:{}".format(power_list_plot[p]))
        incline_list_plot = incline_list
        speed_list_plot = np.zeros_like(incline_list_plot)
        for i in range(len(incline_list_plot)):
            speed_list_plot[i] = get_speed_kmph(power_list_plot[p], weight_kg, bike_weight_kg, incline_list_plot[i])
        ax.plot(speed_list_plot, incline_list_plot, label="power = " + str(power_list_plot[p]) + "W")

    ax.set_xlabel('speed(kmph)')
    ax.set_ylabel('incline(%)')
    ax.legend(loc='upper right')



    plt.show()






