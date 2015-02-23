from netcdf_api import NetCDF

# test
n1 = NetCDF("tos_O1_2001-2002.nc")
print ("the dimensions of the input variable: ")
print (n1.get_var_dim_lens('tos'))
print ("the names of the dimensions for the variable: " )
print (n1.get_var_dim_names('tos'))
print ("the number of grid points that have the variable: ")
print (n1.get_num_of_points('tos'))
print ("the number of cells that have the variable: ")
print (n1.get_num_of_cells('tos'))

n1.sample('tos', 90, 85)