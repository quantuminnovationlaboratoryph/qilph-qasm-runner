// =============

OPENQASM 2.0;
include "qelib1.inc";

// =============

qreg q[5];
creg c[5];

// =============

     x q[0];
     x q[1];
//   x q[2];
//   x q[3];
//   x q[4];
   c4x q[0], q[1], q[2], q[3], q[4];

// =============

measure   q[0] -> c[0];
measure   q[1] -> c[1];
measure   q[2] -> c[2];
measure   q[3] -> c[3];
measure   q[4] -> c[4];
