from vtk import  *
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from datashape.coretypes import float32
from numpy import  *
# The source file

tornado = "tornado.vtk"
reader = vtkStructuredPointsReader()
reader.SetFileName(tornado)
reader.Update()
output=reader.GetOutput()
print output
ImageScalar = vtk_to_numpy(output.GetPointData().GetArray(0))
print mean(ImageScalar,axis=0)
print mean(array(range(0,48)))
#  Dimensions: (48, 48, 48)
# Attributes Components Mean
# ImageScalars 3 [ 0.0053828  -0.00069639  0.00130795]
#  Bounding Box
#    Xmin,Xmax: (0, 47)
#    Ymin,Ymax: (0, 47)
#    Zmin,Zmax: (0, 47)
#Bounding Box Center - (23.5,23.5,23.5)
#Average position of grid points (23.5, 23.5, 23.5)

