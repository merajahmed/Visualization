from vtk import *
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from numpy import *

reader =  vtkNetCDFReader()
reader.SetFileName('isabel_pres_temp.nc')
reader.Update()
#reader.SetVariableArrayStatus('pressure', 1)

#variables = reader.GetVariableArrayName()
#print variables


reader.GetOutput().GetPointData().SetActiveScalars('pressure')
#print reader
#print nanmax(vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0)))
#set proper color and opacity values
opacity = vtkPiecewiseFunction()
opacity.AddPoint(-5395, 0)
opacity.AddPoint(2926, 1)
color = vtkColorTransferFunction()
color.AddRGBPoint(2926, 1, 0, 0)
volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(color)
volumeProperty.SetScalarOpacity(opacity)

# This class describes how the volume is rendered (through ray tracing).
compositeFunction = vtkVolumeRayCastCompositeFunction()
# We can finally create our volume. We also have to specify the data for it, as well as how the data will be rendered.
volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(compositeFunction)

volumeMapper.SetInputConnection(reader.GetOutputPort())

# The class vtkVolume is used to pair the preaviusly declared volume as well as the properties to be used when rendering that volume.
volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
 
# With almost everything else ready, its time to initialize the renderer and window, as well as creating a method for exiting the application
renderer = vtk.vtkRenderer()
renderWin = vtk.vtkRenderWindow()
renderWin.AddRenderer(renderer)
renderInteractor = vtk.vtkRenderWindowInteractor()
renderInteractor.SetRenderWindow(renderWin)
 
# We add the volume to the renderer ...
renderer.AddVolume(volume)
# ... set background color to white ...
renderer.SetBackground(1, 1, 1)
# ... and set window size.
renderWin.SetSize(400, 400)

# A simple function to be called when the user decides to quit the application.
def exitCheck(obj, event):
     if obj.GetEventPending() != 0:
         obj.SetAbortRender(1)
 
# Tell the application to use the function as an exit check.
renderWin.AddObserver("AbortCheckEvent", exitCheck)

renderInteractor.Initialize()
# Because nothing will be rendered without any input, we order the first render manually before control is handed over to the main-loop.
renderWin.Render()
renderInteractor.Start()
