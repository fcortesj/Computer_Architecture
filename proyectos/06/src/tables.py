#In this file we storage the tables that point to instructions of asm

#Jump table
jump_table = {
    "null" : "000",
    "JGT"  : "001",
    "JEQ"  : "010",
    "JGE"  : "011",
    "JLT"  : "100",
    "JNE"  : "101",
    "JLE"  : "110",
    "JMP"  : "111"
}

#Destinations table
dest_table = {
    "null" : "000",
    "M"    : "001",
    "D"    : "010",
    "MD"   : "011",
    "A"    : "100",
    "AM"   : "101",
    "AD"   : "110",
    "AMD"   : "111"
}

#Pre Defined words table
predef_table = {
    "SP" : 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0" : 0,
    "R1" : 1,
    "R2" : 2,
    "R3" : 3,
    "R4" : 4,
    "R5" : 5,
    "R6" : 6,
    "R7" : 7,
    "R8" : 8,
    "R9" : 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD" : 24576
}

#Computation table
comp_table = {
    "0" : "101010",
    "1" : "111111",
    "-1" : "111010",
    "D" : "001100",
    "A" : "110000",
    "M" : "110000",
    "!D" : "001101",
    "!A" : "110001",
    "!M" : "110001",
    "-D" : "001111",
    "-A" : "110011",
    "-M" : "110011",
    "D+1" : "011111",
    "1+D" : "011111",
    "1+A" : "110111",
    "A+1" : "110111",
    "1+M" : "110111",
    "M+1" : "110111",
    "1-D" : "001110",
    "D-1" : "001110",
    "1-A" : "110010",
    "A-1" : "110010",
    "1-M" : "110010",
    "M-1" : "110010",
    "D+A" : "000010",
    "A+D" : "000010",
    "D+M" : "000010",
    "M+D" : "000010",
    "D-A" : "010011",
    "D-M" : "010011",
    "A-D" : "000111",
    "M-D" : "000111",
    "D&A" : "000000",
    "A&D" : "000000",
    "D&M" : "000000",
    "M&D" : "000000",
    "D|A" : "010101",
    "A|D" : "010101",
    "D|M" : "010101",
    "M|D": "010101"
}
