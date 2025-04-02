import sys

def main():
    rgs={
        '00000': 'zero', '00001': 'ra', '00010': 'sp','00011': 'gp',
        '00100': 'tp', '00101': 't0', '00110': 't1', '00111': 't2', 
        '01000': 's0', '01001': 's1', '01010': 'a0', '01011': 'a1', 
        '01100': 'a2', '01101': 'a3', '01110': 'a4', '01111': 'a5', 
        '10000': 'a6', '10001': 'a7', '10010': 's2', '10011': 's3', 
        '10100': 's4', '10101': 's5', '10110': 's6', '10111': 's7', 
        '11000': 's8', '11001': 's9', '11010': 's10', '11011': 's11',
        '11100': 't3', '11101': 't4', '11110': 't5', '11111': 't6'
    }
    ops={
        '00000000000110011':['add','R'],
        '00001000000110011':['sub','R'],
        '01000000000110011':['slt','R'],
        '10100000000110011':['srl','R'],
        '11000000000110011':['or' ,'R'],
        '11100000000110011':['and','R'],
        '0100000011':['lw','I'],
        '0000010011':['addi','I'],
        '0001100111':['jalr','I'],
        '0100100011':['sw','S'],
        '0001100011':['beq','B'],
        '0011100011':['bne','B'],
        '1101111':['jal','J']
    }
    arr=[0]*33
    a=str(input("Enter input file name: "))
    b=str(input("Enter output file name: "))
    f=open(a,"r")
    for l in f:
        l=l.strip("\n")
        f7=l[:7]
        f3=l[17:20]
        opcd=l[25:]
        reg=f3+f7+opcd
        if reg in ops:
            x=ops[reg]
            rs1=rgs[l[12:17]]
            rs2=rgs[l[7:12]]
            rd=rgs[l[20:25]]
            print(x[0],rd,rs1,rs2)
        reg=f3+opcd
        if reg in ops:
            x=ops[reg]
            if x[1]=="I":
                imm=l[:12]
                rs1=rgs[l[12:17]]
                rd=rgs[l[20:25]]
                print(x[0],rd,rs1,int(imm,2))
            elif x[1]=="S":
                imm=l[:7]+l[20:25]
                rs2=rgs[l[7:12]]
                rs1=rgs[l[12:17]]
                print(x[0],rs2,int(imm,2),rs1)
            elif x[1]=="B":
                imm=l[0]+l[24]+l[2:7]+l[20:24]
                rs2=rgs[l[7:12]]
                rs1=rgs[l[12:17]]
                print(x[0],rs1,rs2,int(imm,2))
        if opcd in ops:
            x=ops[opcd]
            imm=l[0]+l[11:20]+l[1:10]+l[10]
            rd=l[20:25]
            print(x[0],rd,int(imm,2))
    
main()
