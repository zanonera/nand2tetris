// Aditional Computer.hdl test case 
// File name: projects/05/ComputerMult.tst

load Computer.hdl,
output-file ComputerMult.out,
compare-to ComputerMult.cmp,
output-list time%S1.4.1 reset%B2.1.2 ARegister[0]%D1.7.1 DRegister[0]%D1.7.1 PC[]%D0.4.0 RAM16K[0]%D1.7.1 RAM16K[1]%D1.7.1 RAM16K[2]%D1.7.1;

// Load a program written in the Hack machine language.
// The program multiplies the two constants R0 and R1 and writes the result in RAM[2]. 
ROM32K load Mult.hack,
output;

// First run (at the beginning PC=0)
repeat 6 {
    tick, tock, output;
}

// Reset the PC
set reset 1,
set RAM16K[0] 25,
set RAM16K[1] 25,
tick, tock, output;


// Second run, to check that the PC was reset correctly.
set reset 0,

repeat 450 {
    tick, tock, output;
}
