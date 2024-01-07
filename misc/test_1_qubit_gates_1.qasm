// =============

OPENQASM 2.0;
include "qelib1.inc";

// =============

qreg q[20];
creg c[20];

// =============

u3(0,0,0) q[0];
u(0,0,0)  q[1];

//==============

u2(0,0)   q[2];

//==============

rx(pi)    q[3]; 
ry(0)     q[4];

//==============

u1(0)     q[5];
p(0)      q[6];
rz(0)     q[7];

//==============

u0(0)     q[8];

//==============

id        q[9];
t        q[10];
tdg      q[11];
s        q[12];
sdg      q[13];
z        q[14];

//==============

x        q[15];
y        q[16];

//==============
       
h        q[17];

//==============

sx       q[18];
sxdg     q[19];

//==============

barrier  q[0];
barrier  q[1];
barrier  q[2];
barrier  q[3];
barrier  q[4];
barrier  q[5];
barrier  q[6];
barrier  q[7];
barrier  q[8];
barrier  q[9];
barrier  q[10];
barrier  q[11];
barrier  q[12];
barrier  q[13];
barrier  q[14];
barrier  q[15];
barrier  q[16];
barrier  q[17];
barrier  q[18];
barrier  q[19];

//==============

measure  q[0]  -> c[0];
measure  q[1]  -> c[1];
measure  q[2]  -> c[2];
measure  q[3]  -> c[3];
measure  q[4]  -> c[4];
measure  q[5]  -> c[5];
measure  q[6]  -> c[6];
measure  q[7]  -> c[7];
measure  q[8]  -> c[8];
measure  q[9]  -> c[9];
measure  q[10] -> c[10];
measure  q[11] -> c[11];
measure  q[12] -> c[12];
measure  q[13] -> c[13];
measure  q[14] -> c[14];
measure  q[15] -> c[15];
measure  q[16] -> c[16];
measure  q[17] -> c[17];
measure  q[18] -> c[18];
measure  q[19] -> c[19];
