
import pya as kdb

from .mosfet import models, make_mosfet

class MOSFETPCell(kdb.PCellDeclarationHelper):

  def __init__(self):

    super().__init__()

    choices = [ (s, s) for s in models ]
    cont_choices = [ ( "None", 0 ), ( "Up to li", 1 ), ( "Up to met1", 2 ) ]

    self.param("_version", self.TypeInt, "Version", hidden=True, default=0)
    self.param("model", self.TypeInt, "Model", choices=choices, default=models[0])
    self.param("w",  self.TypeDouble, "Width", default=1.0, unit="µm")
    self.param("l",  self.TypeDouble, "Length", default=0.15, unit="µm")
    self.param("nf", self.TypeInt, "Number of fingers", default=1)
    self.param("min_poly_space", self.TypeDouble, "Min. Poly Space", default=0.0, unit="µm")
    self.param("source_cont", self.TypeInt, "Source Contacts", choices=cont_choices, default=1)
    self.param("drain_cont", self.TypeInt, "Drain Contacts", choices=cont_choices, default=1)

  def coerce_param_impl(self):
    self.w = max(0.2, self.w)
    self.l = max(0.15, self.l)
    self.nf = min(10000, max(1, self.nf))

  def display_text_impl(self):
    return "MOSFET %s w:%.12g l:%.12g nf:%d" % (self.model, self.w, self.l, self.nf)

  def produce_impl(self):
    gen = make_mosfet(model=self.model, 
                      w=self.w, l=self.l, nf=self.nf,
                      s_cont=self.source_cont, d_cont=self.drain_cont,
                      min_poly_space=self.min_poly_space)
    gen.produce(self.cell, kdb.DTrans())
    

