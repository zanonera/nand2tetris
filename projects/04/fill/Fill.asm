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

// The (i) iterator runs trough all the lines (n) to fill the RAM either with (0) or (-1)

// clear the loop iterator var
@i
M=0

// start the var pos with the screen base address
@SCREEN
D=A
@pos
M=D

// n = the total size of the video ram (8k)
@8192
D=A
@n
M=D

(LOOP)
	@i
	D=M
	@n
	D=D-M
	@AGAIN
	D;JEQ // if i == n goto AGAIN
	// Check Keyboard
	@KBD
	D=M
	@BLACK
	D;JGT // if D > 0 n goto Black
	@WHITE
	0;JMP
	
(BLACK)
	@pos
	D=M
	@i
	A=D+M
	M=-1	// pixel in black
	@pos
	D=D+1
	@i
	M=M+1 // i = i + 1
	@LOOP
	0;JMP

(WHITE)
	@pos
	D=M
	@i
	A=D+M
	M=0		// pixel in white
	@pos
	D=D+1
	@i
	M=M+1 // i = i + 1	
	@LOOP
	0;JMP

// Reset the iterator (i) between the loops	
(AGAIN)
	@i
	M=0
	@LOOP
	0;JMP
	
// In normal conditions the sw will never reach here
(END)
	@END
	0;JMP 