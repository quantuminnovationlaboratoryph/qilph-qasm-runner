// =============

OPENQASM 2.0;
include "qelib1.inc";

// =============

qreg q[1];
creg c[1];

// =============

   u2(pi/4, -pi/2) q[0];

// =============

measure   q[0] -> c[0];
