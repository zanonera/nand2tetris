// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// clear the loop iterator var
@i
M=0

// start the var pos with the screen base address
@SCREEN
D=A
@pos
M=D

// n = the total size of the video ram
@8192
D=A
@n
M=D

(LOOP)
	@i
	D=M
	@n
	D=D-M
	@END
	D;JEQ // if i == n goto STOP
	@pos
	D=M
	@i
	A=D+M
	M=-1
	@pos
	D=D+1
	@i
	M=M+1 // i = i + 1
	@LOOP
	0;JMP
	
(END)
	@END
	0;JMP 