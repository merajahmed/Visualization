from netCDF4 import *
import numpy as np
import matplotlib.pyplot as plt
from numpy import compress, nanmax, nanmin
import matplotlib.cm as cm
from matplotlib.pyplot import *
from matplotlib.colors import *
from matplotlib.pyplot import autoscale
from vtk import *


class NetCDF:
    def __init__(self,ncdfgroup):
        self.ncdfgroup = Dataset(ncdfgroup)
    
    def contour2D(self, var, dim, idx, val):
        #eliminate nans
            data = np.nan_to_num(self.get_slice(var, dim, idx))
            elim_idx = (data.shape).index(1)
            if elim_idx == 0:
                rows = data.shape[1]
                cols = data.shape[2]
            elif elim_idx == 1:
                rows = data.shape[0]
                cols = data.shape[2]
            else:
                rows = data.shape[0]
                cols = data.shape[1]
            data = np.reshape(data,(rows, cols))
            pointlist = []
            #mark vertices with value > val as 1, and others 0
            mask = data>val
            mask = mask.astype(int)
            for i in range(rows-1):
                for j in range(cols-1):
                    bitstring = str(mask[i][j])+str(mask[i][j+1])+str(mask[i+1][j])+str(mask[i+1][j+1])
                    case = int(bitstring, 2)
                    #find intersection points in current cell bounded by (tl, tr, br, bl) t- top, b- bottom, l- left, r- right
                    #add edge end points as consecutive points in pointlist
                    tl = data[i][j]
                    tr = data[i][j+1]
                    bl = data[i+1][j]
                    br = data[i+1][j+1]
                    if case == 1:
                        y = i+1
                        x = j+((val-bl)/(br-bl))
                        pointlist.append((x,y))
                        x = j+1
                        y = i + ((val-tr)/(br-tr))
                        pointlist.append((x,y))
                    elif case == 2:
                        x = j
                        y = i+ ((val-tl)/(bl-tl))
                        pointlist.append((x,y))
                        y = i+1
                        x = j+ ((val-bl)/(br-bl))
                        pointlist.append((x,y))
                    elif case == 3:
                        x = j
                        y = i + ((val-tl)/(bl-tl))
                        pointlist.append((x,y))
                        x = j+1
                        y = i + ((val-tr)/(br-tr))
                        pointlist.append((x,y))
                    elif case == 4:
                        y = i
                        x = j + ((val-tl)/(tr-tl))
                        pointlist.append((x,y))
                        x = j+1
                        y = i + ((val-tr)/(br-tr))
                        pointlist.append((x,y))
                    elif case == 5:
                        y = i
                        x = j + ((val-tl)/(tr-tl))
                        pointlist.append((x,y))
                        y = i+1
                        x = j + ((val-bl)/(br-bl))
                        pointlist.append((x,y))
                    elif case == 7:
                        y = i
                        x = j + ((val-tl)/(tr-tl))
                        pointlist.append((x,y))
                        x = j 
                        y = i + ((val-tl)/(bl-tl))
                        pointlist.append((x,y))
                    elif case == 8:
                        y = i
                        x = j+ ((val-tl)/(tr-tl))
                        pointlist.append((x,y))
                        x = j
                        y = i + ((val-tl)/(bl-tl))
                        pointlist.append((x,y))
                    elif case == 10:
                        y = i
                        x = j + ((val-tl)/(tr-tl))
                        pointlist.append((x,y))
                        y = i + 1
                        x = j + ((val-bl)/(br-bl))
                        pointlist.append((x,y))
                    elif case == 11:
                        y = i
                        x = j + ((val-tl)/(tr-tl))
                        pointlist.append((x,y))
                        x = j + 1
                        y = i + ((val-tr)/(br-tr))
                        pointlist.append((x,y))
                        
                    elif case == 12:
                        x = j
                        y = i + ((val-tl)/(bl-tl))
                        pointlist.append((x,y))
                        x = j+1
                        y = i + ((val-tr)/(br-tr))
                        pointlist.append((x,y))
                        
                    elif case == 13:
                        x = j
                        y = i + ((val-tl)/(bl-tl))
                        pointlist.append((x,y))
                        y = i+1
                        x = j + ((val-bl)/(br-bl))
                        pointlist.append((x,y))
                    
                    elif case == 14:
                        x = j+1
                        y = i + ((val-tr)/(br-tr))
                        pointlist.append((x,y))
                        y = i+1
                        x = j + ((val-bl)/(br-bl))
                        pointlist.append((x,y))
                        
                    elif case == 6:
                        mp = (tl+tr+bl+br)/4
                        if mp <= val:
                            x = j
                            y = i + ((val-tl)/(bl-tl))
                            pointlist.append((x,y))
                            y = i+1
                            x = j + ((val-bl)/(br-bl))
                            pointlist.append((x,y))
                            y = i 
                            x = j + ((val-tl)/(tr-tl))
                            pointlist.append((x,y))
                            x = j+1
                            y = i + ((val-tr)/(br-tr))
                            pointlist.append((x,y))
                        else:
                            y = i
                            x = j + ((val-tl)/(tr-tl))
                            pointlist.append((x,y))
                            x = j
                            y = i + ((val-tl)/(bl-tl))
                            pointlist.append((x,y))
                            x = j + 1
                            y = i + ((val-tr)/(br-tr))
                            pointlist.append((x,y))
                            y = i + 1
                            x = j + ((val-bl)/(br-bl))
                            pointlist.append((x,y))
                    elif case == 9:
                        mp = (tl+tr+bl+br)/4
                        if mp > val:
                            x = j
                            y = i + ((val-tl)/(bl-tl))
                            pointlist.append((x,y))
                            y = i+1
                            x = j + ((val-bl)/(br-bl))
                            pointlist.append((x,y))
                            y = i 
                            x = j + ((val-tl)/(tr-tl))
                            pointlist.append((x,y))
                            x = j+1
                            y = i + ((val-tr)/(br-tr))
                            pointlist.append((x,y))
                        else:
                            y = i
                            x = j + ((val-tl)/(tr-tl))
                            pointlist.append((x,y))
                            x = j
                            y = i + ((val-tl)/(bl-tl))
                            pointlist.append((x,y))
                            x = j + 1
                            y = i + ((val-tr)/(br-tr))
                            pointlist.append((x,y))
                            y = i + 1
                            x = j + ((val-bl)/(br-bl))
                            pointlist.append((x,y))
                            
            return pointlist
            
        
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
            
            #get part of the 3d array between min_idx and max_idx(both included)
            condition = []
            for i in range(dimlength):
                if i<=max_idx and i>=min_idx:
                    condition.append(True)
                else:
                    condition.append(False)
            dimdata = compress(condition, data, axis=dimindex)
            
            #invert along viewing axis if dir = -1
            if dir == -1:
                dimdata = np.swapaxes(np.swapaxes(dimdata, 0, dimindex)[::-1], 0, dimindex)
            
            #make the viewing axis z-axis 
            if dimindex != 2:
                dimdata = np.swapaxes(dimdata,2,dimindex)
            
            #eliminate nans
            dimdata = np.nan_to_num(dimdata)
            
            max_val = nanmax(dimdata)
            min_val = nanmin(dimdata)
            opacity = np.empty(dimdata.shape, dtype = np.float32)
                        
            #create normalization scale for color mapping
            norm = Normalize(vmin = min_val, vmax=max_val)
            #norm.autoscale(dimdata)
            
            #color mapping function
            scalarmap = cm.ScalarMappable(norm=norm, cmap=cm.hot)
            
            color = np.empty(dimdata.shape,dtype=[('r', float),('g', float),('b',float)])
            
            #create transfer function
            for i in range(dimdata.shape[0]):
                for j in range(dimdata.shape[1]):
                    for k in range(dimdata.shape[2]):
                        dimval = dimdata[i,j,k]
                        color[i, j, k] = scalarmap.to_rgba(dimval)[:3]
                        #tent function map for opacity, val = 1, max_val = 0, min_val = 0
                        if dimval >= val:
                            opacity[i,j,k] = 1-((dimval-val)/(max_val-val))
                        elif dimval > val:
                            opacity[i,j,k] = 1-((dimval-val)/(min_val-val))
            
            #blending, alpha composting for each color component
            for i in range(max_idx-min_idx+1):
                if i == 0:
                    R = color[:,:,0]['r']
                    G = color[:,:,0]['g']
                    B = color[:,:,0]['b']
                     
                else:
                    R = np.add(np.multiply(R , (1-opacity[:,:,i])), np.multiply(color[:,:,i]['r'],opacity[:,:,i]))
                    G = np.add(np.multiply(G , (1-opacity[:,:,i])), np.multiply(color[:,:,i]['g'],opacity[:,:,i]))
                    B = np.add(np.multiply(B , (1-opacity[:,:,i])), np.multiply(color[:,:,i]['b'],opacity[:,:,i]))
            
            #return rgb array         
            C = (np.dstack((R,G,B)) * 255.999) .astype(np.uint8)
            return C
        
        
