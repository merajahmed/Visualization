#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
cylindervtk = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [662, 489]

# show data in view
cylindervtkDisplay = Show(cylindervtk, renderView1)
# trace defaults for the display properties.
cylindervtkDisplay.ColorArrayName = [None, '']
cylindervtkDisplay.ScalarOpacityUnitDistance = 1.3249258044319845

# reset view to fit data
renderView1.ResetCamera()

# change representation type
cylindervtkDisplay.SetRepresentationType('Surface With Edges')

# set scalar coloring
ColorBy(cylindervtkDisplay, ('POINTS', 'CH4'))

# rescale color and/or opacity maps used to include current data range
cylindervtkDisplay.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
cylindervtkDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'CH4'
cH4LUT = GetColorTransferFunction('CH4')
cH4LUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 0.00058512, 0.865003, 0.865003, 0.865003, 0.00117024, 0.705882, 0.0156863, 0.14902]
cH4LUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'CH4'
cH4PWF = GetOpacityTransferFunction('CH4')
cH4PWF.Points = [0.0, 0.0, 0.5, 0.0, 0.00117024, 1.0, 0.5, 0.0]
cH4PWF.ScalarRangeInitialized = 1

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-15.893193959723288, -46.557122299745316, 9.232548927286821]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.07999992370605469]
renderView1.CameraViewUp = [-0.5872874143100713, 0.04157855395131266, -0.8083097901450339]
renderView1.CameraParallelScale = 12.951115722667065

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).