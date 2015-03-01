from vtk import *
 
# The source file
file_name = "../data/cylinder.vtk"
 
# Read the source file.
reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
reader.Update()

# Create the mapper that corresponds the objects of the vtk file
# into graphics elements
coloring_by = 'Pres'
mapper = vtkDataSetMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarModeToUsePointData()
mapper.SetColorModeToMapScalars()
scalarRange = reader.GetOutputDataObject(0).GetPointData().GetArray(coloring_by).GetRange()
mapper.SetScalarRange(scalarRange)

scalarBar = vtkScalarBarActor()
scalarBar.SetLookupTable(mapper.GetLookupTable())
scalarBar.SetTitle("ColorLegend")
scalarBar.SetNumberOfLabels(4)

colorMap = vtkLookupTable()
colorMap.SetTableRange(0, 1)
colorMap.SetHueRange(0, 0.7)
colorMap.SetSaturationRange(1, 1)
colorMap.SetValueRange(1, 1)
colorMap.Build()

mapper.SetLookupTable(colorMap)
scalarBar.SetLookupTable(colorMap)
 
# Create the Actor
actor = vtkActor()
actor.SetMapper(mapper)
# task 1
# actor.GetProperty().SetRepresentationToPoints()
# task 2
# actor.GetProperty().SetRepresentationToWireframe()
# task 3
# actor.GetProperty().SetRepresentationToSurface()
# task 4
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().EdgeVisibilityOn()
 
# Create the Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor2D(scalarBar)
renderer.SetBackground(.3, .3, .3) # Set background to white
 
# Create the RendererWindow
renderer_window = vtkRenderWindow()
renderer_window.AddRenderer(renderer)
 
# Create the RendererWindowInteractor and display the vtk_file
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderer_window)
interactor.Initialize()
interactor.Start()