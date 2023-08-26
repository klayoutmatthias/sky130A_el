
import pya as kdb

from .array import Array
from .justify import Justify
from .linear import Linear
from .rect import Rect
from .rules import Rules
from .layers import Layers


bot_layers  = [ "diff",  "tap",   "poly",  "li",   "met1",  "met2",   "met3",   "met4" ]
via_layers  = [ "licon", "licon", "licon", "mcon", "via1",  "via2",   "via3",   "via4" ]
top_layers  = [ "li",    "li",    "li",    "met1", "met2",  "met3",   "met4",   "met5" ]

licon_enc   = [ Rules.li_licon_enc_one, Rules.li_licon_enc, Rules.li_licon_enc_all ]

bot_encs    = [ Rules.diff_con_enc,   Rules.tap_con_enc,    Rules.poly_con_enc,   Rules.mcon_li_enc,    Rules.met1_via1_enc,  Rules.met2_via2_enc,  Rules.met3_via3_enc,  Rules.met4_via4_enc   ]
top_encs    = [ licon_enc,            licon_enc,            licon_enc,            Rules.mcon_met1_enc,  Rules.met2_via1_enc,  Rules.met3_via2_enc,  Rules.met4_via3_enc,  Rules.met5_via4_enc   ]
dims        = [ Rules.licon_size,     Rules.licon_size,     Rules.licon_size,     Rules.mcon_size,      Rules.via1_size,      Rules.via2_size,      Rules.via3_size,      Rules.via4_size       ]
spaces      = [ Rules.licon_spacing,  Rules.licon_spacing,  Rules.licon_spacing,  Rules.mcon_spacing,   Rules.via1_spacing,   Rules.via2_spacing,   Rules.via3_spacing,   Rules.via4_spacing    ]

def make_contact(bot_name: str = "", 
                 bot_index: int = None, 
                 nx: int = 1, ny: int = 1, 
                 w: float = 0.0, h: float = 0.0,
                 make_bot: bool = True):
                
  if bot_index is None:
    bot_index = bot_layers.index(bot_name)
    
  lbot = Layers.__dict__[bot_layers[bot_index]]
  ltop = Layers.__dict__[top_layers[bot_index]]
  lvia = Layers.__dict__[via_layers[bot_index]]

  bot_enc = bot_encs[bot_index]
  top_enc = top_encs[bot_index]
  dim     = dims[bot_index]
  space   = spaces[bot_index]
  
  if type(top_enc) is list:
    single_x = (nx == 1 and w == 0.0)
    single_y = (ny == 1 and h == 0.0)
    if single_x != single_y:
      if single_x:
        top_enc_x, top_enc_y, _ = top_enc
      else:
        top_enc_y, top_enc_x, _ = top_enc
    else:
      top_enc_x = top_enc_y = top_enc[2]
  else:
    top_enc_x = top_enc_y = top_enc
  
  w_via = w - max(bot_enc, top_enc_x) * 2
  h_via = h - max(bot_enc, top_enc_y) * 2

  via_rect      = Rect(layer = lvia, w = dim, h = dim, halo = space * 0.5)

  array         = Array(child = via_rect, nx = nx, ny = ny, w = w_via, h = h_via)
  top_met_added = Rect(layer = ltop, enclose = array, enl_x = top_enc_x, enl_y = top_enc_y, w = w, h = h)
  stack = [ array, top_met_added ]
  
  if make_bot:
    bot_met_added = Rect(layer = lbot, enclose = array, enl = bot_enc, w = w, h = h)
    stack.append(bot_met_added)
  
  return Justify(child = Linear(children = stack, align = "C"), ref_point = "C")

