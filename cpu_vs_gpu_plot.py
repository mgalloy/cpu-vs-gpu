

def makePlot():
    import pylab as pl
    import csv    
    
    fileNames = ['intel-sp.csv', 'intel-dp.csv', 'nvidia-sp.csv', 'nvidia-dp.csv']
    legendNames = ['Intel CPU SP', 'Intel CPU DP', 'Nvidia GPU SP', 'Nvidia GPU DP']      
    
    colors = ['DeepSkyBlue', 'RoyalBlue', 'ForestGreen', 'DarkGreen']
    # load data
    data = {}
    for i in range(len(fileNames)):
        data[legendNames[i]] = {'names':[], 'flops':[], 'dates':[], 
                                'color':colors[i], 'legend':legendNames[i]}
        f = open(fileNames[i])
        csvReader = csv.reader(f)
        for row in csvReader:
            data[legendNames[i]]['names'].append(row[0])
            data[legendNames[i]]['flops'].append(float(row[1]))
            data[legendNames[i]]['dates'].append(row[2].strip(' "'))
                
    # plot data
    dataTicks = ["%s"%v for v in range(2000,2015,2)]
    dataTicksValues = pl.datestr2num(["%s-01-01"%v for v in range(2000,2015,2)])

    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9) 
    textSize = 10
    
    fig = pl.figure()
    #pl.subplot(121)
    for d in data.values():
        x = pl.datestr2num(d['dates'])
        y = d['flops']
        c = d['color']
        pl.plot(x, y, 'o-', color=c, label=d['legend'], lw=2)
        if d['legend'] is not 'Intel CPU SP':
            for n in range(len(d['names'])):
                pl.text(x[n]-50, y[n]+50, d['names'][n], 
                        ha="right", va="top", size=textSize, color=c)#, bbox=bbox_props)
        pl.text(x[-1]+150, y[-1], d['legend'], 
                ha="left", va="center", size=textSize+2, color=c,bbox=bbox_props)

    #pl.legend(loc='upper left')
    pl.xlabel('Release date', fontsize=textSize+4)
    pl.ylabel('Theoretical peak (GFLOP/s)', fontsize=textSize+4)
    pl.xlim((pl.datestr2num('2000-01-01'), pl.datestr2num('2014-01-01')))
    pl.xticks(dataTicksValues, dataTicks, fontsize=textSize)
    pl.yticks(fontsize=textSize)
    pl.ylim((0, 5500))
    #fig.subplots_adjust(right=1.8)
    #pl.gca().set_yscale('log')
    pl.show()
    
    fig.savefig('cpu_vs_gpu.png', bbox_inches='tight')
    fig.savefig('cpu_vs_gpu.pdf', bbox_inches='tight')

if __name__ == "__main__":
    makePlot()