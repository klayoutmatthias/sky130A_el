
import pya as kdb
import typing

class Delegate:

  """
  A generic delegate

  This class can be used as a base class for 
  other classes having a single child node.
  """

  def __init__(self, child):
    self.child = child

  def bounding_box(self) -> kdb.DBox:
    return self.child.bounding_box()

  def pack_box(self) -> kdb.DBox:
    return self.child.pack_box()

  def feature_box(self) -> kdb.DBox:
    return self.child.feature_box()

  def ref_point(self, name) -> kdb.DBox:
    return self.child.ref_point(name)

  def produce(self, cell: kdb.Cell, trans: kdb.DTrans):
    return self.child.produce(cell, trans)
