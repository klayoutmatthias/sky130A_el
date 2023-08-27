
import pya as kdb

class Layers:
  
  def by_name(name):
    return Layers.__dict__[name]
    
  nwell   = kdb.LayerInfo(64, 20)
  diff    = kdb.LayerInfo(65, 20)
  tap     = kdb.LayerInfo(65, 44)
  poly    = kdb.LayerInfo(66, 20)
  npc     = kdb.LayerInfo(95, 20)
  licon   = kdb.LayerInfo(66, 44)
  li      = kdb.LayerInfo(67, 20)
  mcon    = kdb.LayerInfo(67, 44)
  met1    = kdb.LayerInfo(68, 20)
  via1    = kdb.LayerInfo(68, 44)
  met2    = kdb.LayerInfo(69, 20)
  via2    = kdb.LayerInfo(69, 44)
  met3    = kdb.LayerInfo(70, 20)
  via3    = kdb.LayerInfo(70, 44)
  met4    = kdb.LayerInfo(71, 20)
  via4    = kdb.LayerInfo(71, 44)
  met5    = kdb.LayerInfo(72, 20)
  nsdm    = kdb.LayerInfo(93, 44)
  psdm    = kdb.LayerInfo(94, 20)
  lvtn    = kdb.LayerInfo(125, 44)
  hvtp    = kdb.LayerInfo(78, 44)
  hvi     = kdb.LayerInfo(75, 20)

  pr_bnd  = kdb.LayerInfo(235, 4)