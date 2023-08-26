
import pya as kdb
import typing

from .delegate import Delegate
from .node import Node

class PackBBox(Delegate):

  def __init__(self, child: Node):
    super().__init__(child)

  def pack_box(self):
    return self.child.bounding_box()

class PackFBox(Delegate):

  def __init__(self, child: Node, feature_name: str="*"):
    super().__init__(child)
    self.feature_name = feature_name

  def pack_box(self):
    return self.child.feature_box(self.feature_name)

class PackRef(Delegate):

  def __init__(self, child: Node, ref_point: str="C"):
    super().__init__(child)
    self.rp = ref_point

  def pack_box(self):
    rp = self.child.ref_point(self.rp)
    return kdb.DBox(rp, rp)

