#!/usr/bin/env python3
# vim: set ai et ts=4 sw=4: 

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv



def draw(data_values):
    data_names = ['Пропуск','Оплачиваемый пропуск','Явка']
    data_names[0] = data_names[0] + ': '+ str(data_values[0])
    data_names[1] = data_names[1] + ': '+ str(data_values[1])
    data_names[2] = data_names[2] + ': '+ str(data_values[2])


    dpi = 100
    fig = plt.figure(dpi = dpi, figsize = (1280 / dpi, 720 / dpi) )
    mpl.rcParams.update({'font.size': 10})

    plt.title('Статистика ваших посещений')

    plt.pie( 
        data_values, autopct='%.1f', radius = 1.1,
        explode = [0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor = (-0.6, 0.50, 0.25, 0.25),
        loc = 'lower left', labels = data_names)
    fig.savefig('pie.png')

data_values = [45,1,48]
draw(data_values)