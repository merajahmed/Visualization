#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
tos_O1_20012002nc = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [662, 489]

# show data in view
tos_O1_20012002ncDisplay = Show(tos_O1_20012002nc, renderView1)
# trace defaults for the display properties.
tos_O1_20012002ncDisplay.ColorArrayName = [None, '']
tos_O1_20012002ncDisplay.ScalarOpacityUnitDistance = 0.11047191946140596

# reset view to fit data
renderView1.ResetCamera()

# change representation type
tos_O1_20012002ncDisplay.SetRepresentationType('Wireframe')

# set scalar coloring
ColorBy(tos_O1_20012002ncDisplay, ('CELLS', 'tos'))

# rescale color and/or opacity maps used to include current data range
tos_O1_20012002ncDisplay.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
tos_O1_20012002ncDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'tos'
tosLUT = GetColorTransferFunction('tos')
tosLUT.RGBPoints = [271.1732482910156, 0.231373, 0.298039, 0.752941, 5.000000100204387e+19, 0.865003, 0.865003, 0.865003, 1.0000000200408773e+20, 0.705882, 0.0156863, 0.14902]
tosLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'tos'
tosPWF = GetOpacityTransferFunction('tos')
tosPWF.Points = [271.1732482910156, 0.0, 0.5, 0.0, 1.0000000200408773e+20, 1.0, 0.5, 0.0]
tosPWF.ScalarRangeInitialized = 1

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [2.2201097005826513, -0.22588568942637677, 6.2987618888023755]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.00759612349389599]
renderView1.CameraViewUp = [0.5207608104586732, 0.8397671029300705, -0.15362093323132214]
renderView1.CameraParallelScale = 1.7276763163579985

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).