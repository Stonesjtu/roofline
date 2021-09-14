#General imports:

import sys
import os
import math
from matplotlib import rc
rc('text', usetex=True) # this is if you want to use latex to print text. If you do you can create strings that go on labels or titles like this for example (with an r in front): r"$n=$ " + str(int(n))
from numpy import *
from pylab import *
import random
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib.lines as lns
from scipy import stats
from matplotlib.patches import Polygon
import matplotlib.font_manager as fm

font = fm.FontProperties(
        family = 'Gill Sans', fname = 'GillSans.ttc')


background_color =(0.85,0.85,0.85) #'#C0C0C0'
grid_color = 'white' #FAFAF7'
matplotlib.rc('axes', facecolor = background_color)
matplotlib.rc('axes', edgecolor = grid_color)
matplotlib.rc('axes', linewidth = 1.2)
matplotlib.rc('axes', grid = True )
matplotlib.rc('axes', axisbelow = True)
matplotlib.rc('grid',color = grid_color)
matplotlib.rc('grid',linestyle='-' )
matplotlib.rc('grid',linewidth=0.7 )
matplotlib.rc('xtick.major',size =0 )
matplotlib.rc('xtick.minor',size =0 )
matplotlib.rc('ytick.major',size =0 )
matplotlib.rc('ytick.minor',size =0 )
#matplotlib.rc('font', family='serif')

def addPerfLine(peakPerf, label):
    #Peak performance line and text
    ax.axhline(y=peakPerf, linewidth=0.75, color='black')
    #ax.text(X_MAX/10.0, PEAK_PERF+(PEAK_PERF)/10, "Peak Performance ("+str(PEAK_PERF)+" F/C)", fontsize=8)
    label_string = label+" ("+str(peakPerf)+" F/C)"
    yCoordinateTransformed = (math.log(peakPerf)-math.log(Y_MIN))/(math.log(Y_MAX/Y_MIN))
    ax.text(1 - len(label_string) / 120. - 0.01,yCoordinateTransformed+0.01, label_string, fontsize=8, transform=ax.transAxes)


def addBWLine(BW, label):
    x = np.linspace(X_MIN, X_MAX, 10)
    y = x*BW
    ax.plot(x, y, linewidth=0.75, color='black')
    yCoordinateTransformed = (math.log(X_MIN*BW)-math.log(Y_MIN))/(math.log(Y_MAX/Y_MIN))+0.16 #0.16 is the offset of the lower axis
    ax.text(X_MIN*1.1,(X_MIN*1.1*BW)*1.1, label+' ('+str(BW)+' B/C)',fontsize=8, rotation=np.arctan(INVERSE_GOLDEN_RATIO * AXIS_ASPECT_RATIO) * 180 / np.pi, verticalalignment = 'bottom')
    #~ ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(BW))-1), label+' ('+str(BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)


X_MIN=0.01
X_MAX=100.0
Y_MIN=0.01
Y_MAX=50.0
#PEAK_PERF=8.0
#PEAK_BW=11.95
PEAK_PERF=[2.0, 2.0]
PEAK_PERF_LABELS=['Scalar Peak Performance']
PEAK_BW=[6.3]
PEAK_BW_LABELS = ['Bandwidth']

INVERSE_GOLDEN_RATIO=0.618
OUTPUT_FILE="data-rooflinePlot.pdf"
TITLE=""
X_LABEL="Operational Intensity [Flops/Byte]"
Y_LABEL="Performance [Flops/Cycle]"
ANNOTATE_POINTS=1
AXIS_ASPECT_RATIO=math.log10(X_MAX/X_MIN)/math.log10(Y_MAX/Y_MIN)

