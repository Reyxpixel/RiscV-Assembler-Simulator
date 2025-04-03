import sys

def twocomp(num):
    num=str(num)
    if num[0]=="0":
        return int(num,2)
    else:
        return ((~int(num,2)+1)&((1<<12)-1))*(-1)

def sext(num,length):
    num=int(num)
    if num>=0:
        result=format(num,f'0{length}b')
    else:
        result=format(num&((1<<length)-1),f'0{length}b')
    return result

def main():
    rgs={
        'zero': '00000','ra': '00001','sp': '00010','gp': '00011',
        'tp': '00100','t0': '00101','t1': '00110','t2': '00111',
        's0': '01000','s1': '01001','a0': '01010','a1': '01011',
        'a2': '01100','a3': '01101','a4': '01110','a5': '01111',
        'a6': '10000','a7': '10001','s2': '10010','s3': '10011',
        's4': '10100','s5': '10101','s6': '10110','s7': '10111',
        's8': '11000','s9': '11001','s10': '11010','s11': '11011',
        't3': '11100','t4': '11101','t5': '11110','t6': '11111'
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
    a=str(input("Enter input file name: "))
    b=str(input("Enter output file name: "))
    f=open(a,"r")
    arr=[0]*32
    arr[2]=380
    pc=0
    datamem=0
    out=[]
    for l in f:
        l=l.strip("\n")
        f7=l[:7]
        f3=l[17:20]
        opcd=l[25:]
        if f3+f7+opcd in ops:
            reg=f3+f7+opcd
            x=ops[reg]
            rs1=int(l[12:17],2)
            rs2=int(l[7:12],2)
            rd=int(l[20:25],2)
            instr=x[0]+" "+str(rd)+" "+str(rs1)+" "+str(rs2)
            if x[0]=="add":
                arr[rd]=arr[rs1]+arr[rs2]
            elif x[0]=="sub":
                arr[rd]=arr[rs1]-arr[rs2]
            elif x[0]=="slt":
                if twocomp(format(arr[rs1],"032b"))<twocomp(format(arr[rs2],"032b")):
                    arr[rd]=1
                else:
                    arr[rd]=0
            elif x[0]=="srl":
                arr[rd]=twocomp(format(arr[rs1],"032b"))>>twocomp(format(arr[rs2],"032b")[27:])
            elif x[0]=="or":
                arr[rd]=arr[rs1]|arr[rs2]
            elif x[0]=="and":
                arr[rd]=arr[rs1]&arr[rs2]
            else:
                print("Error")
        elif f3+opcd in ops:
            reg=f3+opcd
            x=ops[reg]
            if x[1]=="I":
                imm=l[:12]
                rs1=int(l[12:17],2)
                rd=int(l[20:25],2)
                instr=x[0]+" "+str(rd)+" "+str(rs1)+" "+str(twocomp(imm))
            elif x[1]=="S":
                imm=l[:7]+l[20:25]
                rs2=rgs[l[7:12]]
                rs1=rgs[l[12:17]]
                instr=x[0]+" "+rs2+" "+str(twocomp(imm))+" "+rs1
            elif x[1]=="B":
                imm=l[0]+l[24]+l[2:7]+l[20:24]
                rs2=rgs[l[7:12]]
                rs1=rgs[l[12:17]]
                instr=x[0]+" "+rs1+" "+rs2+" "+str(twocomp(imm))
            else:
                print("Error")
        elif opcd in ops:
            x=ops[opcd]
            imm=l[0]+l[11:20]+l[1:10]+l[10]
            rd=l[20:25]
            instr=x[0]+" "+rd+" "+str(twocomp(imm))
        else:
            print("Error")
        print(instr)
        pc+=4
        print("0b"+format(pc,"032b"),end=" ")
        for i in arr:
            print("0b"+format(i,"032b"),end=" ")
        print()
main()