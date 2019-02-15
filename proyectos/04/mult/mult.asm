// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm
// Modified: Felipe Cortés Jaramillo    

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


@R7   //i
M = 1 //Store in a new variable the counter
@R2
M = 0 //Store the first value of the mulptiplication
(LOOP)
    @R7
    D = M
    @R1 //Fetech the maximun iteration
    D = D - M  // D = i- - R1
    @END
    D;JGT   //If (i-R1)> goto END -> End the cicle
    @R0     //Fetch the base
    D = M
    @R2     //Add the value because its a multiplication
    M = M + D
    @R7
    M = M + 1 //i++
    @LOOP
    0;JMP   //Goto LOOP
(END)
    @END
    0;JMP   //Infinite Loop

