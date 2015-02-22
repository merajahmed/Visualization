#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
cylindervtk = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [981, 819]

# show data in view
cylindervtkDisplay = Show(cylindervtk, renderView1)
# trace defaults for the display properties.
cylindervtkDisplay.ColorArrayName = [None, '']
cylindervtkDisplay.DiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]
cylindervtkDisplay.BackfaceDiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]
cylindervtkDisplay.ScalarOpacityUnitDistance = 1.3249258044319845

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(cylindervtkDisplay, ('POINTS', 'Temp'))

# rescale color and/or opacity maps used to include current data range
cylindervtkDisplay.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
cylindervtkDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Temp'
tempLUT = GetColorTransferFunction('Temp')

# get opacity transfer function/opacity map for 'Temp'
tempPWF = GetOpacityTransferFunction('Temp')

# change representation type
cylindervtkDisplay.SetRepresentationType('Points')

# change representation type
cylindervtkDisplay.SetRepresentationType('Outline')

# create a new 'Contour'
contour1 = Contour(Input=cylindervtk)
contour1.ContourBy = ['POINTS', 'AsH3']
contour1.Isosurfaces = [0.1326579]
contour1.PointMergeMethod = 'Uniform Binning'

# show data in view
contour1Display = Show(contour1, renderView1)
# trace defaults for the display properties.
contour1Display.ColorArrayName = ['POINTS', 'Temp']
contour1Display.DiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]
contour1Display.LookupTable = tempLUT
contour1Display.BackfaceDiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]

# show color bar/color legend
contour1Display.SetScalarBarVisibility(renderView1, True)

# reset view to fit data
renderView1.ResetCamera()

# reset view to fit data
renderView1.ResetCamera()

# reset view to fit data
renderView1.ResetCamera()

# reset view to fit data
renderView1.ResetCamera()

# reset view to fit data
renderView1.ResetCamera()

# reset view to fit data
renderView1.ResetCamera()

# reset view to fit data
renderView1.ResetCamera()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-49.26490111262243, 7.890473115421582, -3.7460106246471616]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.07999992370605469]
renderView1.CameraViewUp = [0.14273026972457897, 0.9746616515350219, 0.17222872911152878]
renderView1.CameraParallelScale = 12.951115722667065

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).