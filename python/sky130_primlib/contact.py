
import pya as kdb

from .array import Array
from .justify import Justify
from .linear import Linear
from .rect import Rect
from .rules import Rules
from .layers import Layers

def make_layer(layer, enc1, enc2 = None):
  if enc2 is None:
    return (layer, enc1, enc1)
  else:
    return (layer, enc1, enc2)
  
class LICONContact:

  li_enc = (Rules.li_licon_enc_one, Rules.li_licon_enc, Rules.li_licon_enc_all)

  def via_layer(self, nx: int, ny: int, w: float, h: float):
    # name, dimension, spacing
    return ("licon", Rules.licon_size, Rules.licon_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    single_x = (nx == 1 and w < Rules.licon_size - 1e-10)
    single_y = (ny == 1 and h < Rules.licon_size - 1e-10)
    if single_x != single_y:
      if single_x:
        top_enc_x, top_enc_y, _ = LICONContact.li_enc
      else:
        top_enc_y, top_enc_x, _ = LICONContact.li_enc
    else:
      top_enc_x = top_enc_y = LICONContact.li_enc[2]
    # name, enclosure_x, enclosure_y
    return make_layer("li", top_enc_x, top_enc_y)

class NTapContact(LICONContact):

  def __init__(self):
    self.name = "ntap"
    self.description = "N Tap"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    # returns an array of (name, enl) or (name, enl_x, enl_y) tuples
    return [
      make_layer("tap", Rules.tap_con_enc),
      make_layer("nsdm", Rules.sdm_tap_enc + Rules.tap_con_enc)
    ]

class PTapContact(LICONContact):

  def __init__(self):
    self.name = "ptap"
    self.description = "P Tap"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    # returns an array of (name, enl) or (name, enl_x, enl_y) tuples
    return [
      make_layer("tap", Rules.tap_con_enc),
      make_layer("psdm", Rules.sdm_tap_enc + Rules.tap_con_enc)
    ]

class PolyContact(LICONContact):

  def __init__(self):
    self.name = "poly"
    self.description = "Poly"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    # returns an array of (name, enl) or (name, enl_x, enl_y) tuples
    return [
      make_layer("poly", Rules.poly_con_enc),
      make_layer("npc", Rules.npc_poly_con_enc)
    ]

class DiffContact(LICONContact):

  def __init__(self):
    self.name = "diff"
    self.description = "Diff"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    # returns an array of (name, enl) or (name, enl_x, enl_y) tuples
    return [
      make_layer("diff", Rules.diff_con_enc),
    ]

class LIContact:

  def __init__(self):
    self.name = "li"
    self.description = "LI to Met1"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("li", Rules.mcon_li_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("mcon", Rules.mcon_size, Rules.mcon_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    return make_layer("met1", Rules.mcon_met1_enc)

class M1Contact:

  def __init__(self):
    self.name = "met1"
    self.description = "Met1 to Met2"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("met1", Rules.met1_via1_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("via1", Rules.via1_size, Rules.via1_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    return make_layer("met2", Rules.met2_via1_enc)

class M2Contact:

  def __init__(self):
    self.name = "met2"
    self.description = "Met2 to Met3"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("met2", Rules.met2_via2_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("via2", Rules.via2_size, Rules.via2_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    return make_layer("met3", Rules.met3_via2_enc)

class M3Contact:

  def __init__(self):
    self.name = "met3"
    self.description = "Met3 to Met4"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("met3", Rules.met3_via3_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("via3", Rules.via3_size, Rules.via3_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    return make_layer("met4", Rules.met4_via3_enc)

class M4Contact:

  def __init__(self):
    self.name = "met4"
    self.description = "Met4 to Met5"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("met4", Rules.met4_via4_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("via4", Rules.via4_size, Rules.via4_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    single_x = (nx == 1)
    single_y = (ny == 1)
    enc_y = enc_x = Rules.met5_via4_enc
    e1 = 0.5 * (Rules.met5_width - Rules.via4_size)
    if single_x:
      enc_x = e1
    if single_y:
      enc_y = e1
    return make_layer("met5", enc_x, enc_y)


via_defs = [
  NTapContact(),
  PTapContact(),
  PolyContact(),
  DiffContact(),
  LIContact(),
  M1Contact(),
  M2Contact(),
  M3Contact(),
  M4Contact()
]  

def make_contact(via_name: str = "", 
                 via_index: int = None, 
                 nx: int = 1, ny: int = 1, 
                 w: float = 0.0, h: float = 0.0,
                 make_bot: bool = True):
                
  if via_index is None:
    via_index = 0
    for i in range(0, len(via_defs)):
      if via_defs[i].name == via_name:
        via_index = i
        break

  via_def = via_defs[via_index]
  
  if make_bot:
    lbot = via_def.bot_layers(nx, ny, w, h)
  else:
    lbot = []
    
  ltop = via_def.top_layer(nx, ny, w, h)
  _, top_enc_x, top_enc_y = ltop
  
  lvia, dim, space = via_def.via_layer(nx, ny, w, h)
  lvia = Layers.by_name(lvia)
  
  w_via = w - top_enc_x * 2
  h_via = h - top_enc_y * 2

  via_rect = Rect(layer=lvia, w=dim, h=dim, halo=space * 0.5)
  array = Array(child=via_rect, nx=nx, ny=ny, w=w_via, h=h_via)
  stack = [array]
  
  for lb in lbot:
    layer, enc_x, enc_y = lb
    layer = Layers.by_name(layer)
    stack.append(Rect(layer=layer, enclose=array, enl_x=enc_x, enl_y=enc_y, w=w-2*enc_x, h=h-2*enc_y))

  layer, enc_x, enc_y = ltop
  layer = Layers.by_name(layer)
  stack.append(Rect(layer=layer, enclose=array, enl_x=enc_x, enl_y=enc_y, w=w-2*enc_x, h=h-2*enc_y, name="top"))
  
  return Justify(child = Linear(children=stack, align="C"), ref_point="C")

