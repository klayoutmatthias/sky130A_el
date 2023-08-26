
import pya as kdb

from .contact import bot_layers, make_contact

class ContactPCell(kdb.PCellDeclarationHelper):

  def __init__(self):

    super().__init__()

    choices = [ (s, s) for s in bot_layers ]

    self.param("_version", self.TypeInt, "Version", hidden = True, default = 0)
    self.param("bot", self.TypeString, "Bottom Layer", choices = choices, default = bot_layers[0])
    self.param("nx", self.TypeInt, "Columns (or width, whichever is larger)", default = 1)
    self.param("ny", self.TypeInt, "Rows (or height, whichever is larger)", default = 1)
    self.param("w",  self.TypeDouble, "Width (or columns, whichever is larger)", default = 0)
    self.param("h",  self.TypeDouble, "Height (or rows, whichever is larger)", default = 0)

  def _bot_index(self):
    return bot_layers.index(self.bot)
    
  def coerce_param_impl(self):
    self.nx = max(1, self.nx)
    self.ny = max(1, self.ny)

  def display_text_impl(self):
    return "Contact %s %d,%d (nx,ny) %.12g,%.12g (w,h)" % (self.bot, self.nx, self.ny, self.w, self.h)

  def produce_impl(self):
    gen = make_contact(bot_index = self._bot_index(), nx = self.nx, ny = self.ny, w = self.w, h = self.h)
    gen.produce(self.cell, kdb.DTrans())
    

