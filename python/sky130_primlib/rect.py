
import pya as kdb
import typing

from .node import Node

class Rect(Node):

  def __init__(self, layer: kdb.LayerInfo=None, 
                     enclose: Node=None,
                     enclose_pack: bool=False,
                     enclose_feature: str="*",
                     name: str="",
                     w: float=0.0, h: float=0.0, 
                     halo: float=0.0, halo_x: float=0.0, halo_y: float=0.0, 
                     halo_l: float=0.0, halo_b: float=0.0, halo_t: float=0.0, halo_r: float=0.0, 
                     enl: float=0.0, enl_x: float=0.0, enl_y: float=0.0,
                     enl_l: float=0.0, enl_b: float=0.0, enl_t: float=0.0, enl_r: float=0.0):

    self.enclose = enclose
    self.name = name

    if enclose is not None:
      if enclose_pack:
        fb = enclose.pack_box()
      else:
        fb = enclose.feature_box(enclose_feature)
      self.w = max(w, fb.width())
      self.h = max(h, fb.height())
      self.etrans = kdb.DTrans(fb.center() - kdb.DPoint(self.w * 0.5, self.h * 0.5))
    else:
      self.w = w
      self.h = h
      self.etrans = kdb.DTrans()
      
    if enl_b is None:
      enl_b = -self.h
    if enl_t is None:
      enl_t = -self.h
      
    if enl_l is None:
      enl_l = -self.w
    if enl_r is None:
      enl_r = -self.w

    self.halo_l = halo + halo_x + halo_l
    self.halo_r = halo + halo_x + halo_r
    self.halo_b = halo + halo_y + halo_b
    self.halo_t = halo + halo_y + halo_t
    self.enl_l = enl + enl_x + enl_l
    self.enl_r = enl + enl_x + enl_r
    self.enl_b = enl + enl_y + enl_b
    self.enl_t = enl + enl_y + enl_t
    self.layer = layer
      
  def bounding_box(self) -> kdb.DBox:
    return self.etrans * kdb.DBox(-self.enl_l, -self.enl_b, self.w + self.enl_r, self.h + self.enl_t)

  def feature_box(self, feature_name: str) -> kdb.DBox:
    if feature_name == "*" or feature_name == self.name:
      return self.bounding_box()
    else:
      return kdb.DBox()

  def pack_box(self) -> kdb.DBox:
    if self.enclose:
      pb = self.enclose.pack_box()
      return kdb.DBox(pb.left - self.halo_l, pb.bottom - self.halo_b, 
                      pb.right + self.halo_r, pb.top + self.halo_t)
    else:
      return kdb.DBox(-self.halo_l, -self.halo_b, self.w + self.halo_r, self.h + self.halo_t)

  def produce(self, cell: kdb.Cell, trans: kdb.DTrans):
    if self.layer is not None:
      lindex = cell.layout().layer(self.layer)
      cell.shapes(lindex).insert(trans * self.bounding_box())
