from netCDF4 import *
import numpy as np
import matplotlib.pyplot as plt

class NetCDF:
    def __init__(self,ncdfgroup):
        self.ncdfgroup = Dataset(ncdfgroup)
    
    def ndims(self):
        return len(self.ncdfgroup.dimensions)
    
    def get_global_dim_names(self):
        return self.ncdfgroup.dimensions.keys()
    
    def get_global_dim_lens(self):
        lens = []
        for dim in self.ncdfgroup.dimensions.values():
            lens.append(len(dim))
        return lens 
        
    def nvars(self):
        return len(self.ncdfgroup.variables)
    
    def get_var_names(self):
        return self.ncdfgroup.variables.keys()
    
    def get_var_dim_lens(self,var):
        return self.ncdfgroup.variables[var].shape
    
    def get_var_dim_names(self,var):
        return self.ncdfgroup.variables[var].dimensions

    def get_num_of_points(self,var):
        v = 1
        for dim in self.get_var_dim_lens(var):
            v = v * dim
        return v

    def get_num_of_cells(self,var):
        v = 1
        for dim in self.get_var_dim_lens(var):
            v = v * (dim - 1)
        return v

    def get_data(self,var):
        return np.array(self.ncdfgroup.variables[var])

    def plot_histogram(self,var):
        data = self.get_data(var)
        data = data.reshape(self.get_num_of_points(var))
        plt.hist(data)
        plt.show()
    
        
    def data_at_comp_pos(self, var, c_coords):
        vardata = self.get_data(var)
        for i in c_coords:
            vardata = vardata[i]
        return vardata

    def phys2comp(self, var, p_coords):
        c_coords = [];
        dimensions = self.get_var_dim_names(var)
        step = []
        start = []
        for i in range(len(p_coords)):
            dim_data = self.get_data(dimensions[i])
            start.append( dim_data[0])
            step.append((dim_data[len(dim_data)-1]-start[i])/(len(dim_data)-1))
            c_coords.append(int((p_coords[i]-start[i])/step[i]))
        return c_coords

    def data_at_phys_pos(self, var, p_coords):
        c_coords = self.phys2comp(var,p_coords)
        return self.data_at_comp_pos(var,c_coords)

    def get_slice(self, var, dim, value):
        vardata = self.get_data(var)
        if dim in self.get_var_names():
            dimdata = self.get_data(dim)
            value = dimdata.index(value)
        dimindex = (self.get_var_dim_names(var)).index(dim)
        condition = []
        dimlength = self.get_var_dim_lens(var)[(self.get_var_dim_names(var)).index(dim)]
        for i in range(dimlength):
            if i == dimindex:
                condition.append(True)
            else:
                condition.append(False)
        return np.compress(condition, vardata, axis=dimindex)
    
    def volume_composite(self, var, dim, dir, min_idx, max_idx, val):
        if len(self.get_var_dim_lens(var)) != 3:
            print var+" is not a 3D Array"
        else:
            data = self.get_data(var)
            dimindex = (self.get_var_dim_names(var)).index(dim)
            dimlength = self.get_var_dim_lens(var)[dimindex]
            condition = []
            for i in range(dimlength):
                if i<=max_idx & i>=min_idx:
                    condition.append(True)
                else:
                    condition.append(False)
            
            dimdata = compress(condition, data, axis=dimindex)
            if dir == -1:
                dimdata = np.swapaxes(np.swapaxes(dimdata, 0, dimindex)[::-1], 0, dimindex)
