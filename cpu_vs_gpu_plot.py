

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

    #bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        
    pl.figure()
    for d in data.values():
        x = pl.datestr2num(d['dates'])
        y = d['flops']
        c = d['color']
        pl.plot(x, y, 'o-', color=c, label=d['legend'], lw=2)
        for n in range(len(d['names'])):
            pl.text(x[n]-50, y[n]+50, d['names'][n], 
                    ha="right", va="top", size=10, color=c)#, bbox=bbox_props)

    pl.legend(loc='upper left')
    pl.xlabel('Release date')
    pl.ylabel('Theoretical peak (GFLOP/s)')
    pl.xlim((pl.datestr2num('2000-01-01'), pl.datestr2num('2014-01-01')))
    pl.xticks(dataTicksValues, dataTicks)
    pl.ylim((0, 5000))
    #pl.gca().set_yscale('log')
    pl.show()


if __name__ == "__main__":
    makePlot()