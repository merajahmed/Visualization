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

    def phys2comp(p_coords, p2c_map):
        c_coords = [];
        for i in p_coords:
            c_coords.append(p_coords[i] * p2c_map[i])
        return c_coords;
    
    # def comp2phys(c_coords, p2c_map):
    #     p_coords = [];
    #     for i in c_coords:
    #         p_coords.append(c_coords[i] / p2c_map[i])
    #     return p_coords;

    def data_at_phys_pos(self, var, p_coords, p2c_map):
        c_coords = phys2comp(p_coords, p2c_map)
        return self.data_at_phys_pos(var,c_coords)
