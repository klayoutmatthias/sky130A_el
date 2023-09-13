
# Sky130 Elements - Teaching Layout

This package can be installed through the KLayout Package Manager.

It collects a few components from different sources that comprise a 
small physical design kit for Sky130A technology. Specifically:

* A technology called "sky130A_el" with
  * A layer properties file
  * A net tracer configuration
* DRC (not complete)
* LVS
* XSection setup
* D25 setup (3d view)
* A device library with a few components called "Sky130PrimLib"
* Some samples

DRC, LVS and D25 are made available under Tools/Sky130A.

The samples can be found in `<KLAYOUT_HOME>/salt/sky130A_el/sample`.
"KLAYOUT_HOME" is `c:\Users\Your_Account\KLayout` on Windows and
`~/.klayout` on Linux.

Currently there are some scripts and a sample layout for a 
two-transistor diode equivalent (ULPD). 
 
The latter sample includes a netlist for LVS and a testbench for
simulation with ngspice.

The script samples are intended for a layout scripting tutorial and 
show some basic techniques for scripting layout generators and
analysis tools.

