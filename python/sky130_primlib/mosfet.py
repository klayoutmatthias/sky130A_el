
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

def make_single_mosfet(model: str, w: float, l: float, l_cont: int, r_cont: int, l_half: bool, r_half: bool, min_poly_space: float):
  
  # NOTE: Rules.poly_diff_sep for gate connection ...
  et = Rules.poly_endcap
  eb = Rules.poly_endcap

  h1 = Rules.licon_poly_sep + Rules.licon_size * 0.5
  h2 = max(Rules.poly_spacing, min_poly_space) * 0.5
  hl = max(h1 if l_cont > 0 else 0.0, h2)
  hr = max(h1 if r_cont > 0 else 0.0, h2)
  
  ex = Rules.licon_poly_sep + Rules.licon_size + Rules.diff_con_enc
  el = hl if l_half else ex
  er = hr if r_half else ex

  poly = Rect(layer=Layers.poly, w=l, h=w, enl_t=et, enl_b=eb, halo_l=hl, halo_r=hr)
  diff = Rect(layer=Layers.diff, w=l, h=w, enl_l=el, enl_r=er, halo_l=hl, halo_r=hr, name="diff")
  gate = Rect(w=l, h=w, name="gate")
  device = Linear(align="C", children=[ poly, diff, gate ])
  
  if l_cont > 0 or r_cont > 0:
  
    c = []
      
    def append_cd(cd):
      if cd > 0:
        cont = make_contact("diff", nx=1, h=w, make_bot=False)
        if cd > 1:
          cont2 = make_contact("li", nx=1, h=w, make_bot=False)
          cont = Linear(align="C", children=[ cont, cont2 ])
        c.append(PackRef(child=cont, ref_point="C"))
      
    append_cd(l_cont)
    c.append(device)
    append_cd(r_cont)
    
    device = Linear(children=c, align="HC")
    
  return device    
  

def make_mosfet(model: str, 
                w: float=1.0, l: float=0.15, 
                nf: int=1, 
                d_cont: int=1, s_cont: int=1, 
                d_wire: bool=False, s_wire: bool=False,
                min_poly_space: float=0.0):

  chain = []
  for i in range(0, nf):
    l_half = i > 0
    r_half = i < nf - 1
    l_cont, r_cont = (s_cont, d_cont) if (i % 2) == 0 else (d_cont, s_cont)
    chain.append(make_single_mosfet(model, w, l, l_cont, r_cont, l_half, r_half, min_poly_space))

  device = Linear(children=chain, align="HC")
  
  comp = [ device ]
  
  # Add well and marker layers
  for id in impl_defs[model]:
    feature, rule, layer = impl_parts[id]
    comp.append(Rect(enclose=device, enclose_feature=feature, layer=layer, enl=rule))

  # Add the PR boundary rect and align  
  comp.append(Rect(enclose=device, enclose_pack=True, layer=Layers.pr_bnd))
  
  return Justify(
    child=Linear(children=comp, align="C"), 
    ref_point="SW"
  )
