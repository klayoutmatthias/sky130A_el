
import pya as kdb

from .contact import make_contact
from .layers import Layers
from .rules import Rules
from .rect import Rect
from .array import Array
from .linear import Linear
from .pack import PackRef
from .justify import Justify

models = [
  "nfet_1v8_lvt",
  "nfet_1v8",
  "pfet_1v8_lvt",
  "pfet_1v8",
  "pfet_1v8_hvt",
]

impl_defs = {
  "nfet_1v8_lvt": [ "nsdm", "lvt" ],
  "nfet_1v8":     [ "nsdm" ],
  "pfet_1v8_lvt": [ "nwell", "psdm", "lvt" ],
  "pfet_1v8":     [ "nwell", "psdm" ],
  "pfet_1v8_hvt": [ "nwell", "psdm", "hvt" ]
}

impl_parts = {
  "nsdm": ( "diff", Rules.sdm_diff_enc, Layers.nsdm ),
  "psdm": ( "diff", Rules.sdm_diff_enc, Layers.psdm ),
  "lvt": ( "gate", Rules.lvtn_gate_enc, Layers.lvtn ),
  "hvt": ( "gate", Rules.hvtp_gate_enc, Layers.hvtp ),
  "nwell": ( "diff", Rules.nwell_diff_enc, Layers.nwell )
}

class MOSFETParam:

   w = 0.15
   l = 1.0
   l_cont = 0
   r_cont = 0
   l_half = False
   r_half = False
   min_poly_space = 0.0
   poly_ext_top = 0.0
   poly_ext_bottom = 0.0
   l_li_ext_top = 0.0
   l_li_ext_bottom = 0.0
   r_li_ext_top = 0.0
   r_li_ext_bottom = 0.0
   l_met1_ext_top = 0.0
   l_met1_ext_bottom = 0.0
   r_met1_ext_top = 0.0
   r_met1_ext_bottom = 0.0
  

def make_single_mosfet(param: MOSFETParam, drain_is_left: bool):
  
  l = param.l
  w = param.w

  et = param.poly_ext_top
  eb = param.poly_ext_bottom

  h1 = Rules.licon_poly_sep + Rules.licon_size * 0.5
  h2 = max(Rules.poly_spacing, param.min_poly_space) * 0.5
  hl = max(h1 if param.l_cont > 0 else 0.0, h2)
  hr = max(h1 if param.r_cont > 0 else 0.0, h2)
  
  ex = max(Rules.licon_poly_sep + Rules.licon_size * 0.5, param.min_poly_space * 0.5) + Rules.licon_size * 0.5 + Rules.diff_con_enc
  el = hl if param.l_half else ex
  er = hr if param.r_half else ex

  poly = Rect(layer=Layers.poly, w=l, h=w, enl_t=et, enl_b=eb, halo_l=hl, halo_r=hr, name="poly")
  diff = Rect(layer=Layers.diff, w=l, h=w, enl_l=el, enl_r=er, halo_l=hl, halo_r=hr, name="diff")
  gate = Rect(layer=None, w=l, h=w, name="gate")
  device = Linear(align="C", children=[ gate, poly, diff ])
  
  if param.l_cont > 0 or param.r_cont > 0:
  
    c = []
      
    def append_cd(cd, li_ext_top, li_ext_bottom, met1_ext_top, met1_ext_bottom, is_drain):
    
      if cd == 0:
        return
        
      cont = [make_contact("diff", nx=1, h=w, make_bot=False)]
      if li_ext_top > 0.0 or li_ext_bottom > 0.0:
        name = "li_drain" if is_drain else "li_source"
        cont.append(Rect(name=name, enclose=cont[-1], enclose_feature="top", enl_t=li_ext_top, enl_b=li_ext_bottom, layer=Layers.li))
        
      if cd > 1:
        cont.append(make_contact("li", nx=1, h=w, make_bot=False))
        if met1_ext_top > 0.0 or met1_ext_bottom > 0.0:
          name = "met1_drain" if is_drain else "met1_source"
          cont.append(Rect(name=name, enclose=cont[-1], enclose_feature="top", enl_t=met1_ext_top, enl_b=met1_ext_bottom, layer=Layers.met1))
          
      if len(cont) > 1:
        cont = Linear(align="C", children=cont)
      else:
        cont = cont[0]
        
      c.append(PackRef(child=cont, ref_point="C"))
      
    
    if not param.l_half:
      append_cd(param.l_cont, param.l_li_ext_top, param.l_li_ext_bottom, param.l_met1_ext_top, param.l_met1_ext_bottom, drain_is_left)
      
    c.append(device)
    
    append_cd(param.r_cont, param.r_li_ext_top, param.r_li_ext_bottom, param.r_met1_ext_top, param.r_met1_ext_bottom, not drain_is_left)
    
    device = Linear(children=c, align="HC")
    
  return device    
  
