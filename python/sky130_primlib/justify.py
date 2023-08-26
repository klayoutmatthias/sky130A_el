
import pya as kdb
import typing

from .node import Node

class Justify(Node):

  def __init__(self, ref_point: str = "C", child: Node = None):

    """
    Aligns the node at the given reference point (the pack box counts)
    """
    self.rp = ref_point
    self.child = child

  def _trans(self) -> kdb.DTrans:
    rp = self.child.ref_point(self.rp)
    return kdb.DTrans(kdb.DPoint() - rp)

  def bounding_box(self) -> kdb.DBox:
    return self._trans() * self.child.bounding_box()

  def pack_box(self) -> kdb.DBox:
    return self._trans() * self.child.pack_box()

  def feature_box(self, feature_name: str) -> kdb.DBox:
    return self._trans() * self.child.feature_box(feature_name)

  def ref_point(self, name):
    return self._trans() * self.child.ref_point(name)

  def produce(self, cell: kdb.Cell, trans: kdb.DTrans):
    self.child.produce(cell, trans * self._trans())

