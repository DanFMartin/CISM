#!/usr/bin/env python
# Script to plot results of stream test case

# Import modules
import sys, os, numpy
from netCDF import *
from runStream import *  # Get all the parameter values and functions defined in the run script
from matplotlib import pyplot as plt

# Parse options
from optparse import OptionParser
optparser = OptionParser()
optparser.add_option("-f", "--file", dest="filename", default="stream.out.nc", help="file to test", metavar="FILE")
for option in optparser.option_list:
    if option.default != ("NO", "DEFAULT"):
        option.help += (" " if option.help else "") + "[default: %default]"
options, args = optparser.parse_args()



################################
# Start actual script here.

# Open file and get needed vars
f = NetCDFFile(options.filename, 'r')
y0 = f.variables['y0'][:]
ny = y0.shape[0] + 1  # the actual ny dimension, not the size of y0
dy = y0[1]-y0[0]
y0_centered = y0 - (ny-1) * dy / 2.0  # use y coord that are symmetrical about 0

uvel = f.variables['uvel'][0,:,:,:]  # get all levels at time 0
if netCDF_module == 'Scientific.IO.NetCDF':
   uvel = uvel * f.variables['uvel'].scale_factor

x0 = f.variables['x0'][:]
xpos = x0.shape[0]/2   # integer division on x-length to get the middle column of the domain
print 'Plotting uvel across-flow profile at x=',x0[xpos], ' (i=', xpos, ')'

# Calculate analytic velocity profile - the analytic functions are in runStream.py
if analytic_solution == 'raymond':
    uvel_analytic_profile = raymond_uvel(y0_centered)
    analytic_name = 'Raymond analytic solution'
elif analytic_solution == 'schoof':
    uvel_analytic_profile = schoof_uvel(y0_centered)
    # Some adjustments to the analytic profile - not entirely sure why these are needed.
    ind = numpy.nonzero( numpy.absolute(y0_centered) >= W )
    uvel_analytic_profile[ind] = uvel_analytic_profile.min()
    uvel_analytic_profile = uvel_analytic_profile - uvel_analytic_profile.min()
    analytic_name = 'Schoof analytic solution'
else:
    sys.exit("Error: Invalid value for 'analytic_solution'.")



# Setup plot of uvel cross-section
fig = plt.figure(1, facecolor='w', figsize=(10, 5), dpi=100)

plt.plot(y0/1000.0, uvel_analytic_profile, '-or', label=analytic_name)
plt.plot(y0/1000.0, uvel[ 0,:,xpos], '-xk', label='CISM surface')
plt.plot(y0/1000.0, uvel[-1,:,xpos], '-^k', label='CISM basal')

plt.xlabel('distance across flow (km)')
plt.ylabel('along flow velocity (m/a)')
plt.title(analytic_name)
plt.legend(loc='lower center')

plt.draw()
plt.show()

#f.close()





#ind = find( abs( yy ) >= W ); us(ind) = min( min( us ) );

#us = us - min( us );


#    subplot(2,1,2), hold on
#    xlabel( 'dist across flow (m)'), ylabel( 'yield stress (kPa)')
#    box on



#uvel=permute(ncread(filename, 'uvel'), [ 2 1 3 ] );
#vvel=permute(ncread(filename, 'vvel'), [ 2 1 3 ] );


#yy2 = [ yy yy(end)+dx yy(end)+2*dx ];
#yy2 = [ -fliplr(yy2(2:end)), yy2 ];

#if( flag == 0 )
#    figure(198)
#    subplot(2,1,1), hold on
#    plot( yy2/1e3, uvel(:,round(c/2),1), 'bo:' )
#    plot( yy2/1e3, uvel(:,end,1), 'b*' )              %% boundary value
#    legend( 'analytic', 'model', 'boundary' )
#    subplot(2,1,2), hold on
#    legend( 'specified', 'model' )
#else
#    figure(199)
#    subplot(2,1,1), hold on
#    plot( yy2/1e3, uvel(:,round(c/2),1), 'bo:' )
#    plot( yy2/1e3, uvel(:,end,1), 'b*' )              %% boundary value
#    legend( 'analytic', 'model', 'boundary' )
#    subplot(2,1,2), hold on
#    legend( 'specified', 'model' )
#end


