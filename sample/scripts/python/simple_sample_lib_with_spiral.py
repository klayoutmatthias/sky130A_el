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


class Spiral(pya.PCellDeclarationHelper):

  def __init__(self):
    super().__init__()
    self.param("l", self.TypeLayer, "Layer")
    self.param("r1", self.TypeDouble, "Radius1", default = 1.0)
    self.param("r2", self.TypeDouble, "Radius2", default = 2.0)
    self.param("w", self.TypeDouble, "Width", default = 0.2)
    self.param("t", self.TypeDouble, "Number of turns", default = 3)
    self.param("n", self.TypeInt, "Number of points per turn", default = 64)     

  def display_text_impl(self):
    return f"Spiral(L={self.l},R1={self.r1},R2={self.r2},T={self.t})"
  
  def produce_impl(self):
    pts = []
    da = math.pi * 2 / self.n
    ntot = int(self.n * self.t)
    for i in range(0, ntot + 1):
      r = self.r1 + (self.r2 - self.r1) * i / ntot
      p = pya.DPoint(r*math.cos(i*da), r*math.sin(i*da))
      pts.append(p)
    self.cell.shapes(self.l_layer).insert(pya.DPath(pts, self.w))

class MyLib(pya.Library):

  def __init__(self):
    self.description = "A Simple Sample Library"
    
    # populate the library
    self.layout().register_pcell("Circle", Circle())
    self.layout().register_pcell("Spiral", Spiral())
    
    self.register("SimpleSampleLib")

# create and register the library
MyLib()
