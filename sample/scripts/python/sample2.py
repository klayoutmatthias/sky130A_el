from pya import *

layout = Layout()

layer1 = layout.layer(1, 0)

child_cell = layout.create_cell("CHILD")
box = DBox(-0.5, -1.0, 0.5, 1.0)
child_cell.shapes(layer1).insert(box)

top_cell = layout.create_cell("TOP")
t = DTrans(1.0, 2.0) * DTrans.R90
a = DVector(0, 3.0)
b = DVector(4.0, 0.0)
top_cell.insert(DCellInstArray(child_cell, t, a, b, 3, 2))

layout.write("sample.gds")
