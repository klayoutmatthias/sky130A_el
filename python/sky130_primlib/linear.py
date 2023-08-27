

import pya as kdb
import typing

from .node import Node

class Linear(Node):

  def __init__(self, align: str = "C", children: [Node] = []):

    """
    Arranges the children nodes in a linear way 
    
    Alignment strings are:
    * HB: left to right, bottom-aligned
    * HC: left to right, center-aligned
    * HT: left to right, top-aligned
    * VL: bottom to top, left-aligned
    * VC: bottom to top, center-aligned
    * VR: bottom to top, right-aligned
    * <other ref point>: stack at ref point
    
    If "align" is None, the children will simply be stacked
    """
    
    self.children = children
    self.trans = []
    
    if len(children) == 0:
      return
      
    if align == None:
    
      for c in children:
        self.trans.append(kdb.DTrans())
      
    else:
      
      ref_points = {
        "HB": ( "SW", "SE" ),
        "HC": ( "W", "E" ),
        "HT": ( "NW", "NE" ),
        "VL": ( "SW", "NW" ),
        "VC": ( "S", "N" ),
        "VR": ( "SE", "NE" )
      }
      
      if align in ref_points:
        rp, prev_rp = ref_points[align]
      else:
        prev_rp = rp = align
      
      prev = None
      
      for c in children:
        curr = c.ref_point(rp)
        if prev is None:
          trans = kdb.DTrans()
        else:
          trans = kdb.DTrans(prev - curr)
        self.trans.append(trans)
        prev = trans * c.ref_point(prev_rp)
      
  def bounding_box(self) -> kdb.DBox:
    box = kdb.DBox()
    for i in range(0, len(self.children)):
      box += self.trans[i] * self.children[i].bounding_box()
    return box

  def pack_box(self) -> kdb.DBox:
    box = kdb.DBox()
    for i in range(0, len(self.children)):
      box += self.trans[i] * self.children[i].pack_box()
    return box

  def feature_box(self, feature_name: str) -> kdb.DBox:
    box = kdb.DBox()
    for i in range(0, len(self.children)):
      box += self.trans[i] * self.children[i].feature_box(feature_name)
    return box

  def produce(self, cell: kdb.Cell, trans: kdb.DTrans):
    for i in range(0, len(self.children)):
      self.children[i].produce(cell, trans * self.trans[i])

