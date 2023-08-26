
import pya as kdb
import typing

from .delegate import Delegate
from .node import Node

class PackBBox(Delegate):

  def __init__(self, child: Node):
    super().__init__(child)

  def pack_box(self):
    return self.child.bounding_box()

