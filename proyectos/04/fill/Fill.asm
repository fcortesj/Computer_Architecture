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

(RESTART)
  @SCREEN    // get the first pixel position
  D = A 
  @iteratorP
  M = D      // set the first pixel

(CHECKC)
  @KBD
  D = M
  @BLACK     // when the key pressed is different to 0 paints black (D > 0)
  D;JGT
  @WHITE     // if 0 then paints white because no key is pressed (D = 0)
  D;JEQ
  @CHECKC   // else it loops to itself
  0;JMP

(BLACK)
  @Ccolor
  M = -1     // sets the color to -1 (all bits in 1) 1 -> black
  @CHANGEP
  0;JMP

(WHITE)
  @Ccolor
  M = 0      // sets the color to -1 (all bits in 1) 1 -> black
  @CHANGEP
  0;JMP

(CHANGEP)
  @Ccolor
  D = M      // Stores color in D
  @iteratorP
  A = M      // Get direction of pixel
  M = D      // Get the information of the pixel color and change it
  @iteratorP
  D = M + 1  // Add 1 to the current pixel in order to check next pixel or not
  @KBD
  D = A - D  // Check if all the pixels are ready because where ends pixels start KBD
  @iteratorP
  M = M + 1  // Add 1 to the current pixel
  @CHANGEP
  D;JGT      // If not it stays in the infinite loop
  @RESTART   
  0;JMP      // Otherwise restart the cycle
