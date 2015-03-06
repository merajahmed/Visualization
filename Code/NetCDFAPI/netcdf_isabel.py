from netcdf_api import NetCDF
from matplotlib.pyplot import *

isabel_file = 'isabel_pres_temp.nc'
isabel = NetCDF(isabel_file)
C = isabel.volume_composite('pressure', 'height', 1, 80, 99, 100)
imshow(C)
gca().invert_yaxis()
show()
