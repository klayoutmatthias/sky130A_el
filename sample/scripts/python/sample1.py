from pya import *

layout = Layout()

layer1 = layout.layer(1, 0)

top_cell = layout.create_cell("TOP")

box = DBox(-0.5, -1.0, 0.5, 1.0)
top_cell.shapes(layer1).insert(box)

layout.write("sample.gds")
