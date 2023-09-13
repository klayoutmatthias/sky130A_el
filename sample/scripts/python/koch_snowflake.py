
from pya import *
import math

layout = Layout()

layer1 = layout.layer(1, 0)

# Build first-level cell

cell0 = layout.create_cell("C0")

cos30 = math.sqrt(3) / 2.0

pts = [ 
  DPoint(0, 0),
  DPoint(1.0, 0),
  DPoint(1.5, cos30),
  DPoint(2.0, 0),
  DPoint(3.0, 0)
]

width = 0.01

cell0.shapes(layer1).insert(DPath(pts, width))

prev_cell = cell0

# Build another level of cells based
# on a previous cell. Note that recursive 
# hierarchies are not allowed.
# Here we use 10 levels of recursion

for n in range(0, 10):

  new_cell = layout.create_cell("C" + str(n + 1))
  
  scale = 1.0 / 3.0

  for t in [
    DCplxTrans(scale, 0.0,   False, DVector(0, 0)),
    DCplxTrans(scale, 60.0,  False, DVector(1.0, 0)),
    DCplxTrans(scale, -60.0, False, DVector(1.5, cos30)),
    DCplxTrans(scale, 0.0,   False, DVector(2.0, 0)),
  ]:
    new_cell.insert(DCellInstArray(prev_cell, t))
    
  prev_cell = new_cell
  
# finalize by placing the final cell three times
# to form a triangle

top_cell = layout.create_cell("TOP")

for t in [
  DCplxTrans(1.0, 0.0,    False, DVector(0, 0)),
  DCplxTrans(1.0, -120.0,  False, DVector(3.0, 0)),
  DCplxTrans(1.0, -240.0, False, DVector(1.5, -3.0 * cos30)),
]:
  top_cell.insert(DCellInstArray(prev_cell, t))

# write layout to "sample.gds"

layout.write("sample.gds")  