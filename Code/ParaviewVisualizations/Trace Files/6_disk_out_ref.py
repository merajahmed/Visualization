#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
disk_out_refex2 = GetActiveSource()

# Properties modified on disk_out_refex2
disk_out_refex2.ElementBlocks = ['Unnamed block ID: 1 Type: HEX8']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [981, 819]

# show data in view
disk_out_refex2Display = Show(disk_out_refex2, renderView1)
# trace defaults for the display properties.
disk_out_refex2Display.ColorArrayName = [None, '']
disk_out_refex2Display.DiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]
disk_out_refex2Display.BackfaceDiffuseColor = [0.5000076295109483, 0.0, 0.5000076295109483]
disk_out_refex2Display.ScalarOpacityUnitDistance = 1.3249258044319845

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(disk_out_refex2Display, ('POINTS', 'GlobalNodeId'))

# rescale color and/or opacity maps used to include current data range
disk_out_refex2Display.RescaleTransferFunctionToDataRange(True)

# change representation type
disk_out_refex2Display.SetRepresentationType('Volume')

# get color transfer function/color map for 'GlobalNodeId'
globalNodeIdLUT = GetColorTransferFunction('GlobalNodeId')

# get opacity transfer function/opacity map for 'GlobalNodeId'
globalNodeIdPWF = GetOpacityTransferFunction('GlobalNodeId')

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-16.152509413544767, 24.62859077738983, -40.37315026639653]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.07999992370605469]
renderView1.CameraViewUp = [0.2762395054146659, 0.8659551786820527, 0.4169092996827908]
renderView1.CameraParallelScale = 12.951115722667065

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).