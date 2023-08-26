
import pya as kdb
import typing
import math

from .node import Node

class Array(Node):

  def __init__(self, nx: int=1, ny: int=1, w: float=None, h: float=None, child: Node=None, array_feature: str="*"):

    """
    Defines a densely packed array of nx columns and ny rows of child
    """

    self.child = child
    fb = self.child.feature_box(array_feature)
    pb = self.child.pack_box()

    if w is not None:
      nx = max(nx, int(math.floor((w - fb.width()) / pb.width() + 1e-10)) + 1)
    else:
      nx = nx
    self.nx = max(1, nx)

    if h is not None:
      ny = max(ny, int(math.floor((h - fb.height()) / pb.height() + 1e-10)) + 1)
    else:
      ny = ny
    self.ny = max(1, ny)

  def _pitches(self) -> (float, float):
    pb = self.child.pack_box()
    return ( pb.width(), pb.height() )

  def bounding_box(self) -> kdb.DBox:
    px, py = self._pitches()
    box = self.child.bounding_box()
    return box + box.moved(px * (self.nx - 1), py * (self.ny - 1))

  def pack_box(self) -> kdb.DBox:
    px, py = self._pitches()
    box = self.child.pack_box()
    return box + box.moved(px * (self.nx - 1), py * (self.ny - 1))

  def feature_box(self, feature_name) -> kdb.DBox:
    px, py = self._pitches()
    box = self.child.feature_box(feature_name)
    return box + box.moved(px * (self.nx - 1), py * (self.ny - 1))

  def produce(self, cell: kdb.Cell, trans: kdb.DTrans):
    px, py = self._pitches()
    for ix in range(0, self.nx):
      for iy in range(0, self.ny):
        self.child.produce(cell, trans * kdb.DTrans(kdb.DVector(ix * px, iy * py)))