#series = ['444', '450','470','482','999' ]
#series = ['daxpy-cold', 'daxpy-warm', 'daxpy-parallel-cold', 'daxpy-parallel-warm','fft-MKL-cold',  'fft-MKL-parallel-cold', 'fft-MKL-parallel-warm', 'dgemv-cold', 'dgemv-warm', 'dgemv-parallel-cold', 'dgemv-parallel-warm','dgemm-cold', 'dgemm-warm', 'dgemm-parallel-cold', 'dgemm-parallel-warm' ]
#series = ['daxpy-cold', 'daxpy-warm', 'daxpy-parallel-cold', 'daxpy-parallel-warm']
#series = ['dgemm-cold', 'dgemm-warm', 'dgemm-parallel-cold', 'dgemm-parallel-warm']
#series = ['fft-MKL-warm', 'fft-MKL-cold',  'fft-MKL-parallel-cold', 'fft-MKL-parallel-warm']
#series = ['dgemv-cold', 'dgemv-warm', 'dgemv-parallel-cold', 'dgemv-parallel-warm']
series= ['Accumulators-double-warm1','Accumulators-double-warm2','Accumulators-double-warm3','Accumulators-double-warm4','Accumulators-double-warm5','Accumulators-double-warm6','Accumulators-double-warm7','Accumulators-double-warm8']
#series= ['Accumulators-double-warm','Accumulators-double-cold']
#series= ['Accumulators-single-warm','Accumulators-single-cold']
#series = ['444', '450','470','482','999' ]
#series = ['daxpy-cold', 'daxpy-warm', 'daxpy-parallel-cold', 'daxpy-parallel-warm','fft-cold', 'fft-warm', 'fft-parallel-cold', 'fft-parallel-warm', 'dgemv-cold', 'dgemv-warm', 'dgemv-parallel-cold', 'dgemv-parallel-warm','dgemm-cold', 'dgemm-warm', 'dgemm-parallel-cold', 'dgemm-parallel-warm' ]
colors=[(0.6,0.011,0.043), (0.258, 0.282, 0.725),(0.2117, 0.467, 0.216),'#CC0033' ,'#FFFF00','green','cyan','yellow','brown','orange' ]
fig = plt.figure()
# Returns the Axes instance
ax = fig.add_subplot(111)

#Log scale - Roofline is always log-log plot, so remove the condition if LOG_X
ax.set_yscale('log')
ax.set_xscale('log')

#formatting:
ax.set_title(TITLE,fontsize=14,fontweight='bold')
ax.set_xlabel(X_LABEL, fontproperties = font, fontsize=12)
ax.set_ylabel(Y_LABEL, fontproperties = font, fontsize=12)


#x-y range
ax.axis([X_MIN,X_MAX,Y_MIN,Y_MAX])
ax.set_aspect(INVERSE_GOLDEN_RATIO*AXIS_ASPECT_RATIO)



# Manually adjust xtick/ytick labels when log scale
locs, labels = xticks()
minloc =int(math.log10(X_MIN))
maxloc =int(math.log10(X_MAX) +1)
newlocs = []
newlabels = []
for i in range(minloc,maxloc):
    newlocs.append(10**i)
    # Do not plot the first label, it is ugly in the corner
    if i==minloc:
        newlabels.append('')
    elif i==maxloc-1: #Do not plot the last label either
        newlabels.append('')
    elif 10**i <= 100:
        newlabels.append(str(10**i))
    else:
        newlabels.append(r'$10^ %d$' %i)
xticks(newlocs, newlabels)

locs, labels = yticks()
minloc =int(math.log10(Y_MIN))
maxloc =int(math.log10(Y_MAX) +1)
newlocs = []
newlabels = []
for i in range(minloc,maxloc):
    newlocs.append(10**i)
    if i==minloc:
        newlabels.append('')
    elif 10**i <= 100:
        newlabels.append(str(10**i))
    else:
        newlabels.append(r'$10^ %d$' %i)
yticks(newlocs, newlabels)

# Load the data

