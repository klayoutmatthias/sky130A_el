
import pya as kdb

from .contact import via_defs, make_contact

class ContactPCell(kdb.PCellDeclarationHelper):

  def __init__(self):

    super().__init__()

    choices = [ (s.description, s.name) for s in via_defs ]

    self.param("_version", self.TypeInt, "Version", hidden = True, default = 0)
    self.param("via", self.TypeString, "Via Type", choices = choices, default = via_defs[0].name)
    self.param("nx", self.TypeInt, "Columns (or width, whichever is larger)", default = 1)
    self.param("ny", self.TypeInt, "Rows (or height, whichever is larger)", default = 1)
    self.param("w",  self.TypeDouble, "Width (or columns, whichever is larger)", default = 0)
    self.param("h",  self.TypeDouble, "Height (or rows, whichever is larger)", default = 0)

  def _via_index(self):
    for i in range(0, len(via_defs)):
      if via_defs[i].name == self.via:
        return i
    raise ValueError("Invalid via name: " + self.via)
    
  def coerce_param_impl(self):
    self.nx = max(1, self.nx)
    self.ny = max(1, self.ny)

  def display_text_impl(self):
    return "Contact %s %d,%d (nx,ny) %.12g,%.12g (w,h)" % (self.via, self.nx, self.ny, self.w, self.h)

  def produce_impl(self):
    gen = make_contact(via_index = self._via_index(), nx = self.nx, ny = self.ny, w = self.w, h = self.h)
    gen.produce(self.cell, kdb.DTrans())
    

