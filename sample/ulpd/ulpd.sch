v {xschem version=3.1.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 160 -300 160 -160 {
lab=VDD}
N 300 -160 300 -30 {
lab=GND}
N 190 -160 270 -160 {
lab=#net1}
N 160 -120 160 -60 {
lab=vn}
N 330 -160 400 -160 {
lab=vn}
N 60 -160 130 -160 {
lab=vp}
N 300 -260 300 -200 {
lab=vp}
N 90 -260 300 -260 {
lab=vp}
N 90 -260 90 -160 {
lab=vp}
N 160 -60 370 -60 {
lab=vn}
N 370 -160 370 -60 {
lab=vn}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 300 -180 3 1 {name=M2
L=0.5
W=15
nf=10
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
C {devices/vdd.sym} 160 -300 0 0 {name=l1 lab=VDD}
C {devices/gnd.sym} 300 -30 0 0 {name=l2 lab=GND}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 160 -140 3 0 {name=M1
L=0.5
W=20
nf=10
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8_lvt
spiceprefix=X
}
C {devices/iopin.sym} 400 -160 0 0 {name=p1 lab=vn}
C {devices/iopin.sym} 60 -160 0 1 {name=p2 lab=vp}