def swapped_if(a, b, cond):
  if cond:
    return (b, a)
  else:
    return (a, b)
    
def make_mosfet(model: str, 
                w: float=1.0, l: float=0.15, 
                nf: int=1, 
                min_poly_space: float=0.0,
                d_cont: int=1, s_cont: int=1, 
                g_wire: int=0, d_wire: int=0, s_wire: int=0,
                g_wire_width: float=0.0, 
                d_wire_width: float=0.0, s_wire_width: float=0.0,
                poly_ext_top: float=0.0, poly_ext_bottom: float=0.0,
                d_li_ext_top: float=0.0, d_li_ext_bottom: float=0.0,
                s_li_ext_top: float=0.0, s_li_ext_bottom: float=0.0,
                d_met1_ext_top: float=0.0, d_met1_ext_bottom: float=0.0,
                s_met1_ext_top: float=0.0, s_met1_ext_bottom: float=0.0
                ):

  g_wire_width      = max(g_wire_width, Rules.poly_width)

  if s_cont == 1:
    s_wire_width    = max(s_wire_width, Rules.li_width)
  if s_cont == 2:
    s_wire_width    = max(s_wire_width, Rules.met1_width)

  if d_cont == 1:
    d_wire_width    = max(d_wire_width, Rules.li_width)
  if d_cont == 2:
    d_wire_width    = max(d_wire_width, Rules.met1_width)
  
  poly_ext_top      = max(poly_ext_top,    Rules.poly_endcap if (g_wire & 2) == 0 else Rules.poly_diff_sep)
  poly_ext_bottom   = max(poly_ext_bottom, Rules.poly_endcap if (g_wire & 1) == 0 else Rules.poly_diff_sep)

  d1                = max(d_li_ext_top,    0.0 if (d_wire & 2) == 0 else Rules.li_spacing + max(0.0, s_li_ext_top))
  d2                = max(d_li_ext_bottom, 0.0 if (d_wire & 1) == 0 else Rules.li_spacing + max(0.0, s_li_ext_bottom))
  
  s1                = max(s_li_ext_top,    0.0 if (s_wire & 2) == 0 else Rules.li_spacing + max(0.0, d_li_ext_top))
  s2                = max(s_li_ext_bottom, 0.0 if (s_wire & 1) == 0 else Rules.li_spacing + max(0.0, d_li_ext_bottom))
  
  d_li_ext_top      = d1
  d_li_ext_bottom   = d2
  
  s_li_ext_top      = s1
  s_li_ext_bottom   = s2
  
  d1                = max(d_met1_ext_top,    0.0 if (d_wire & 2) == 0 else Rules.met1_spacing + max(0.0, s_met1_ext_top))
  d2                = max(d_met1_ext_bottom, 0.0 if (d_wire & 1) == 0 else Rules.met1_spacing + max(0.0, s_met1_ext_bottom))
  
  s1                = max(s_met1_ext_top,    0.0 if (s_wire & 2) == 0 else Rules.met1_spacing + max(0.0, d_met1_ext_top))
  s2                = max(s_met1_ext_bottom, 0.0 if (s_wire & 1) == 0 else Rules.met1_spacing + max(0.0, d_met1_ext_bottom))
  
  d_met1_ext_top    = d1
  d_met1_ext_bottom = d2
  
  s_met1_ext_top    = s1
  s_met1_ext_bottom = s2
  
  chain = []
  for i in range(0, nf):

    l_half = i > 0
    r_half = i < nf - 1
    
    param = MOSFETParam()
    param.w = w
    param.l = l
    param.l_cont, param.r_cont = swapped_if(s_cont, d_cont, (i % 2) != 0)
    param.l_half = l_half
    param.r_half = r_half
    param.min_poly_space = min_poly_space
    param.poly_ext_top = poly_ext_top
    param.poly_ext_bottom = poly_ext_bottom
    param.l_li_ext_top, param.r_li_ext_top = swapped_if(s_li_ext_top, d_li_ext_top, (i % 2) != 0)
    param.l_li_ext_bottom, param.r_li_ext_bottom = swapped_if(s_li_ext_bottom, d_li_ext_bottom, (i % 2) != 0)
    param.l_met1_ext_top, param.r_met1_ext_top = swapped_if(s_met1_ext_top, d_met1_ext_top, (i % 2) != 0)
    param.l_met1_ext_bottom, param.r_met1_ext_bottom = swapped_if(s_met1_ext_bottom, d_met1_ext_bottom, (i % 2) != 0)
    
    chain.append(make_single_mosfet(param, i % 2 != 0))

  device = Linear(children=chain, align="HC")
  
  comp = [ device ]
  
  # Add well and marker layers
  for id in impl_defs[model]:
    feature, rule, layer = impl_parts[id]
    comp.append(Rect(enclose=device, enclose_feature=feature, layer=layer, enl=rule))
    
  # Add gate wiring
  if (g_wire & 2) != 0:  # top
    comp.append(Rect(enclose=device, enclose_feature="poly", layer=Layers.poly, enl_b = None, enl_t = g_wire_width))
  if (g_wire & 1) != 0:  # bottom
    comp.append(Rect(enclose=device, enclose_feature="poly", layer=Layers.poly, enl_b = g_wire_width, enl_t = None))

  # Add drain wiring in LI
  if d_cont == 1:
    if (d_wire & 2) != 0:  # top
      comp.append(Rect(enclose=device, enclose_feature="li_drain", layer=Layers.li, enl_b = None, enl_t = d_wire_width))
    if (d_wire & 1) != 0:  # bottom
      comp.append(Rect(enclose=device, enclose_feature="li_drain", layer=Layers.li, enl_b = d_wire_width, enl_t = None))

  # Add drain wiring in MET1
  if d_cont == 2:
    if (d_wire & 2) != 0:  # top
      comp.append(Rect(enclose=device, enclose_feature="met1_drain", layer=Layers.met1, enl_b = None, enl_t = d_wire_width))
    if (d_wire & 1) != 0:  # bottom
      comp.append(Rect(enclose=device, enclose_feature="met1_drain", layer=Layers.met1, enl_b = d_wire_width, enl_t = None))

  # Add source wiring in LI
  if s_cont == 1:
    if (s_wire & 2) != 0:  # top
      comp.append(Rect(enclose=device, enclose_feature="li_source", layer=Layers.li, enl_b = None, enl_t = s_wire_width))
    if (s_wire & 1) != 0:  # bottom
      comp.append(Rect(enclose=device, enclose_feature="li_source", layer=Layers.li, enl_b = s_wire_width, enl_t = None))

  # Add source wiring in MET1
  if s_cont == 2:
    if (s_wire & 2) != 0:  # top
      comp.append(Rect(enclose=device, enclose_feature="met1_source", layer=Layers.met1, enl_b = None, enl_t = s_wire_width))
    if (s_wire & 1) != 0:  # bottom
      comp.append(Rect(enclose=device, enclose_feature="met1_source", layer=Layers.met1, enl_b = s_wire_width, enl_t = None))

  # Add the PR boundary rect and align  
  comp.append(Rect(enclose=device, enclose_pack=True, layer=Layers.pr_bnd))
  
  return Justify(
    child=Linear(children=comp, align="C"), 
    ref_point="SW"
  )
