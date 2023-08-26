
import pya as kdb
import typing

from .node import Node

class Rect(Node):

  def __init__(self, layer: kdb.LayerInfo = None, 
                     enclose: Node = None, 
                     w: float = 1.0, h: float = 1.0, 
                     halo: float = 0.0, halo_x: float = 0.0, halo_y: float = 0.0,
                     enl: float = 0.0, enl_x: float = 0.0, enl_y: float = 0.0):

    self.enclose = enclose

    self.halo_x = halo + halo_x
    self.halo_y = halo + halo_y
    self.enl_x = enl + enl_x
    self.enl_y = enl + enl_y
    self.layer = layer

    if enclose is not None:
      fb = enclose.feature_box()
      self.w = max(w - 2 * self.enl_x, fb.width())
      self.h = max(h - 2 * self.enl_y, fb.height())
      self.etrans = kdb.DTrans(fb.center() - kdb.DPoint(self.w * 0.5, self.h * 0.5))
    else:
      self.w = w
      self.h = h
      self.etrans = kdb.DTrans()

  def bounding_box(self) -> kdb.DBox:
    if self.enclose:
      return self.enclose.bounding_box()
    else:
      return kdb.DBox(0, 0, self.w, self.h)

  def feature_box(self) -> kdb.DBox:
    if self.enclose:
      return self.enclose.feature_box()
    else:
      return kdb.DBox(0, 0, self.w, self.h)

  def pack_box(self) -> kdb.DBox:
    if self.enclose:
      return self.enclose.pack_box().enlarged(self.halo_x, self.halo_y)
    else:
      return kdb.DBox(-self.halo_x, -self.halo_y, self.w + self.halo_x, self.h + self.halo_y)

  def produce(self, cell: kdb.Cell, trans: kdb.DTrans):
    lindex = cell.layout().layer(self.layer)
    cell.shapes(lindex).insert(trans * self.etrans * kdb.DBox(0, 0, self.w, self.h).enlarged(self.enl_x, self.enl_y))
    if self.enclose:
      self.enclose.produce(cell, trans)

