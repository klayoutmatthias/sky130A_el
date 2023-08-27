
class Rules:

  diff_con_enc      = 0.060     # licon.5c enclosure of contact by diff
  tap_con_enc       = 0.120     # licon.7 enclosure of contact by tap
  npc_poly_con_enc  = 0.100     # licon.15 enclosure of poly contact by npc
  poly_con_enc      = 0.080     # licon.8a enclosure of poly contact by poly
  licon_size        = 0.170     # licon.1 poly/diff to licon contact size
  licon_spacing     = 0.190     # licon.2 poly/diff to licon contact to contact spacing
  li_licon_enc      = 0.080     # li.5 enclosure of licon by li, one of two adjacent sides
  li_licon_enc_all  = 0.050     # enclosure of licon by li, all sides (???)
  li_licon_enc_one  = 0.000     # enclosure of licon by li, one side
  licon_poly_sep    = 0.050     # licon.11a Spacing of licon of diff or tap to poly on diff
  mcon_li_enc       = 0.000     # ct.4 enclosure of contact by li
  mcon_size         = 0.170     # ct.1 li to met1 contact size
  mcon_spacing      = 0.190     # ct.2 li to met1 contact to contact spacing
  mcon_met1_enc     = 0.060     # m1.5 enclosure of contact by met1
  mcon_met1_enc_one = 0.030     # m1.4 enclosure of contact by met1, one of two adjacent sides
  via1_size         = 0.150     # via.1a met1 to met2 via1 size
  via1_spacing      = 0.170     # via.2 met1 to met2 via to via spacing
  met1_via1_enc     = 0.085     # via.5a enclosure of via1 by met1
  met2_via1_enc     = 0.085     # m2.5 enclosure of via1 by met2
  via2_size         = 0.200     # via2.1a  met2 to met3 via size
  via2_spacing      = 0.200     # via2.2 met2 to met3 via to via spacing
  met2_via2_enc     = 0.085     # via2.5 enclosure of via2 by met2
  met3_via2_enc     = 0.065     # m3.4 enclosure of via2 by met3
  via3_size         = 0.200     # via3.3 met3 to met4 via size
  via3_spacing      = 0.350     # via3.1 met3 to met4 via to via spacing
  met3_via3_enc     = 0.060     # via3.4 enclosure of via3 by met3
  met4_via3_enc     = 0.065     # m4.3 enclosure of via3 by met4
  via4_size         = 0.800     # via4.1 met4 to met5 via size
  via4_spacing      = 0.800     # via4.2 met4 to met5 via to via spacing
  met4_via4_enc     = 0.190     # via4.4 enclosure of via4 by met4
  met5_via4_enc     = 0.310     # m5.3 enclosure of via4 by met5
  
  li_width          = 0.170     # li.1
  li_spacing        = 0.170     # li.3
  met1_width        = 0.140     # m1.1
  met1_spacing      = 0.140     # m1.2
  met2_width        = 0.140     # m2.1
  met2_spacing      = 0.140     # m2.2
  met3_width        = 0.300     # m3.1
  met3_spacing      = 0.300     # m3.2
  met4_width        = 0.300     # m4.1
  met4_spacing      = 0.300     # m4.2
  met5_width        = 1.600     # m5.1
  met5_spacing      = 1.600     # m5.2

  poly_width        = 0.150     # poly.1a width of poly 
  poly_spacing      = 0.210     # poly.2 spacing of poly
  poly_diff_sep     = 0.075     # poly.4 spacing of poly on field to diff (parallel edges only)
  poly_tap_sep      = 0.055     # poly.5 spacing of poly on field to tap
  min_source        = 0.300     # poly.6 spacing of poly on diff to abutting tap (min source)
  min_drain         = 0.250     # poly.7 extension of diff beyond poly (min drain)
  poly_endcap       = 0.130     # poly.8 extension of poly beyond diffusion (endcap)
  
  diff_width        = 0.150     # difftap.1 diff or tap width
  
  sdm_diff_enc      = 0.125     # nsd.5a, psd.5a
  sdm_tap_enc       = 0.125     # nsd.5b, psd.5b
  nwell_lvtn_enc    = 0.380     # lvtn.10
  nwell_diff_enc    = 0.180     # difftap.8
  nwell_tap_enc     = 0.180     # difftap.10
  lvtn_gate_enc     = 0.180     # lvtn.4b
  hvtp_gate_enc     = 0.180     # hvtp.3
