// =============

OPENQASM 2.0;
include "qelib1.inc";

// =============

qreg q[2];
creg c[2];

// =============

//   h q[0];
     h q[1];
   cu3(pi/2,pi/4,pi/8) q[0], q[1];

// =============

measure   q[0] -> c[0];
measure   q[1] -> c[1];
