def main():

    rgs = {
        'zero': '00000','ra': '00001','sp': '00010','gp': '00011',
        'tp': '00100','t0': '00101','t1': '00110','t2': '00111',
        's0': '01000','s1': '01001','a0': '01010','a1': '01011',
        'a2': '01100','a3': '01101','a4': '01110','a5': '01111',
        'a6': '10000','a7': '10001','s2': '10010','s3': '10011',
        's4': '10100','s5': '10101','s6': '10110','s7': '10111',
        's8': '11000','s9': '11001','s10': '11010','s11': '11011',
        't3': '11100','t4': '11101','t5': '11110','t6': '11111'
    }
    ops = {
        'add': ['000', '0000000'],
        'sub': ['000', '0100000'],
        'slt': ['010', '0000000'],
        'srl': ['101', '0000000'],
        'or': ['110', '0000000'],
        'and': ['111', '0000000']
    }
    
    a = input("Enter input file name: ")
    b = input("Enter output file name: ")
    
    f1 = open(a, 'r')
    f2 = open(b, 'w')
    
    num = 0
    for l in f1:
        num += 1
        l = l.strip()
        if l == "":
            continue
        if ':' in l:
            l = l.split(':',1)[1].strip()
        p = l.replace(',',' ').split()
        if len(p) == 0:
            continue
        op = p[0]
        if op not in ops:
            print("Error: Wrong operation found!", num)
            return
        if len(p) != 4:
            print("Error: Wrong number of arguments found!", num)
            return
        x, y, z = p[1], p[2], p[3]
        if x not in rgs or y not in rgs or z not in rgs:
            print("Error: Bad register found!", num)
            return
        f7, f3 = ops[op]
        r1, r2, r3 = rgs[x], rgs[y], rgs[z]
        opcd = '0110011'
        bincode = f7 + r3 + r2 + f3 + r1 + opcd
        if len(bincode) != 32:
            print("Oops 32 bits not made at line", num)
            return
        f2.write(bincode + '\n')
     
    f1.close()
    f2.close()
    print("Commands Succesfully Executed!")

main()
