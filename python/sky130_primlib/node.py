
import pya as kdb
import typing

class Node:

  ref_points = { 
    "C":  ( 0,  0  ),
    "E":  ( 1, 0  ),
    "NE": ( 1, 1  ),
    "SE": ( 1, -1 ),
    "W":  ( -1,  0  ),
    "NW": ( -1,  1  ),
    "SW": ( -1,  -1 ),
    "S":  ( 0,  -1 ),
    "N":  ( 0,  1  )
  }

  """
  A node object in the object tree

  The leaf object is the bottom-most element
  of the tree.

  It provides a number of query functions 
  and a way to fit itself in various ways.
  Finally, the object can implement itself
  on a cell.
  """

  def __init__(self):
    pass

  def bounding_box(self) -> kdb.DBox:
    """
    Returns the overall bounding box

    The overall bounding box defines the
    center for example.
    """
    return kdb.DBox()

  def pack_box(self) -> kdb.DBox:
    """
    Returns the packing box

    This is the box defining the pack dimensions.
    Objects of this type can be packed densely 
    using this box as the core region which must
    not overlap.
    """
    return kdb.DBox()

  def feature_box(self, feature_name: str) -> kdb.DBox:
    """
    Returns the feature box for the given feature
    
    This is the bounding box of "interesting features",
    i.e. the MOS device without the nwell patch.
    """
    return kdb.DBox()

  def ref_point(self, name) -> kdb.DPoint:
    """
    Returns a named reference point
    """
    jx, jy = Node.ref_points[name] 
    b = self.pack_box()
    return b.p1 + kdb.DVector(b.width() * (jx * 0.5 + 0.5), b.height() * (jy * 0.5 + 0.5))

  def produce(self, cell: kdb.Cell, trans: kdb.DTrans):
    pass

