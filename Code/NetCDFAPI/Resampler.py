from netcdf_api import NetCDF
import numpy as np
from netCDF4 import Dataset

class Sampler:
    def sample_tos_lat_lon(self,ncdf,sampledfile,var,londim,latdim):
        lat_original_length = ncdf.get_var_dim_lens('lat')[0]
        lon_original_length = ncdf.get_var_dim_lens('lon')[0]
        time_length = 24
        tos_scaled_lon = np.empty([time_length,lat_original_length,londim],dtype=np.float32)
        #np.reshape(tos_scaled_lon, (time_length,lat_original_length,londim))
        for i in range(time_length):
            for j in range(lat_original_length):
                y=np.interp(range(londim), range(lon_original_length),ncdf.get_data(var)[i,j,:])
                for k in range(len(y)):
                    tos_scaled_lon[i,j,k] = y[k]
        tos_scaled = np.empty([time_length,latdim,londim],dtype=np.float32)
        #np.reshape(tos_scaled_lon, (time_length,latdim,londim))
        for i in range(time_length):
            for j in range(londim):
                y =np.interp(range(latdim),range(lat_original_length),tos_scaled_lon[i,:,j])
                for k in range(len(y)):
                    tos_scaled[i,k,j] = y[k]
                    
        lat_scaled = np.interp(range(latdim),range(lat_original_length),ncdf.get_data('lat'))
        lon_scaled = np.interp(range(londim),range(lon_original_length),ncdf.get_data('lon'))
        rootgrp = Dataset(sampledfile, 'w', format='NETCDF4')
        lat = rootgrp.createDimension('lat', latdim)
        lon = rootgrp.createDimension('lon', londim)
        time = rootgrp.createDimension('time', time_length)
        tos = rootgrp.createVariable('tos','f4',('time','lat','lon'))
        lats = rootgrp.createVariable('lat','f4',('lat',))
        lons = rootgrp.createVariable('lon','f4',('lon',))
        times = rootgrp.createVariable('time',np.dtype('int32').char,('time',))
        lats[:]=lat_scaled
        lons[:]=lon_scaled
        times[:] = ncdf.get_data('time') 
        tos[:]=tos_scaled
        rootgrp.close()
            
sample = Sampler()
n1 = NetCDF("tos_O1_2001-2002.nc")
sampledfile = 'upsample.nc'
sample.sample_tos_lat_lon(n1, sampledfile, 'tos', 360, 340)            
sampledfile = 'downsample.nc'
sample.sample_tos_lat_lon(n1, sampledfile, 'tos', 90, 85)      
imshow(upsample.get_data('tos')[19])
savefig('upsampled.png')
imshow(downsample.get_data('tos')[19])
savefig('downsampled.png'
