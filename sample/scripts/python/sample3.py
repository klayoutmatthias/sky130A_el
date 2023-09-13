from pya import *

layout = Layout()

layer1 = layout.layer(1, 0)
layer2 = layout.layer(2, 0)
layer3 = layout.layer(3, 0)

top_cell = layout.create_cell("TOP")

r = Region()
r.insert(Box(-500, -500, 500, 500))

rt = r.transformed(ICplxTrans(1.0, 45.0, False, Vector(0, 0)))

r1 = r - rt
r2 = rt - r
r3 = r & rt

top_cell.shapes(layer1).insert(r1)
top_cell.shapes(layer2).insert(r2)
top_cell.shapes(layer3).insert(r3)

layout.write("sample.gds")
