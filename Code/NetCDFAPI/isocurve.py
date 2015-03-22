from netcdfapi import NetCDF
from matplotlib.pyplot import *

isabel = NetCDF('isabel_pres_temp.nc')
contour= isabel.contour2D('pressure', 'height', 80, 100)
fig, ax = subplots()

for i in range(0,len(contour),2):
    line = contour[i:i+2] 
    (line_x, line_y) = zip(*line)
    ax.add_line(Line2D(line_x, line_y, linewidth=2, color='red'))
plot()
show()
