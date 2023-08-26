
import pya as kdb

from .layers import Layers
from .rules import Rules
from .rect import Rect
from .array import Array
from .justify import Justify

class ContactPCell(kdb.PCellDeclarationHelper):

  bot_layers  = [ "diff",  "tap",   "poly",  "li",   "met1",  "met2",   "met3",   "met4" ]
  via_layers  = [ "licon", "licon", "licon", "mcon", "via1",  "via2",   "via3",   "via4" ]
  top_layers  = [ "li",    "li",    "li",    "met1", "met2",  "met3",   "met4",   "met5" ]

  bot_enc     = [ Rules.diff_con_enc,   Rules.tap_con_enc,    Rules.poly_con_enc,   Rules.mcon_li_enc,    Rules.met1_via1_enc,  Rules.met2_via2_enc,  Rules.met3_via3_enc,  Rules.met4_via4_enc   ]
  top_enc     = [ Rules.li_licon_enc,   Rules.li_licon_enc,   Rules.li_licon_enc,   Rules.mcon_met1_enc,  Rules.met2_via1_enc,  Rules.met3_via2_enc,  Rules.met4_via3_enc,  Rules.met5_via4_enc   ]
  dim         = [ Rules.licon_size,     Rules.licon_size,     Rules.licon_size,     Rules.mcon_size,      Rules.via1_size,      Rules.via2_size,      Rules.via3_size,      Rules.via4_size       ]
  space       = [ Rules.licon_spacing,  Rules.licon_spacing,  Rules.licon_spacing,  Rules.mcon_spacing,   Rules.via1_spacing,   Rules.via2_spacing,   Rules.via3_spacing,   Rules.via4_spacing    ]
    
  def __init__(self):

    super().__init__()

    choices = []
    for i in range(0, len(ContactPCell.bot_layers)):
      choices.append(( ContactPCell.bot_layers[i], i ))

    self.param("bot_index", self.TypeInt, "Bottom Layer", choices = choices, default = 0)
    self.param("nx", self.TypeInt, "Columns (or width, whichever is larger)", default = 1)
    self.param("ny", self.TypeInt, "Rows (or height, whichever is larger)", default = 1)
    self.param("w",  self.TypeDouble, "Width (or columns, whichever is larger)", default = 0)
    self.param("h",  self.TypeDouble, "Height (or rows, whichever is larger)", default = 0)

  def coerce_param_impl(self):
    self.nx = max(1, self.nx)
    self.ny = max(1, self.ny)

  def display_text_impl(self):
    bn = self.bot_layers[self.bot_index]
    return "Contact %s %d,%d (nx,ny) %.12g,%.12g (w,h)" % (bn, self.nx, self.ny, self.w, self.h)

  def produce_impl(self):

    lbot = Layers.__dict__[ContactPCell.bot_layers[self.bot_index]]
    ltop = Layers.__dict__[ContactPCell.top_layers[self.bot_index]]
    lvia = Layers.__dict__[ContactPCell.via_layers[self.bot_index]]

    bot_enc = ContactPCell.bot_enc[self.bot_index]
    top_enc = ContactPCell.top_enc[self.bot_index]
    dim     = ContactPCell.dim[self.bot_index]
    space   = ContactPCell.space[self.bot_index]
    
    w_via = self.w - max(bot_enc, top_enc) * 2
    h_via = self.h - max(bot_enc, top_enc) * 2

    via_rect      = Rect(layer = lvia, w = dim, h = dim, halo = space * 0.5)
    array         = Array(child = via_rect, nx = self.nx, ny = self.ny, w = w_via, h = h_via)
    top_met_added = Rect(layer = ltop, enclose = array, enl = top_enc, w = self.w, h = self.h)
    bot_met_added = Rect(layer = lbot, enclose = top_met_added, enl = bot_enc, w = self.w, h = self.h)
    just          = Justify(child = bot_met_added, ref_point = "C")
    
    just.produce(self.cell, kdb.DTrans())
    

