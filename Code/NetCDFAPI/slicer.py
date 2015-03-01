import time
from netcdf_api import NetCDF
from vtk import *
from numpy import *
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
tornado = NetCDF('tornado.nc')

lon_slice = tornado.get_slice('magnitude', 'height', 20)
shapelist = []
sliceshape = list(lon_slice.shape)
ncells = 1
for i in sliceshape:
    if i!=1:
        shapelist.append(i)
        ncells = ncells*i
slice = lon_slice.reshape(tuple(shapelist))
grid = vtkStructuredGrid()

grid.SetDimensions(shapelist[0],shapelist[1],1)
points = vtkPoints()
points.SetNumberOfPoints(shapelist[0]*shapelist[1])
count = 0
for i in range(shapelist[0]):
    for j in range(shapelist[1]):
        points.InsertPoint(count, (i, j, 0))
        count = count + 1
        

grid.SetPoints(points)
vtk_slice = vtkFloatArray()
count = 0
for i in range(shapelist[0]):
    for j in range(shapelist[1]):
        vtk_slice.InsertValue(count, slice[i,j])
        count = count + 1

grid.GetPointData().SetScalars(vtk_slice)

#fil = vtkStructuredGridWriter()
wsg = vtkXMLStructuredGridWriter()
wsg.SetInput(grid)
#wsg.SetFileTypeToBinary()
wsg.SetFileName("strgrd.vtk")
wsg.Write()
wsg.Update()
reader = vtkXMLStructuredGridReader()
reader.SetFileName("strgrd.vtk")
reader.Update()
 
geomFilter = vtkStructuredGridGeometryFilter()
 
geomFilter.SetInputConnection(reader.GetOutputPort())  
geomFilter.Update()
mapper = vtkPolyDataMapper()
 
mapper.SetInputConnection(geomFilter.GetOutputPort()) # Create an Actor
actor = vtkActor()
actor.SetMapper(mapper)
  
 
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 0, 1) # Set background to white
  
 
renderer_window = vtkRenderWindow()
renderer_window.AddRenderer(renderer)
  
  
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderer_window)
interactor.Initialize()
interactor.Start()

