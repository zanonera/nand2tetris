// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

//Clear RAM[2] before everything
	@0
	D=A
	@R2
	M=D

//IF R1 or R0 is equal to zero, goto the end
	@R0
	D=M		// D=RAM[0]
	@END
	D;JEQ	// If R0=0 goto END

	@R1
	D=M		// D=RAM[1]
	@END
	D;JEQ	// If R1=0 goto END
	
(END)
	@END
	0;JMP