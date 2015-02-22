#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
tornadovtk = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [981, 819]

# show data in view
tornadovtkDisplay = Show(tornadovtk, renderView1)
# trace defaults for the display properties.
tornadovtkDisplay.Representation = 'Outline'
tornadovtkDisplay.ColorArrayName = ['POINTS', '']
tornadovtkDisplay.DiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]
tornadovtkDisplay.BackfaceDiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]
tornadovtkDisplay.ScalarOpacityUnitDistance = 1.7320508075688774
tornadovtkDisplay.Slice = 23

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(tornadovtkDisplay, ('POINTS', 'ImageScalars'))

# rescale color and/or opacity maps used to include current data range
tornadovtkDisplay.RescaleTransferFunctionToDataRange(True)

# change representation type
tornadovtkDisplay.SetRepresentationType('Slice')

# get color transfer function/color map for 'ImageScalars'
imageScalarsLUT = GetColorTransferFunction('ImageScalars')

# get opacity transfer function/opacity map for 'ImageScalars'
imageScalarsPWF = GetOpacityTransferFunction('ImageScalars')

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-22.834508292406344, 32.60319586985278, -126.5084859866768]
renderView1.CameraFocalPoint = [23.500000000000007, 23.500000000000007, 23.50000000000001]
renderView1.CameraViewUp = [0.13125904928173826, 0.9911542382069392, 0.01960454197568264]
renderView1.CameraParallelScale = 40.703193977868615

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).