pp = []
ss=[]
for serie,i in zip(series,range(len(series))):
    nCycles = []
    file_in = open('tsc_'+serie+'.txt','r')
    lines = file_in.readlines()
    for line in lines:
        split_line = line.rstrip('\n').split(' ')
        nCycles.append(split_line)

    file_in.close()

    nFLOPS = []
    file_in = open('flop_'+serie+'.txt','r')
    lines = file_in.readlines()
    for line in lines:
            split_line = line.rstrip('\n').split(' ')
            nFLOPS.append(split_line)

    file_in.close()

    bytesTransferred = []
    file_in = open('bytes_transferred_'+serie+'.txt','r')
    lines = file_in.readlines()
    for line in lines:
            split_line = line.rstrip('\n').split(' ')
            bytesTransferred.append(split_line)

    file_in.close()

    yData =[]
    for f,c in zip(nFLOPS,nCycles):
        yData.append([float(vf)/float(vc) for vf, vc in zip(f,c) if vf != '' and vc != ''])

    xData =[]
    for f,b in zip(nFLOPS,bytesTransferred):
        xDataTmp = []
        for vf, vb in zip(f,b):
            if vf != '' and vb != '' and float(vb)!= 0:
                xDataTmp.append(float(vf)/float(vb))
            if float(vb)== 0:
                xDataTmp.append(float(vf)/X_MAX)
        xData.append(xDataTmp)

    x=[]
    xerr_low=[]
    xerr_high = []
    yerr_high = []
    y = []
    yerr_low = []

    for xDataItem in xData:
        x.append(stats.scoreatpercentile(xDataItem, 50))
        xerr_low.append(stats.scoreatpercentile(xDataItem, 25))
        xerr_high.append(stats.scoreatpercentile(xDataItem, 75))

    for yDataItem in yData:
        y.append(stats.scoreatpercentile(yDataItem, 50))
        yerr_low.append(stats.scoreatpercentile(yDataItem, 25))
        yerr_high.append(stats.scoreatpercentile(yDataItem, 75))

    xerr_low = [a - b for a, b in zip(x, xerr_low)]
    xerr_high = [a - b for a, b in zip(xerr_high, x)]
    yerr_low = [a - b for a, b in zip(y, yerr_low)]
    yerr_high = [a - b for a, b in zip(yerr_high, y)]

    p, =ax.plot(x, y, '-', color=colors[i],label=serie)
    pp.append(p)
    ss.append(serie)
    ax.errorbar(x, y, yerr=[yerr_low, yerr_high], xerr=[xerr_low, xerr_high], fmt='b.',elinewidth=0.4, ecolor = 'Black', capsize=0, color=colors[i])

    # Read sizes
    sizes = []
    file_in = open('size_'+serie+'.txt','r')
    lines = file_in.readlines()
    for line in lines:
        split_line = line.rstrip('\n').split(' ')
        sizes.append(split_line)

    file_in.close()

    if ANNOTATE_POINTS:
        ax.annotate(sizes[0][0],
        xy=(x[0], y[0]), xycoords='data',
        xytext=(+3, +1), textcoords='offset points', fontsize=8)

        ax.annotate(sizes[0][len(sizes[0])-1],
        xy=(x[len(x)-1],y[len(y)-1]), xycoords='data',
        xytext=(+3, +1), textcoords='offset points', fontsize=8)

# Work around to get rid of the problem with frameon=False and the extra space generated in the plot
ax.legend(pp,ss, numpoints=1, loc='best',fontsize =6).get_frame().set_visible(False)
#ax.legend(pp,ss, numpoints=1, loc='best',fontsize =6,frameon = False )





#Peak performance line and text
for p,l in zip(PEAK_PERF, PEAK_PERF_LABELS):
    addPerfLine(p,l)

#ax.axhline(y=PEAK_PERF, linewidth=0.75, color='black')
#yCoordinateTransformed = (log(PEAK_PERF)-log(Y_MIN))/(log(Y_MAX/Y_MIN))
#ax.text(0.76,yCoordinateTransformed+0.01, "Peak Performance ("+str(PEAK_PERF)+" F/C)", fontsize=8, transform=ax.transAxes)

#BW line and text
for bw,l in zip(PEAK_BW, PEAK_BW_LABELS):
    addBWLine(bw,l)
#x = np.linspace(X_MIN, X_MAX, X_MAX)
#y = x*PEAK_BW
#ax.plot(x, y, linewidth=0.75, color='black')
#yCoordinateTransformed = (log(X_MIN*PEAK_BW)-log(Y_MIN))/(log(Y_MAX/Y_MIN))+0.16 #0.16 is the offset of the lower axis
#ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(PEAK_BW))-1),'MemLoad ('+str(PEAK_BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)


#save file
fig.savefig(OUTPUT_FILE, dpi=250,  bbox_inches='tight')