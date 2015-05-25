#!/usr/bin/env python

import argparse
import csv
import datetime

import matplotlib.dates
import matplotlib.pyplot
import matplotlib.ticker
import numpy as np


def read_data():
    filenames = ['intel-sp.csv',
                 'intel-dp.csv',
                 'nvidia-sp.csv',
                 'nvidia-dp.csv']
    legend_names = ['Intel CPU SP',
                    'Intel CPU DP',
                    'Nvidia GPU SP',
                    'Nvidia GPU DP']
    colors = ['DeepSkyBlue', 'RoyalBlue', 'ForestGreen', 'DarkGreen']

    date_format = '%Y-%m-%d'
    data = {}
    for filename, legend_name, color in zip(filenames, legend_names, colors):
        data[legend_name] = {'names': [],
                             'flops': [],
                             'dates': [],
                             'placement_offset': [],
                             'color': color,
                             'legend': legend_name}
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data[legend_name]['names'].append(row[0])
                data[legend_name]['flops'].append(float(row[1]))
                d = datetime.datetime.strptime(row[2].strip(' "'), date_format)
                data[legend_name]['dates'].append(d)
                data[legend_name]['placement_offset'].append(float(row[4]))
    return data


def format_axes(ax, fontsize=8):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
    ax.yaxis.set_ticks_position('left')

    x_minor_locator = matplotlib.dates.MonthLocator(interval=3)
    y_major_locator = matplotlib.ticker.MultipleLocator(1000)
    y_minor_locator = matplotlib.ticker.MultipleLocator(250)

    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)

    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fontsize)


def text_with_background(ax, x, y, offset, s, color):
    label_ygap = 200
    t = ax.text(x, y + label_ygap + offset, s,
                color=color,
                fontsize=7,
                horizontalalignment='right')
    #t.set_bbox({'color': '1.0', 'alpha': 0.5})


def plot(output_filename):
    data = read_data()

    fig, ax = matplotlib.pyplot.subplots(nrows=1, ncols=1)
    format_axes(ax)
    ax.set_xlim(datetime.datetime(2000, 1, 1), datetime.datetime.today())

    label_xgap = datetime.timedelta(100)

    for name, series in data.items():
        # plot series data
        ax.plot(series['dates'], series['flops'], 'o-',
                label=name,
                color=series['color'],
                markeredgecolor=series['color'],
                linewidth=2.0)

        # label series data points with architecture names
        if name != 'Intel CPU SP':
            for x, y, aname, offset in zip(series['dates'], series['flops'], series['names'], series['placement_offset']):
                text_with_background(ax, x, y, offset, aname, series['color'])

        # label series
        ax.text(series['dates'][-1] + label_xgap, series['flops'][-1], name,
                verticalalignment='center',
                color=series['color'],
                weight='bold',
                fontsize=9)

    ax.set_xlabel('Release date', size=12)
    ax.set_ylabel('Theoretical peak (GFLOPS/s)', size=11)

    matplotlib.pyplot.savefig(output_filename, bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CPU vs GPU performance plot')
    parser.add_argument('-o', '--output',
                        help='filename for plot output',
                        default='cpu_vs_gpu.pdf')
    args = parser.parse_args()

    plot(output_filename=args.output)