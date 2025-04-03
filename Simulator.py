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

    stackmem={
        "0x00000100":0, "0x00000104":0, "0x00000108":0, "0x0000010C":0,
        "0x00000110":0, "0x00000114":0, "0x00000118":0, "0x0000011C":0,
        "0x00000120":0, "0x00000124":0, "0x00000128":0, "0x0000012C":0,
        "0x00000130":0, "0x00000134":0, "0x00000138":0, "0x0000013C":0,
        "0x00000140":0, "0x00000144":0, "0x00000148":0, "0x0000014C":0,
        "0x00000150":0, "0x00000154":0, "0x00000158":0, "0x0000015C":0,
        "0x00000160":0, "0x00000164":0, "0x00000168":0, "0x0000016C":0,
        "0x00000170":0, "0x00000174":0, "0x00000178":0, "0x0000017C":0
    }

    datamem={
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
        '1101111':['jal','J'],
        '00000000000000000000000000000000':['rst','bonus'],
        '11111111111111111111111111111111':['halt','bonus'],
    }

    a=sys.argv[1]
    b=sys.argv[2]
    f1=open(a,"r")
    f2=open(b,"w")
    arr=[0]*32
    arr[2]=380
    pc=0
    lines={}
    for l in f1:
        l=l.strip("\n")
        lines[pc]=l
        pc+=4
    pc=0
    stop=False
    error=False

    while not stop:
        l=lines[pc]
        f7=l[:7]
        f3=l[17:20]
        opcd=l[25:]

        if f3+f7+opcd in ops:
            reg=f3+f7+opcd
            x=ops[reg]
            rs1=int(l[12:17],2)
            rs2=int(l[7:12],2)
            rd=int(l[20:25],2)
            if x[0]=="add":
                arr[rd]=arr[rs1]+arr[rs2]
            elif x[0]=="sub":
                arr[rd]=arr[rs1]-arr[rs2]
            elif x[0]=="slt":
                if twocomp(sext(arr[rs1],32))<twocomp(sext(arr[rs2],32)):
                    arr[rd]=1
                else:
                    arr[rd]=0
            elif x[0]=="srl":
                arr[rd]=twocomp(sext(arr[rs1],32))>>twocomp(sext(arr[rs2],32)[27:])
            elif x[0]=="or":
                arr[rd]=arr[rs1]|arr[rs2]
            elif x[0]=="and":
                arr[rd]=arr[rs1]&arr[rs2]
            else:
                print("Error")
                error=True
                return

        elif f3+opcd in ops:
            reg=f3+opcd
            x=ops[reg]
            if x[1]=="I":
                imm=l[:12]
                rs1=int(l[12:17],2)
                rd=int(l[20:25],2)
                if x[0]=="lw":
                    if (arr[rs1]+int(imm,2))>380:
                        arr[rd]=datamem["0x"+format(arr[rs1]+int(imm,2),"08X")]
                    else:
                        arr[rd]=stackmem["0x"+format(arr[rs1]+int(imm,2),"08X")]
                elif x[0]=="addi":
                    arr[rd]=arr[rs1]+twocomp(imm)
                elif x[0]=="jalr":
                    arr[rd]=pc+4
                    arr[0]=0
                    pc=arr[rs1]+int(imm,2)
                    pc-=4
                else:
                    print("Error")
                    error=True
                    return

            elif x[1]=="S":
                imm=l[:7]+l[20:25]
                rs2=int(l[7:12],2)
                rs1=int(l[12:17],2)
                if x[0]=="sw":
                    if (arr[rs1]+int(imm,2))>380:
                        datamem["0x"+format(arr[rs1]+int(imm,2),"08X")]=arr[rs2]
                    else:
                        stackmem["0x"+format(arr[rs1]+int(imm,2),"08X")]=arr[rs2]
                else:
                    print("Error")
                    error=True
                    return

            elif x[1]=="B":
                imm=l[0]+l[24]+l[1:7]+l[20:24]+"0"
                rs2=int(l[7:12],2)
                rs1=int(l[12:17],2)
                if x[0]=="beq":
                    if arr[rs1]==arr[rs2]:
                        pc+=twocomp(imm)
                        pc-=4
                elif x[0]=="bne":
                    if arr[rs1]!=arr[rs2]:
                        pc+=twocomp(imm)
                        pc-=4
                else:
                    print("Error")
                    error=True
                    return
            else:
                print("Error")
                error=True
                return

        elif opcd in ops:
            x=ops[opcd]
            imm=l[0]+l[11:20]+l[1:10]+l[10]
            rd=int(l[20:25],2)
            if x[0]=="jal":
                arr[rd]=pc+4
                pc+=int(imm+"0",2)
                pc-=4
            else:
                print("Error")
                error=True
                return

        elif l in ops:
            x=ops[l]
            if x[0]=="rst":
                arr=[0]*32
                arr[2]=380
            elif x[0]=="halt":
                pc-=4
                stop=True
        else:
            print("Error")
            error=True
            return

        pc+=4
        arr[0]=0
        if l=="00000000000000000000000001100011":
            stop=True
        if error:
            return
        f2.write("0b"+sext(pc,32)+" ")
        for i in arr:
            f2.write("0b"+sext(i,32)+" ")
        f2.write("\n")
    if error:
        return
    for i in datamem:
        f2.write(i+":0b"+sext(datamem[i],32)+"\n")
        
main()
