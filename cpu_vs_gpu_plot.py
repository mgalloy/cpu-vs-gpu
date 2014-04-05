import pylab as pl

def plotTextWithWhiteOutline(x, y, text, textSize, color, offset, ha):
    
    xx = x+offset[0]
    yy = y+offset[1]
    
    # Plot white border around text
    c = 'LemonChiffon'
    w = 'bold'
    outline = 3
    pl.text(xx-outline, yy, text, ha=ha, va="top", size=textSize, color=c, weight=w)
    pl.text(xx+outline, yy, text, ha=ha, va="top", size=textSize, color=c, weight=w)
    pl.text(xx, yy+outline, text, ha=ha, va="top", size=textSize, color=c, weight=w)
    pl.text(xx, yy-outline, text, ha=ha, va="top", size=textSize, color=c, weight=w)
    pl.text(xx-outline, yy-outline, text, ha=ha, va="top", size=textSize, color=c, weight=w)
    pl.text(xx+outline, yy+outline, text, ha=ha, va="top", size=textSize, color=c, weight=w)
    pl.text(xx-outline, yy+outline, text, ha=ha, va="top", size=textSize, color=c, weight=w)
    pl.text(xx+outline, yy-outline, text, ha=ha, va="top", size=textSize, color=c, weight=w)
  
    pl.text(xx, yy, text, ha=ha, va="top", size=textSize, color=color, weight=w)

def makePlot(): 
    
    import csv
    
    xlimMax = 2014
    xlimMaxDate = '%s-01-01'%xlimMax
    ylimMax = 5500 # GFLOP/s
    textSize = 10
    
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
    dataTicks = ["%s"%v for v in range(2000,xlimMax+1,2)]
    dataTicksValues = pl.datestr2num(["%s-01-01"%v for v in range(2000,xlimMax+1,2)])

    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9) 
    
    fig = pl.figure()
    for d in data.values():
        x = pl.datestr2num(d['dates'])
        y = d['flops']
        c = d['color']
        pl.plot(x, y, 'o-', color=c, label=d['legend'], lw=2)
        i = 0
        for n in range(len(d['names'])):
            i += 1
            if i < 3: 
                continue
            if d['legend'] is 'Intel CPU SP' and i%2==0:
                continue
            if d['legend'] is 'Intel CPU DP' and i%2==1:
                continue
            offset = (-100, 50)
            ha = 'right'
            plotTextWithWhiteOutline(x[n], y[n], d['names'][n], textSize, c, offset, ha)

        pl.text(x[-1]+150, y[-1], d['legend'], ha="left", va="center", size=textSize+2, color=c, bbox=bbox_props, weight='bold')

    pl.xlabel('Release date', fontsize=textSize+4)
    pl.ylabel('Theoretical peak (GFLOP/s)', fontsize=textSize+4)
    pl.xlim((pl.datestr2num('2000-01-01'), pl.datestr2num(xlimMaxDate)))
    pl.xticks(dataTicksValues, dataTicks, fontsize=textSize)
    pl.yticks(fontsize=textSize)
    pl.ylim((0, ylimMax))
    #pl.gca().set_aspect(1.5)
    pl.show()
    
    fig.savefig('cpu_vs_gpu.png', bbox_inches='tight')
    fig.savefig('cpu_vs_gpu.pdf', bbox_inches='tight')

if __name__ == "__main__":
    makePlot()