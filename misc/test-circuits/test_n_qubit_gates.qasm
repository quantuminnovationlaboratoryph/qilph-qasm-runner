// =============

OPENQASM 2.0;
include "qelib1.inc";

// =============

qreg      ctrl[4];
qreg      qbit[20];
creg      clbt[24];

// =============

x ctrl[0];
x ctrl[1];
x ctrl[2];
x ctrl[3];

id qbit[0];
id qbit[1];
id qbit[2];
id qbit[3];
id qbit[4];
id qbit[5];
id qbit[6];
id qbit[7];
id qbit[8];
id qbit[9];
id qbit[10];
id qbit[11];
id qbit[12];
id qbit[13];
id qbit[14];
id qbit[15];
id qbit[16];
id qbit[17];
id qbit[18];
id qbit[19];


// =============

barrier   ctrl[0], 
          ctrl[1], 
          ctrl[2], 
          ctrl[3],  
          qbit[0], 
          qbit[1], 
          qbit[2], 
          qbit[3],
          qbit[4], 
          qbit[5],
          qbit[6],
          qbit[7],
          qbit[8],
          qbit[9],
          qbit[10],
          qbit[11],
          qbit[12],
          qbit[13],
          qbit[14],
          qbit[15],
          qbit[16],
          qbit[17],
          qbit[18],
          qbit[19];

// =============

cx  ctrl[0], qbit[0];
cy  ctrl[0], qbit[1];
cz  ctrl[0], qbit[2];
ch  ctrl[0], qbit[3];
csx ctrl[0], qbit[4];

// =============

crx(pi) ctrl[0], qbit[5];
cry(pi) ctrl[0], qbit[6];
crz(pi) ctrl[0], qbit[7];
cp(pi)  ctrl[0], qbit[8];
cu1(pi) ctrl[0], qbit[9];
rzz(pi) ctrl[0], qbit[10];
rxx(pi) ctrl[0], qbit[11]; // weird

// =============

cu3(pi,pi,pi) ctrl[0], qbit[12];

// =============

cu(pi,pi,pi,pi) ctrl[0], qbit[13];

// =============

ccx  ctrl[0], ctrl[1], qbit[14];
rccx ctrl[0], ctrl[1], qbit[15];  //weird

// =============

c3x     ctrl[0], ctrl[1], ctrl[2], qbit[16];
c3sqrtx ctrl[0], ctrl[1], ctrl[2], qbit[17];
rc3x    ctrl[0], ctrl[1], ctrl[2], qbit[18];

// =============

c4x     ctrl[0], ctrl[1], ctrl[2], ctrl[3], qbit[19];

// =============

cswap ctrl[0], ctrl[2], ctrl[3];
swap  ctrl[0], ctrl[1];

// =============

barrier   ctrl[0], 
          ctrl[1], 
          ctrl[2], 
          ctrl[3],  
          qbit[0], 
          qbit[1], 
          qbit[2], 
          qbit[3],
          qbit[4], 
          qbit[5],
          qbit[6],
          qbit[7],
          qbit[8],
          qbit[9],
          qbit[10],
          qbit[11],
          qbit[12],
          qbit[13],
          qbit[14],
          qbit[15],
          qbit[16],
          qbit[17],
          qbit[18],
          qbit[19];


//==============

measure   ctrl[0] -> clbt[0];
measure   ctrl[1] -> clbt[1];
measure   ctrl[2] -> clbt[2];
measure   ctrl[3] -> clbt[3];

measure   qbit[0]  -> clbt[4];
measure   qbit[1]  -> clbt[5];
measure   qbit[2]  -> clbt[6];
measure   qbit[3]  -> clbt[7];
measure   qbit[4]  -> clbt[8];
measure   qbit[5]  -> clbt[9];
measure   qbit[6]  -> clbt[10];
measure   qbit[7]  -> clbt[11];
measure   qbit[8]  -> clbt[12];
measure   qbit[9]  -> clbt[13];
measure   qbit[10] -> clbt[14];
measure   qbit[11] -> clbt[15];
measure   qbit[12] -> clbt[16];
measure   qbit[13] -> clbt[17];
measure   qbit[14] -> clbt[18];
measure   qbit[15] -> clbt[19];
measure   qbit[16] -> clbt[20];
measure   qbit[17] -> clbt[21];
measure   qbit[18] -> clbt[22];
measure   qbit[19] -> clbt[23];




