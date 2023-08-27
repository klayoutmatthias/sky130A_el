
import math
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

class ContactBase:

  def __init__(self):
    self.bottom_is_metal = True
    
  def well_layers(self, nx: int, ny: int, w: float, h: float):
    return [
      make_layer("pr_bnd", 0.0)
    ]
    
class LICONContact(ContactBase):

  def __init__(self):
    super().__init__()
    self.bottom_is_metal = False
    
  li_enc = (Rules.li_licon_enc_one, Rules.li_licon_enc)

  def via_layer(self, nx: int, ny: int, w: float, h: float):
    # name, dimension, spacing
    return ("licon", Rules.licon_size, Rules.licon_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    single_x = (nx == 1 and w < Rules.licon_size - 1e-10)
    single_y = (ny == 1 and h < Rules.licon_size - 1e-10)
    if single_x or single_y:
      if single_x:
        top_enc_x, top_enc_y = LICONContact.li_enc
      else:
        top_enc_y, top_enc_x = LICONContact.li_enc
    else:
      top_enc_x = top_enc_y = Rules.li_licon_enc
    # name, enclosure_x, enclosure_y
    return make_layer("li", top_enc_x, top_enc_y)

class NTapContact(LICONContact):

  def __init__(self):
    super().__init__()
    self.name = "ntap"
    self.description = "N Tap"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    # returns an array of (name, enl) or (name, enl_x, enl_y) tuples
    return [
      make_layer("nwell", Rules.nwell_tap_enc + Rules.tap_con_enc),
      make_layer("tap", Rules.tap_con_enc),
      make_layer("nsdm", Rules.sdm_tap_enc + Rules.tap_con_enc)
    ]
    
  def well_layers(self, nx: int, ny: int, w: float, h: float):
    return super().well_layers(nx, ny, w, h) + [
      make_layer("nwell", 0.0)
    ]

class PTapContact(LICONContact):

  def __init__(self):
    super().__init__()
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
    super().__init__()
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
    super().__init__()
    self.name = "diff"
    self.description = "Diff"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    # returns an array of (name, enl) or (name, enl_x, enl_y) tuples
    return [
      make_layer("diff", Rules.diff_con_enc),
    ]

class LIContact(ContactBase):

  li_enc = (Rules.mcon_met1_enc_one, Rules.mcon_met1_enc)

  def __init__(self):
    super().__init__()
    self.name = "li"
    self.description = "LI to Met1"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("li", Rules.mcon_li_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("mcon", Rules.mcon_size, Rules.mcon_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    single_x = (nx == 1 and w < Rules.mcon_size - 1e-10)
    single_y = (ny == 1 and h < Rules.mcon_size - 1e-10)
    if single_x != single_y:
      if single_x:
        top_enc_x, top_enc_y = LIContact.li_enc
      else:
        top_enc_y, top_enc_x = LIContact.li_enc
    else:
      top_enc_x = top_enc_y = Rules.mcon_met1_enc
    # name, enclosure_x, enclosure_y
    return make_layer("met1", top_enc_x, top_enc_y)

class M1Contact(ContactBase):

  def __init__(self):
    super().__init__()
    self.name = "met1"
    self.description = "Met1 to Met2"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("met1", Rules.met1_via1_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("via1", Rules.via1_size, Rules.via1_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    return make_layer("met2", Rules.met2_via1_enc)

class M2Contact(ContactBase):

  def __init__(self):
    super().__init__()
    self.name = "met2"
    self.description = "Met2 to Met3"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("met2", Rules.met2_via2_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("via2", Rules.via2_size, Rules.via2_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    return make_layer("met3", Rules.met3_via2_enc)

class M3Contact(ContactBase):

  def __init__(self):
    super().__init__()
    self.name = "met3"
    self.description = "Met3 to Met4"

  def bot_layers(self, nx: int, ny: int, w: float, h: float):
    return [make_layer("met3", Rules.met3_via3_enc)]
    
  def via_layer(self, nx: int, ny: int, w: float, h: float):
    return ("via3", Rules.via3_size, Rules.via3_spacing)

  def top_layer(self, nx: int, ny: int, w: float, h: float):
    return make_layer("met4", Rules.met4_via3_enc)

class M4Contact(ContactBase):

  def __init__(self):
    super().__init__()
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
                 make_bot: bool = True,
                 as_ring: bool = False,
                 ring_left: bool = True,
                 ring_right: bool = True,
                 ring_top: bool = True,
                 ring_bottom: bool = True):
                
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

  if as_ring:
    lwells = via_def.well_layers(nx, ny, w, h)
  else:
    lwells = []
  
  lvia, dim, space = via_def.via_layer(nx, ny, w, h)
  lvia = Layers.by_name(lvia)
  
  arrays = []
  side_enabled = []
  
  if as_ring:
  
    w_outside = w + nx * (dim + space)
    h_outside = h + ny * (dim + space)
    
    cnx = int(math.floor(w_outside / (dim + space) + 1e-10)) // 2
    cny = int(math.floor(h_outside / (dim + space) + 1e-10)) // 2
    
    well_area = Rect(layer = None, w=w, h=h)
    align = Rect(layer = None, enclose=well_area, halo_x=0.5*(w_outside-w), halo_y=0.5*(h_outside-h))
    via_rect = Rect(layer=lvia, w=dim, h=dim, halo=space * 0.5, name="via")
    via_rect_dummy = Rect(layer=None, w=dim, h=dim, halo=space * 0.5, name="via")
    
    sides = [ [], [], [], [] ]
    side_enabled = [ ring_top, ring_bottom, ring_left, ring_right ]
    
    for arr_def in [
      (cnx, ny, "NW", 0),
      (cnx, ny, "NE", 0),
      (cnx, ny, "SW", 1),
      (cnx, ny, "SE", 1),
      (nx, cny, "SW", 2),
      (nx, cny, "NW", 2),
      (nx, cny, "SE", 3),
      (nx, cny, "NE", 3)
    ]:
      ax, ay, al, si = arr_def
      flag = side_enabled[si]
      array = Array(child=via_rect if flag else via_rect_dummy, nx=ax, ny=ay)
      sides[si].append(Linear(children=[ align, array ], align=al))
    
    for side_elements in sides:
      arrays.append(Linear(children=side_elements, align=None))
      
  else:
      
    w_via = w - top_enc_x * 2
    h_via = h - top_enc_y * 2

    via_rect = Rect(layer=lvia, w=dim, h=dim, halo=space * 0.5, name="via")
    
    arrays = [ Array(child=via_rect, nx=nx, ny=ny, w=w_via, h=h_via) ]
    side_enabled = [ True ]

  stacks = []

  for i in range(0, len(arrays)):
    
    array = arrays[i]
    stack = [array]
      
    if side_enabled[i] or not via_def.bottom_is_metal:
      for lb in lbot:
        layer, enc_x, enc_y = lb
        layer = Layers.by_name(layer)
        wr = 0.0 if as_ring else w - 2 * enc_x
        hr = 0.0 if as_ring else h - 2 * enc_y
        stack.append(Rect(layer=layer, enclose=array, enclose_feature="via", enl_x=enc_x, enl_y=enc_y, w=wr, h=hr))
  
    if side_enabled[i]:
      layer, enc_x, enc_y = ltop
      layer = Layers.by_name(layer)
      wr = 0.0 if as_ring else w - 2 * enc_x
      hr = 0.0 if as_ring else h - 2 * enc_y
      stack.append(Rect(layer=layer, enclose=array, enclose_feature="via", enl_x=enc_x, enl_y=enc_y, w=wr, h=hr, name="top"))
      
    stacks.append(Linear(children=stack, align=None))
    
  for lw in lwells:
    layer, enc_x, enc_y = lw
    layer = Layers.by_name(layer)
    stacks.append(Rect(layer=layer, enclose=well_area, enl_x=enc_x, enl_y=enc_y))
  
  return Justify(child=Linear(children=stacks, align=None), ref_point="C")

