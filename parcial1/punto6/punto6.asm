	(CHECK)
	@KBD
	D=M
	@letter
	M=D
	@128
	D=D-A
	@CONTINUE
	D;JNE
	@CHECK
	0;JMP
	(CONTINUE)
	@R0
	D=M
	@170
	D=DxA
	@SCREEN
	M=D
	(END)
	@END
	0;JMP
	
	
	
	
	
