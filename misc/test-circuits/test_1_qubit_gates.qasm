// =============

OPENQASM 2.0;
include "qelib1.inc";

// =============

qreg      q0[10];
qreg      q1[10];
creg      c0[10];
creg      c1[10];

// =============

u3(pi/2,0,pi) q0[0]; // equal to H
u(pi,0,pi)     q0[1]; // equal to X 

//==============

u2(0,pi)   q0[2]; //equal to H

//==============

rx(pi)    q0[3]; 
ry(0)     q0[4];

//==============

u1(0)     q0[5];
p(0)      q0[6];
rz(0)     q0[7];

//==============

u0(0)     q0[8];

//==============

id        q0[9];
t         q1[0];
tdg       q1[1];
s         q1[2];
sdg       q1[3];
z         q1[4];

//==============

x         q1[5];
y         q1[6];

//==============
       
h         q1[7];

//==============

sx        q1[8];
sxdg      q1[9];

//==============

barrier   q0[0];
barrier   q0[1];
barrier   q0[2];
barrier   q0[3];
barrier   q0[4];
barrier   q0[5];
barrier   q0[6];
barrier   q0[7];
barrier   q0[8];
barrier   q0[9];
barrier   q1[0];
barrier   q1[1];
barrier   q1[2];
barrier   q1[3];
barrier   q1[4];
barrier   q1[5];
barrier   q1[6];
barrier   q1[7];
barrier   q1[8];
barrier   q1[9];

//==============

measure   q0[0] -> c0[0];
measure   q0[1] -> c0[1];
measure   q0[2] -> c0[2];
measure   q0[3] -> c0[3];
measure   q0[4] -> c0[4];
measure   q0[5] -> c0[5];
measure   q0[6] -> c0[6];
measure   q0[7] -> c0[7];
measure   q0[8] -> c0[8];
measure   q0[9] -> c0[9];
measure   q1[0] -> c1[0];
measure   q1[1] -> c1[1];
measure   q1[2] -> c1[2];
measure   q1[3] -> c1[3];
measure   q1[4] -> c1[4];
measure   q1[5] -> c1[5];
measure   q1[6] -> c1[6];
measure   q1[7] -> c1[7];
measure   q1[8] -> c1[8];
measure   q1[9] -> c1[9];
