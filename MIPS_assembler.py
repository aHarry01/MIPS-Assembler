#should be spaces between commas (ex - add $s0, $s1, $s2)
#branch target labels should be on a line by themselves (Loop:)
#and should be labelled before they are referenced in a branch instr
#currently supports add, sub, addi, or, and, slt, beq, bne, lw, sw

#converts number to twos-complement binary string with 16 bits 
def twos_complement(number):
    if number >= 0: #positive number
        return '{0:016b}'.format(number)
    else: #negative number
        number = 2**16 + number #2^N - |number|, since number < 0, becomes 2^N + number
        bin_str = '{0:b}'.format(number)
        return ('1' * (16-len(bin_str))) + bin_str

filename = input("File to assemble: ")

opcode_dict = {'add' : '000000', 'sub' : '000000', 'addi' : '001000', 'or' : '000000',
               'and' : '000000', 'slt' : '000000', 'beq' :  '000100', 'bne' : '000101',
               'lw' : '100011', 'sw' : '101011'}

func_dict = {'add' : '100000', 'sub' : '100010', 'or' : '100101', 'and' : '100100', 'slt' : '101010'}

#haven't implement jal so don't need $v0-$v1, $a0-$a3, $sp, $fp, $ra, $gp, $k0-$k1 yet
register_dict = {'$zero' : '00000', '$t0' : '01000', '$t1' : '01001', '$t2' : '01010', '$t3' : '01011', '$t4' : '01100',
                 '$t5' : '01101', '$t6' : '01110', '$t7' : '01111', '$s0' : '10000', '$s1' : '10001', '$s2' : '10010', '$s3' : '10011', '$s4' : '10100',
                 '$s5' : '10101', '$s6' : '10110', '$s7' : '10111', '$t8' : '11000', '$t9' : '11001'}

label_dict = {}

with open(filename, 'r') as f:
    lines = [line.rstrip() for line in f]
    word_address = 3072
    #convert each line to assembly
    for line in lines:
        words = line.split(" ")
        binary_str = ""
        if len(words) == 1: #only 1 word on the line => it's a label
            label_dict[words[0].rstrip(':')] = word_address #add this location to dictionary
        else:
            binary_str += opcode_dict[words[0]] #first translate the instruction to opcode
            
            if binary_str == "000000": #if it's an R-type instruction...
                binary_str += register_dict[words[2].rstrip(',')] #rs
                binary_str += register_dict[words[3].rstrip(',')] #rt
                binary_str += register_dict[words[1].rstrip(',')] #rd
                binary_str += "00000" #shamt - none of the instructions I implemented use this
                binary_str += func_dict[words[0]] #func
            elif binary_str == "000100" or binary_str == "000101": #bne or beq
                #beq rs rt Label    opcode rs rt imm
                binary_str += register_dict[words[1].rstrip(',')] #rs
                binary_str += register_dict[words[2].rstrip(',')] #rt
                offset = label_dict[words[3]]  - (word_address + 1) #calculate PC-relative offset to given label
                binary_str += twos_complement(offset) #immediate (address of label)
            else: #lw ,sw
                #lw rt, num(rs)     sw rt, num(rs)   opcode rs rt imm
                rs = words[2][len(words[2])-4 : -1]
                binary_str += register_dict[rs] #rs
                binary_str += register_dict[words[1].rstrip(',')] #rt
                offset = words[2][0:len(words[2])-5]
                binary_str += twos_complement(int(offset)) #16-bit immediate
            print(binary_str)
            word_address += 1
