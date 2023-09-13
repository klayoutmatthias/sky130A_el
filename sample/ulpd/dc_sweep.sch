v {xschem version=3.1.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 420 -230 440 -230 {
lab=vin}
N 440 -120 440 -110 {
lab=vin}
N 440 -50 440 -30 {
lab=GND}
N 340 -230 360 -230 {
lab=vdio}
N 340 -230 340 -220 {
lab=vdio}
N 320 -220 340 -220 {
lab=vdio}
N 320 -200 340 -200 {
lab=vbias}
N 440 -230 460 -230 {
lab=vin}
N 440 -230 440 -120 {
lab=vin}
N 340 -200 340 -110 {
lab=vbias}
N 340 -50 340 -30 {
lab=GND}
N 340 -130 610 -130 {
lab=vbias}
N 610 -150 610 -130 {
lab=vbias}
N 560 -180 570 -180 {
lab=vdio_nfet}
N 520 -230 610 -230 {
lab=vdio_nfet}
N 610 -230 610 -210 {
lab=vdio_nfet}
N 560 -230 560 -180 {
lab=vdio_nfet}
N 180 -50 180 -30 {
lab=GND}
N 180 -130 180 -110 {
lab=VDD}
N 610 -180 650 -180 {
lab=GND}
N 650 -180 650 -130 {
lab=GND}
C {/home/matthias/versuche/ulpd/ulpd.sym} 170 -210 0 0 {name=x1}
C {devices/vsource.sym} 440 -80 0 0 {name=vin value=1V}
C {devices/gnd.sym} 440 -30 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 340 -30 0 0 {name=l2 lab=GND}
C {devices/res.sym} 390 -230 1 0 {name=R1
value=10k
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 340 -230 1 0 {name=l3 lab=vdio}
C {devices/code.sym} 40 -400 0 0 {name=NGSPICE_DC

only_toplevel=false

value="
.param mc_mm_switch=0
.lib /home/matthias/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.temp 100

.control
dc vin 0.01 2.0 0.01
plot 
+ abs(v(vin)-v(vdio))/1e4+1e-15 vs v(vdio)-v(vbias)
+ abs(v(vin)-v(vdio_nfet))/1e4+1e-15 vs v(vdio_nfet)-(vbias) ylog
.endc
" }
C {devices/vsource.sym} 340 -80 0 0 {name=vbias value=0.8V}
C {devices/res.sym} 490 -230 3 1 {name=R2
value=10k
footprint=1206
device=resistor
m=1}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 590 -180 0 0 {name=M1
L=0.5
W=10
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_pin.sym} 560 -230 1 0 {name=l4 lab=vdio_nfet}
C {devices/lab_pin.sym} 440 -230 1 0 {name=l5 lab=vin}
C {devices/vsource.sym} 180 -80 0 0 {name=vdd value=1.8V}
C {devices/gnd.sym} 180 -30 0 0 {name=l6 lab=GND}
C {devices/vdd.sym} 180 -130 0 0 {name=l7 lab=VDD}
C {devices/lab_pin.sym} 480 -130 1 0 {name=l8 lab=vbias}
C {devices/gnd.sym} 650 -130 0 0 {name=l9 lab=GND}
