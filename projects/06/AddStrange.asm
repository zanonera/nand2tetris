// This file is part of www.nand2tetris.org
   // and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
   // File name: projects/06/add/Add.asm

            // Computes R0 = 2 + 3  (R0 refers to RAM[0])

                  @2    //c1
               D=A      //c2
            @3          //c3
         D=D+A                            //c4
      @R0//c5
   M=D   //c6
   @white
(LOOP)
   @delta
(DOOP)
   @bigas
   @bilas
   @digas
@LOOP
@DOOP

