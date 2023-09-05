
import pya as kdb

from .mosfet import models, make_mosfet

class MOSFETPCell(kdb.PCellDeclarationHelper):

  def __init__(self):

    super().__init__()

    choices = [ (s, s) for s in models ]
    cont_choices = [ ( "None", 0 ), ( "Up to li", 1 ), ( "Up to met1", 2 ) ]
    wire_choices = [ ( "None", 0 ), ( "Bottom", 1 ), ( "Top", 2 ), ( "Both", 3 ) ]

    self.param("_version", self.TypeInt, "Version", hidden=True, default=0)
    self.param("model", self.TypeInt, "Model", choices=choices, default=models[0])
    self.param("w",  self.TypeDouble, "Width", default=1.0, unit="µm")
    self.param("l",  self.TypeDouble, "Length", default=0.15, unit="µm")
    self.param("nf", self.TypeInt, "Number of fingers", default=1)
    self.param("min_poly_space", self.TypeDouble, "Min. Poly Space", default=0.0, unit="µm")
    self.param("source_cont", self.TypeInt, "Source Contacts", choices=cont_choices, default=1)
    self.param("drain_cont", self.TypeInt, "Drain Contacts", choices=cont_choices, default=1)
    
    self.param("gate_wire", self.TypeInt, "Gate wiring", choices=wire_choices, default=0)
    self.param("gate_wire_width", self.TypeDouble, "Min. gate wire width", default=0.0, unit="µm")
    self.param("gate_ext_bottom", self.TypeDouble, "Min. gate extension (bottom)", default=0.0, unit="µm")
    self.param("gate_ext_top", self.TypeDouble, "Min. gate extension (top)", default=0.0, unit="µm")
    
    self.param("source_wire", self.TypeInt, "Source wiring (needs source contacts)", choices=wire_choices, default=0)
    self.param("source_wire_width", self.TypeDouble, "Source wire width", default=0.0, unit="µm")
    self.param("source_ext_bottom", self.TypeDouble, "Source wire extension (bottom)", default=0.0, unit="µm")
    self.param("source_ext_top", self.TypeDouble, "Source wire extension (top)", default=0.0, unit="µm")
    
    self.param("drain_wire", self.TypeInt, "Drain wiring (needs drain contacts)", choices=wire_choices, default=0)
    self.param("drain_wire_width", self.TypeDouble, "Drain wire width", default=0.0, unit="µm")
    self.param("drain_ext_bottom", self.TypeDouble, "Drain wire extension (bottom)", default=0.0, unit="µm")
    self.param("drain_ext_top", self.TypeDouble, "Drain wire extension (top)", default=0.0, unit="µm")
    

  def coerce_param_impl(self):
    self.w = max(0.2, self.w)
    self.l = max(0.15, self.l)
    self.nf = min(10000, max(1, self.nf))

  def display_text_impl(self):
    return "MOSFET %s w:%.12g l:%.12g nf:%d" % (self.model, self.w, self.l, self.nf)

  def produce_impl(self):
  
    s_li_fac   = 1.0 if self.source_cont == 1 else 0.0
    s_met1_fac = 1.0 if self.source_cont == 2 else 0.0
    d_li_fac   = 1.0 if self.drain_cont  == 1 else 0.0
    d_met1_fac = 1.0 if self.drain_cont  == 2 else 0.0
  
    gen = make_mosfet(
            model=self.model, 
            w=self.w, l=self.l, nf=self.nf,
            s_cont=self.source_cont, d_cont=self.drain_cont,
            min_poly_space=self.min_poly_space,
            g_wire=self.gate_wire, poly_ext_top=self.gate_ext_top, poly_ext_bottom=self.gate_ext_bottom, g_wire_width=self.gate_wire_width,
            s_wire=self.source_wire, 
            s_li_ext_top=self.source_ext_top*s_li_fac, 
            s_li_ext_bottom=self.source_ext_bottom*s_li_fac,
            s_wire_width=self.source_wire_width,
            s_met1_ext_top=self.source_ext_top*s_met1_fac, 
            s_met1_ext_bottom=self.source_ext_bottom*s_met1_fac, 
            d_wire=self.drain_wire, 
            d_li_ext_top=self.drain_ext_top*d_li_fac, 
            d_li_ext_bottom=self.drain_ext_bottom*d_li_fac,
            d_wire_width=self.drain_wire_width,
            d_met1_ext_top=self.drain_ext_top*d_met1_fac, 
            d_met1_ext_bottom=self.drain_ext_bottom*d_met1_fac, 
          )
                      
    gen.produce(self.cell, kdb.DTrans())
    

