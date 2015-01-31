from vtk import  *
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from datashape.coretypes import float32
from numpy import  *
# The source file
cylinder = "cylinder.vtk"
tornado = "tornado.vtk"

 
# Read the source file.
reader = vtkUnstructuredGridReader()
reader.SetFileName(cylinder)
reader.Update() # Needed because of GetScalarRange
output = reader.GetOutput()
Cell_Types = vtk_to_numpy(output.GetCellTypesArray())
print Cell_Types
for i in Cell_Types:
    if i != 12:
        print i
print len(Cell_Types)
print output.GetAttributes(0)
print output.GetAttributes(1)
print output.GetPoints()
pointcoords= vtk_to_numpy( output.GetPoints().GetData())

print mean(pointcoords,axis=0)

PedigreeNodeID=vtk_to_numpy(output.GetPointData().GetArray(0))
Temp=vtk_to_numpy(output.GetPointData().GetArray(1))
V=vtk_to_numpy(output.GetPointData().GetArray(2))
Pres=vtk_to_numpy(output.GetPointData().GetArray(3))
AsH3=vtk_to_numpy(output.GetPointData().GetArray(4))
GaMe3=vtk_to_numpy(output.GetPointData().GetArray(5))
CH4=vtk_to_numpy(output.GetPointData().GetArray(6))
H2=vtk_to_numpy(output.GetPointData().GetArray(7))
print mean(PedigreeNodeID)
print mean(Temp)
print mean(Pres)
print mean(AsH3)
print mean(GaMe3)
print mean(CH4)
print mean(H2)
print mean(V,axis=0)    
GlobalElementId= vtk_to_numpy(output.GetCellData().GetArray(0))
PedigreeElementId = vtk_to_numpy(output.GetCellData().GetArray(1))
print mean(GlobalElementId)
print mean(PedigreeElementId)

#Type of Cell = 12,Hexahedron
# Number of Cells = 7472
  #=============================================================================
  #Point Attributes Number of Components Mean
  #Array 0 name = PedigreeNodeId 1 4250.0
  #Array 1 name = Temp 1 425.163532063
  # Array 2 name = V 3 [  8.33003170e-08  -1.98482042e-08  -6.02950051e+00]
  # Array 3 name = Pres 1 0.0208810824191
  # Array 4 name = AsH3 1 0.138173172667
  # Array 5 name = GaMe3 1 0.00480803024179
  # Array 6 name = CH4 1 0.000514910423864
  # Array 7 name = H2 1 0.856503914931
  #Cell Attributes Number of Componenets Mean
  #Array 0 name = GlobalElementId 1 3736.5
  #Array 1 name = PedigreeElementId 1 3736.5
  #confirm if rank is same as number of components
  #Bounding Box
  #Bounds: 
   # Xmin,Xmax: (-5.75, 5.75)
    #Ymin,Ymax: (-5.75, 5.75)
    #Zmin,Zmax: (-10, 10.16)
  #Average Position Grid Points
#(0.0,2.79234349622e-16,2.63508661444)
#Center of Bounding box
#(0,0,0.08)
  #=============================================================================

        

