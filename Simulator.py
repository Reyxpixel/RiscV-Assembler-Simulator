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
    mem={
        "0x00010000":0, "0x00010004":0, "0x00010008":0, "0x0001000C":0,
        "0x00010010":0, "0x00010014":0, "0x00010018":0, "0x0001001C":0,
        "0x00010020":0, "0x00010024":0, "0x00010028":0, "0x0001002C":0,
        "0x00010030":0, "0x00010034":0, "0x00010038":0, "0x0001003C":0,
        "0x00010040":0, "0x00010044":0, "0x00010048":0, "0x0001004C":0,
        "0x00010050":0, "0x00010054":0, "0x00010058":0, "0x0001005C":0,
        "0x00010060":0, "0x00010064":0, "0x00010068":0, "0x0001006C":0,
        "0x00010070":0, "0x00010074":0, "0x00010078":0, "0x0001007C":0
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
    f1=open(a,"r")
    f2=open(b,"w")
    arr=[0]*32
    arr[2]=380
    pc=0
    datamem=0
    out=[]
    for l in f1:
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
                if x[0]=="lw":
                    arr[rd]=sext(mem[format(int((arr[rs1],"032b")+sext(imm,32),2),"08X")],32)
                elif x[0]=="addi":
                    arr[rd]=arr[rs1]+int(imm,2)
                elif x[0]=="jalr":
                    arr[rd]=pc+4
                    pc=arr[6]+int(imm,2)
                else:
                    print("Error")
            elif x[1]=="S":
                imm=l[:7]+l[20:25]
                rs2=int([l[7:12]],2)
                rs1=int([l[12:17]],2)
                instr=x[0]+" "+str(rs2)+" "+str(twocomp(imm))+" "+str(rs1)
                if x[0]=="sw":
                    mem[format(int(format(arr[rs1],"032b")+sext(imm,32),2),"08X")]=rs2
                else:
                    print("Error")
            elif x[1]=="B":
                imm=l[0]+l[24]+l[2:7]+l[20:24]
                rs2=int(l[7:12],2)
                rs1=int(l[12:17],2)
                instr=x[0]+" "+str(rs1)+" "+str(rs2)+" "+str(twocomp(imm))
                if x[0]=="beq":
                    if rs1==rs2:
                        pc+=int(sext(imm+"0",32),2)
                elif x[0]=="bne":
                    if rs1!=rs2:
                        pc+=int(sext(imm+"0",32),2)
                else:
                    print("Error")
            else:
                print("Error")
        elif opcd in ops:
            x=ops[opcd]
            imm=l[0]+l[11:20]+l[1:10]+l[10]
            rd=int(l[20:25],2)
            instr=x[0]+" "+str(rd)+" "+str(twocomp(imm))
            if x[0]=="jal":
                rd=pc+4
                pc+=int(sext(imm+"0",32),2)
            else:
                print("Error")
        else:
            print("Error")
        f2.write(instr)
        f2.write("\n")
        pc+=4
        f2.write("0b"+format(pc,"032b")+" ")
        for i in arr:
            f2.write("0b"+format(i,"032b")+" ")
        f2.write("\n")
main()
