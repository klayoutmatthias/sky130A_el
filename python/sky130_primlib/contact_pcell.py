
import pya as kdb

from .contact import bot_layers, make_contact

class ContactPCell(kdb.PCellDeclarationHelper):

  def __init__(self):

    super().__init__()

    choices = []
    for i in range(0, len(bot_layers)):
      choices.append(( bot_layers[i], i ))

    self.param("bot_index", self.TypeInt, "Bottom Layer", choices = choices, default = 0)
    self.param("nx", self.TypeInt, "Columns (or width, whichever is larger)", default = 1)
    self.param("ny", self.TypeInt, "Rows (or height, whichever is larger)", default = 1)
    self.param("w",  self.TypeDouble, "Width (or columns, whichever is larger)", default = 0)
    self.param("h",  self.TypeDouble, "Height (or rows, whichever is larger)", default = 0)

  def coerce_param_impl(self):
    self.nx = max(1, self.nx)
    self.ny = max(1, self.ny)

  def display_text_impl(self):
    bn = bot_layers[self.bot_index]
    return "Contact %s %d,%d (nx,ny) %.12g,%.12g (w,h)" % (bn, self.nx, self.ny, self.w, self.h)

  def produce_impl(self):
    gen = make_contact(bot_index = self.bot_index, nx = self.nx, ny = self.ny, w = self.w, h = self.h)
    gen.produce(self.cell, kdb.DTrans())
    

