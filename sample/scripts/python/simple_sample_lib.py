import pya
import math

class Circle(pya.PCellDeclarationHelper):

  def __init__(self):
    super().__init__()
    self.param("l", self.TypeLayer, "Layer")
    self.param("r", self.TypeDouble, "Radius", default = 1.0)
    self.param("n", self.TypeInt, "Number of points", default = 64)     

  def display_text_impl(self):
    return f"Circle(L={self.l},R={self.r})"
  
  def produce_impl(self):
    pts = []
    da = math.pi * 2 / self.n
    for i in range(0, self.n):
      p = pya.DPoint(self.r*math.cos(i*da), self.r*math.sin(i*da))
      pts.append(p)
    self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))


class MyLib(pya.Library):

  def __init__(self):
    self.description = "A Simple Sample Library"
    
    # populate the library
    self.layout().register_pcell("Circle", Circle())
    
    self.register("SimpleSampleLib")

# create and register the library
MyLib()
