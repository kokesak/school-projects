import sys
import xml.etree.ElementTree as ET
import re
import getopt


# kotrola pro <var> pomoci regularniho vyrazu 
def check_var(var):
    if(re.fullmatch(r'^(GF|LF|TF)@([A-Z]|[a-z]|(_|-|\$|&|%|\*|\?|!))([A-Z]|[a-z]|[0-9]|(_|-|\$|&|%|\*|\?|!))*', var)):
        return True
    else:
        return False

# kotrola pro <symb> pomoci regularniho vyrazu 
def check_symb(symb):
    if(re.fullmatch(r'^(GF|LF|TF)@([A-Z]|[a-z]|(_|-|\$|&|%|\*|\?|!))([A-Z]|[a-z]|[0-9]|(_|-|\$|&|%|\*|\?|!))*', symb)):
        return "var"
    elif(re.fullmatch(r'^int@(\+|-)?([0-9])+', symb)):
        return "int"
    elif(re.fullmatch(r'^bool@(true|false)$', symb)):
        return "bool"
    #### nefunguje hashtag v string regexu !!!!
    elif(re.fullmatch(r'^string@((\\\d\d\d)|([^#| \s|\\]))*$', symb)):
        return "string"
    elif(re.fullmatch('^nil@nil$', symb)):
        return "nil"
    else:
        return False

# kotrola pro <label> pomoci regularniho vyrazu 
def check_label(label):
    if(re.fullmatch(r'^([A-Z]|[a-z]|(_|-|\$|&|%|\*|\?|!))([A-Z]|[a-z]|[0-9]|(_|-|\$|&|%|\*|\?|!))*', label)):
        return True
    else:
        return False

# ziska hodnotu z predaneho symbolu. Format symbolu je napr.: LF@var, string@retezec
def get_value_from_symb(symb):
    value_of_val1 = symb.split("@",1)
    type1 = check_symb(symb)

    if(type1 == "string"):
        value_of_val1[1] = convert_esc_to_str(value_of_val1[1])


    if(type1 == "var"):
        if(value_of_val1[0] == 'TF'):
            global TF
            if(not TF == None):
                hodnota = TF.get(value_of_val1[1]) 
                if(hodnota == None):
                    sys.stderr.write("no variable found in TF\n")
                    sys.exit(no_var_err)
                return hodnota['value']
            #print(TF)
            else:
                sys.stderr.write("no frame TF, instr MOVE \n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == 'LF'):
            global LF
            if(LF):
                hodnota = LF[0].get(value_of_val1[1])
                if(hodnota == None):
                    sys.stderr.write("no variable found in LF\n")
                    sys.exit(no_var_err)
                return hodnota['value']
            else:
                sys.stderr.write("no frame LF\n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == 'GF'):
            global GF
            hodnota = GF.get(value_of_val1[1])
            if(hodnota == None):
                    sys.stderr.write("no variable found in GF\n")
                    sys.exit(no_var_err)
            return hodnota['value']
        else:
            sys.stderr.write("some other err \n")
            sys.exit(other_err)
    else:
        return value_of_val1[1]

# ziska typ hodnoty z predaneho symbolu. Format symbolu je napr.: LF@var, string@retezec
def get_type_from_symb(symb):
    value_of_val1 = symb.split("@",1)
    type1 = check_symb(symb)
    if(type1 == "var"):
        if(value_of_val1[0] == 'TF'):
            global TF
            if(not TF == None):
                hodnota = TF.get(value_of_val1[1]) 
                if(hodnota == None):
                    sys.stderr.write("no variable found in TF\n")
                    sys.exit(no_var_err)
                return hodnota['type']
            #print(TF)
            else:
                sys.stderr.write("no frame TF, instr MOVE \n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == 'LF'):
            global LF
            if(LF):
                hodnota = LF[0].get(value_of_val1[1])
                if(hodnota == None):
                    sys.stderr.write("no variable found in LF\n")
                    sys.exit(no_var_err)
                return hodnota['type']
            else:
                sys.stderr.write("no frame LF\n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == 'GF'):
            global GF
            hodnota = GF.get(value_of_val1[1])
            if(hodnota == None):
                    sys.stderr.write("no variable found in GF\n")
                    sys.exit(no_var_err)
            return hodnota['type']
        else:
            sys.stderr.write("some other err \n")
            sys.exit(other_err)
    else:
        return value_of_val1[0]

#ulozeni hodnoty do promenne
#parametry ve tvaru: LF@var, 45, int
# vsechny parametry se predavaji jako string
def save_to_var(var, value, value_type):
    if(not check_var(var)):
        sys.stderr.write("value not compatible with symb \n")
        sys.exit(xml_structure_err)

    value_of_val1 = var.split("@",1)

    if(value_of_val1[0] == "TF"):
        global TF
        if(not TF == None):
            if(TF.get(value_of_val1[1]) == None):
                    sys.stderr.write("no variable1 found in TF \n")
                    sys.exit(no_var_err)
            TF.update({value_of_val1[1]:{"type": value_type, "value": value}})
            #print(TF)
        else:
            sys.stderr.write("no frame TF \n")
            sys.exit(no_frame_err)
    elif(value_of_val1[0] == "LF"):
        global LF
        if(LF):
            if(LF[0].get(value_of_val1[1]) == None):
                    sys.stderr.write("no variable1 found in LF \n")
                    sys.exit(no_var_err)
            LF[0].update({value_of_val1[1]:{"type": value_type, "value": value}})
        else:
            sys.stderr.write("no frame LF, instr MOVE \n")
            sys.exit(no_frame_err)
    elif(value_of_val1[0] == "GF"):
        global GF
        if(GF.get(value_of_val1[1]) == None):
                    sys.stderr.write("no variable1 found in GF\n")
                    sys.exit(no_var_err)
        GF.update({value_of_val1[1]:{"type": value_type, "value": value}})
    else:
        sys.stderr.write("some other err, instr MOVE \n")
        sys.exit(other_err)

#odstrani esc sekvence ve stringu na odpovidajici ascii znak
def convert_esc_to_str(string):
    #print(string)
    #print(bytes('test \\u0259', 'ascii').decode('unicode-escape'))
    esc = re.findall(r'\\\d\d\d', string)
    #print(esc)
    for escape_seq in esc:
	    string = string.replace(escape_seq, chr(int(escape_seq.lstrip('\\'))))
    
    return string
    
    #string = string.encode('raw_unicode_escape')
    #string = string.decode('raw_unicode_escape')
    #print(string)
    #number = hex(int('064'))
    #print(number)
    #number = number[2:]
    #number = '\\u00' + str(number)
    #print(number)



#errorove vypisy
xml_format_err = 31
xml_structure_err = 32 # zkontrolovart jestli sedi na syntax errory
no_frame_err = 55
other_err = 99
no_var_err = 54
semantic_err = 52
wrong_operators_err = 53
no_value_in_var = 56
division_by_zero = 57
running_err = 58
arguments_err = 10
file_err = 11


# Nacteni argumentu akontrola argumentu
try:
    opts, args = getopt.getopt(sys.argv[1:],"h",["help","source=", "input="])

except getopt.GetoptError:
    sys.stderr.write("Wrong arguments \n")
    sys.exit(arguments_err)

source_file = None
input_file = None

for opt, arg in opts:
    if((opt == "--help" or opt == "-h") and len(opts) == 1):
        print("Interpret .IPPcode19")
        print("--source=file || file of xml input that represent IPPcode19.")
        print("--input=file  || file from which instr READ will read IPPcode19.")
        print("If one argument file is missing stdin will be used instead.")
        print("At least one argument file must be specificed!")
        sys.exit(0)
    elif(opt == "--source"):
        source_file = arg
    elif(opt == "--input"):
        input_file = arg
    else:
        sys.stderr.write("Wrong arguments, --help cant be used with other arguments \n")
        sys.exit(arguments_err)
    
if(source_file == None and input_file == None):
    sys.stderr.write("Wrong arguments, --input or --source must be used. Use --help or -h for more info \n")
    sys.exit(arguments_err)
if(source_file == None):
    file = sys.stdin
else:
    try:
        file = open(source_file, 'r')
    except Exception:
        sys.stderr.write("Cant open source file \n")
        sys.exit(file_err)
if(input_file !=  None):
    try:
        #print(input_file)
        file_input = open(input_file, 'r')
    except Exception:
        sys.stderr.write("Cant open input file \n")
        sys.exit(file_err)



try:
    first_xml_line = file.readline()
except IOError:
    sys.stderr.write("Cant read first line from file \n")
    sys.exit(file_err)

first_xml_line = first_xml_line.strip()
if(first_xml_line not in "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" and first_xml_line not in "<?xml version=\'1.0\' encoding=\'UTF-8\'?>"):
    sys.stderr.write("missing xml header \n")
    sys.exit(xml_format_err)


#nacitani vstupniho xml formatu
string = ""
for line in file:
    string += line

try:
    program = ET.fromstring(string)

#except Exception as e:
except ET.ParseError:
        sys.stderr.write("wrong xml format \n")
        sys.exit(xml_format_err)

#slovnik instrukci       
instr = {}

#slovnik labelu
labels = {}

file.close()

#xml format se ulozi do slovnku
for instrukce in program:
    #print(instrukce.tag)
    
    if(instrukce.tag == 'instruction'):
        if('order' not in instrukce.attrib):
            sys.stderr.write("missiong order in instruction \n")
            sys.exit(xml_structure_err)
        
        instr[int(instrukce.attrib['order'])] = instrukce.attrib

        arg_counter_check = 0
        for atr in instrukce:
            arg_counter_check += 1
            arg_number = atr.tag[3:]
            if('type' not in atr.attrib):
                sys.stderr.write("missing type in xml argument \n")
                sys.exit(xml_structure_err)

            instr[int(instrukce.attrib['order'])].update({"type"+arg_number: atr.attrib['type']})
            if(atr.attrib['type'] not in 'var' and atr.attrib['type'] not in 'label' and atr.attrib['type'] not in 'type'):
                if(atr.text == None and atr.attrib['type'] in 'string'):
                    atr.text = ""
                elif(atr.text == None):
                    sys.stderr.write("missing text value in xml argument \n")
                    sys.exit(xml_structure_err)
                instr[int(instrukce.attrib['order'])].update({"val"+arg_number: atr.attrib['type'] + '@' + atr.text})
            else:
                if(atr.text == None):
                    sys.stderr.write("missing text value in xml argument \n")
                    sys.exit(xml_structure_err)
                instr[int(instrukce.attrib['order'])].update({"val"+arg_number: atr.text})
            
            #zpracovani a ulozeni labelu
            if(instrukce.attrib['opcode'].upper() == 'LABEL'):
                if(atr.attrib['type'] not in 'label'):
                    sys.stderr.write("type1 not label, instr LABEL \n")
                    sys.exit(xml_structure_err)
                if(int(arg_number) >= 2):
                    sys.stderr.write("wrong number of arguments, instr LABEL \n")
                    sys.exit(xml_structure_err)
                
                label_name = atr.text
                if(not check_label(label_name)):
                    sys.stderr.write("wrong label name, instr LABEL \n")
                    sys.exit(xml_structure_err) 
                
                if(label_name in labels.keys()):
                    sys.stderr.write("redefinition of label, instr LABEL \n")
                    sys.exit(semantic_err)
                labels.update({label_name:int(instrukce.attrib['order'])})
        #kontrola poctu argumentu (kdyz je zadan arg1 a arg3):
        tmp = 1
        while(tmp <= arg_counter_check):
            if(instr[int(instrukce.attrib['order'])].get('val'+str(tmp)) == None):
                sys.stderr.write("Arguments of instruction are not complete\n")
                sys.exit(xml_structure_err)
            tmp += 1 


#global fram
GF = {}
#temporary frame
TF = None
#local frame (reprezentovan jako seznam, ale pracuji s nim jako se zasobnikem)
LF = []

#zasobnik hodnot pro zasobnikove fce
values_stack = []

#zasobnik volani
call_stack = []

#soucasne provadena instrukce
CURRENT_INSTRUCTION_NUMBER = 1

#pocet provedenych instrukci
instructions_done = 0
instr_count = len(instr)
#print(instr)
while CURRENT_INSTRUCTION_NUMBER <= instr_count:
    current_instruction = instr.get(CURRENT_INSTRUCTION_NUMBER)
    #musi sedet cisla jedno po druhe, nesmi chybet instrukce
    try:
        name = current_instruction['opcode'].upper()
    except TypeError:
        sys.stderr.write("Wrong xml format \n")
        sys.exit(xml_structure_err)


    if(name == 'CREATEFRAME'):
        if(not len(current_instruction) == 2):
            sys.stderr.write("wrong number of arguments, instr CREATEFRAME \n")
            sys.exit(xml_structure_err)
        TF = {}
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'PUSHFRAME'):
        if(not len(current_instruction) == 2):
            sys.stderr.write("wrong number of arguments, instr PUSHFRAME \n")
            sys.exit(xml_structure_err)
        if(TF == None):
            sys.stderr.write("TF not defined, instr PUSHFRAME \n")
            sys.exit(no_frame_err)
        else:
            LF.insert(0, TF)
            TF = None
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'POPFRAME'):
        if(not len(current_instruction) == 2):
            sys.stderr.write("wrong number of arguments, instr POPFRAME \n")
            sys.exit(xml_structure_err)

        if(LF):
            TF = LF.pop(0)
        else:
            sys.stderr.write("LF not defined, instr POPFRAME\n")
            sys.exit(no_frame_err)
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'DEFVAR'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr DEFVAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr DEFVAR \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("val1 not compatible with var, instr DEFVAR \n")
            sys.exit(xml_structure_err)
        
        value_of_val1 = current_instruction['val1'].split("@",1)
        ######TODO ZJISTIT ZDA UZ NENI PROMENNA DEFINOVANA !!!! #####
        if(value_of_val1[0] == "TF"):
            if(not TF == None):
                if(not TF.get(value_of_val1[1]) == None):
                    sys.stderr.write("reusing defvar upon the same variable, instr DEFVAR \n")
                    sys.exit(semantic_err)
                TF.update({value_of_val1[1]:{"type": None, "value": None}})
                #print(TF)
            else:
                sys.stderr.write("no frame TF, instr DEFVAR \n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == 'LF'):
            if(LF):
                if(not LF[0].get(value_of_val1[1]) == None):
                    sys.stderr.write("reusing defvar upon the same variable, instr DEFVAR \n")
                    sys.exit(semantic_err)
                LF[0].update({value_of_val1[1]:{"type": None, "value": None}})
            else:
                sys.stderr.write("no frame LF, instr DEFVAR \n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == 'GF'):
            if(not GF.get(value_of_val1[1]) == None):
                    sys.stderr.write("reusing defvar upon the same variable, instr DEFVAR \n")
                    sys.exit(semantic_err)
            GF.update({value_of_val1[1]:{"type": None, "value": None}})
        else:
            sys.stderr.write("some other err, instr DEFVAR \n")
            sys.exit(other_err)
        CURRENT_INSTRUCTION_NUMBER += 1
        
    elif(name == 'MOVE'):
        if(not len(current_instruction) == 6):
            sys.stderr.write("wrong number of arguments, instr MOVE \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr MOVE \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr MOVE \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            print(type2)
            sys.stderr.write("value2 not compatible with symb, instr MOVE \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr MOVE \n")
            sys.exit(xml_structure_err)
        
        value_of_val1 = current_instruction['val1'].split("@",1)
        value_of_val2 = current_instruction['val2'].split("@",1)

        if(type2 == "string"):
            value_of_val2[1] = convert_esc_to_str(value_of_val2[1])

        if(type2 == "var"):
            if(value_of_val2[0] == 'TF'):
                if(not TF == None):
                    hodnota = TF.get(value_of_val2[1]) 
                    if(hodnota == None):
                        sys.stderr.write("no variable2 found in TF, instr MOVE \n")
                        sys.exit(no_var_err)
                    value_of_val2[1] = hodnota['value']
                    type2 = hodnota['type']
                #print(TF)
                else:
                    sys.stderr.write("no frame TF, instr MOVE \n")
                    sys.exit(no_frame_err)
            elif(value_of_val2[0] == 'LF'):
                if(LF):
                    hodnota = LF[0].get(value_of_val2[1])
                    if(hodnota == None):
                        sys.stderr.write("no variable2 found in LF, instr MOVE \n")
                        sys.exit(no_var_err)
                    value_of_val2[1] = hodnota['value']
                    type2 = hodnota['type']
                else:
                    sys.stderr.write("no frame LF, instr MOVE \n")
                    sys.exit(no_frame_err)
            elif(value_of_val2[0] == 'GF'):
                hodnota = GF.get(value_of_val2[1])
                if(hodnota == None):
                        sys.stderr.write("no variable2 found in GF, instr MOVE \n")
                        sys.exit(no_var_err)
                value_of_val2[1] = hodnota['value']
                type2 = hodnota['type']
            else:
                sys.stderr.write("some other err, instr MOVE \n")
                sys.exit(other_err)

        if(value_of_val1[0] == "TF"):
            if(not TF == None):
                if(TF.get(value_of_val1[1]) == None):
                        sys.stderr.write("no variable1 found in TF, instr MOVE \n")
                        sys.exit(no_var_err)
                TF.update({value_of_val1[1]:{"type": type2, "value": value_of_val2[1]}})
                #print(TF)
            else:
                sys.stderr.write("no frame TF, instr MOVE \n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == "LF"):
            if(LF):
                if(LF[0].get(value_of_val1[1]) == None):
                        sys.stderr.write("no variable1 found in LF, instr MOVE \n")
                        sys.exit(no_var_err)
                LF[0].update({value_of_val1[1]:{"type": type2, "value": value_of_val2[1]}})
            else:
                sys.stderr.write("no frame LF, instr MOVE \n")
                sys.exit(no_frame_err)
        elif(value_of_val1[0] == "GF"):
            if(GF.get(value_of_val1[1]) == None):
                        sys.stderr.write("no variable1 found in GF, instr MOVE \n")
                        sys.exit(no_var_err)
            GF.update({value_of_val1[1]:{"type": type2, "value": value_of_val2[1]}})
        else:
            sys.stderr.write("some other err, instr MOVE \n")
            sys.exit(other_err)
        CURRENT_INSTRUCTION_NUMBER += 1

    elif(name == 'CALL'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr CALL \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in "label"):
            sys.stderr.write("type1 not label, instr CALL \n")
            sys.exit(xml_structure_err)
        label_name = current_instruction['val1']
        if(not check_label(label_name)):
            sys.stderr.write("wrong label name, instr CALL \n")
            sys.exit(xml_structure_err)
        if(label_name not in labels.keys()):
            sys.stderr.write("no label found, instr CALL \n")
            sys.exit(semantic_err)
        call_stack.insert(0, CURRENT_INSTRUCTION_NUMBER + 1)
        CURRENT_INSTRUCTION_NUMBER = labels.get(label_name)
    
    elif(name == 'LABEL'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr LABEL \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in "label"):
            sys.stderr.write("type1 not label, instr LABEL \n")
            sys.exit(xml_structure_err)
        label_name = current_instruction['val1']
        if(not check_label(label_name)):
            sys.stderr.write("wrong label name, instr LABEL \n")
            sys.exit(xml_structure_err)
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'RETURN'):
        # TODO return nad neexitujicim labelem, ma to byt chyba???!!!!!
        if(not len(current_instruction) == 2):
            sys.stderr.write("wrong number of arguments, instr RETURN \n")
            sys.exit(xml_structure_err)
        if(call_stack):
            CURRENT_INSTRUCTION_NUMBER = call_stack.pop(0)
        else:
            sys.stderr.write("call stack is epmty, instr RETURN \n")
            sys.exit(no_value_in_var)
    
    elif(name == 'PUSHS'):        
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr PUSHS \n")
            sys.exit(xml_structure_err)
        type1 = check_symb(current_instruction['val1'])
        if(not type1):
            sys.stderr.write("value1 not compatible with symb, instr PUSHS \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in type1):
            sys.stderr.write("value1 not compatible with type1, instr PUSHS \n")
            sys.exit(xml_structure_err)

        value1 = get_value_from_symb(current_instruction['val1'])
        if(value1 == None):
            sys.stderr.write("no value in symb, instr PUSHS \n")
            sys.exit(no_value_in_var)

        type1 = get_type_from_symb(current_instruction['val1'])
        values_stack.insert(0, {"type" : type1, "value" : value1})
        CURRENT_INSTRUCTION_NUMBER += 1

    elif(name == 'POPS'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr POPS \n")
            sys.exit(xml_structure_err)
        if(values_stack):
            tmp = values_stack.pop(0)
        else:
            sys.stderr.write("STACK is empty, instr POPS \n")
            sys.exit(no_value_in_var)
        save_to_var(current_instruction['val1'], tmp['value'], tmp['type'])
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'ADD'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr ADD \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr ADD \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr ADD \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr ADD \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr ADD \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr ADD \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr ADD \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'int' or type3 not in 'int'):
            sys.stderr.write("values not int, instr ADD \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value2 == 'nil' or value3 == None or value3 == 'nil'):
            sys.stderr.write("no value in symb, instr ADD \n")
            sys.exit(no_value_in_var)
        
        save_to_var(current_instruction['val1'], str(int(value2) + int(value3)), 'int')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'SUB'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr SUB \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr SUB \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr SUB \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr SUB \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr SUB \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr SUB \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr SUB \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'int' or type3 not in 'int'):
            sys.stderr.write("values not int, instr SUB \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value2 == 'nil' or value3 == None or value3 == 'nil'):
            sys.stderr.write("no value in symb, instr SUB \n")
            sys.exit(no_value_in_var)
        
        save_to_var(current_instruction['val1'], str(int(value2) - int(value3)), 'int')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'MUL'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr MUL \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr MUL \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr MUL \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr MUL \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr MUL \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr MUL \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr MUL \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'int' or type3 not in 'int'):
            sys.stderr.write("values not int, instr MUL \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value2 == 'nil' or value3 == None or value3 == 'nil'):
            sys.stderr.write("no value in symb, instr MUL \n")
            sys.exit(no_value_in_var)
        
        save_to_var(current_instruction['val1'], str(int(value2) * int(value3)), 'int')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'IDIV'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr IDIV \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr IDIV \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr IDIV \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr IDIV \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr IDIV \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr IDIV \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr IDIV \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'int' or type3 not in 'int'):
            sys.stderr.write("values not int, instr IDIV \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value2 == 'nil' or value3 == None or value3 == 'nil'):
            sys.stderr.write("no value in symb, instr IDIV \n")
            sys.exit(no_value_in_var)
        if(value3 == '0'):
            sys.stderr.write("division by zero, instr IDIV \n")
            sys.exit(division_by_zero)
        
        save_to_var(current_instruction['val1'], str(int(value2) // int(value3)), 'int')
        CURRENT_INSTRUCTION_NUMBER += 1

    elif(name == 'AND'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr AND \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr AND \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr AND \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr AND \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr AND \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr AND \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr AND \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'bool' or type3 not in 'bool'):
            sys.stderr.write("values not bool, instr AND \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value2 == 'nil' or value3 == None or value3 == 'nil'):
            sys.stderr.write("no value in symb, instr AND \n")
            sys.exit(no_value_in_var)

        if((value2 not in 'true' and value2 not in 'false') or (value3 not in 'true' and value3 not in 'false')):
            sys.stderr.write("no bool value in operand, instr AND \n")
            sys.exit(wrong_operators_err)

        if(value2 == 'true' and value3 == 'true'):
            save_to_var(current_instruction['val1'], 'true', 'bool')
        else:
            save_to_var(current_instruction['val1'], 'false', 'bool')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'OR'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr OR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr OR \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr OR \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr OR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr OR \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr OR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr OR \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'bool' or type3 not in 'bool'):
            sys.stderr.write("values not bool, instr OR \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value2 == 'nil' or value3 == None or value3 == 'nil'):
            sys.stderr.write("no value in symb, instr OR \n")
            sys.exit(no_value_in_var)

        if((value2 not in 'true' and value2 not in 'false') or (value3 not in 'true' and value3 not in 'false')):
            sys.stderr.write("no bool value in operand, instr OR \n")
            sys.exit(wrong_operators_err)

        if(value2 == 'true' or value3 == 'true'):
            save_to_var(current_instruction['val1'], 'true', 'bool')
        else:
            save_to_var(current_instruction['val1'], 'false', 'bool')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'NOT'):
        if(not len(current_instruction) == 6):
            sys.stderr.write("wrong number of arguments, instr NOT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr NOT \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr NOT \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr NOT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr NOT \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])

        if(type2 not in 'bool'):
            sys.stderr.write("value not bool, instr NOT \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])

        if(value2 == None or value2 == 'nil'):
            sys.stderr.write("no value in symb, instr NOT \n")
            sys.exit(no_value_in_var)

        if(value2 not in 'true' and value2 not in 'false'):
            sys.stderr.write("no bool value in operand, instr NOT \n")
            sys.exit(wrong_operators_err)

        if(value2 == 'true'):
            save_to_var(current_instruction['val1'], 'false', 'bool')
        else:
            save_to_var(current_instruction['val1'], 'true', 'bool')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'EQ'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr EQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr EQ \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr EQ \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr EQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr EQ \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr EQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr EQ \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])
        #or valu2 == nil
        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr EQ \n")
            sys.exit(no_value_in_var)

        if(type2 == 'int' and type3 == 'int'):
            if(value2 == value3):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        elif(type2 == 'bool' and type3 == 'bool'):
            if(value2 == value3):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        elif(type2 == 'nil' and type3 == 'nil'):
            if(value2 == value3):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        elif(type2 == 'string' and type3 == 'string'):
            if(value2 == value3):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        elif(type2 == 'nil' or type3 == 'nil'):
            save_to_var(current_instruction['val1'], 'false', 'bool')
        else:
            sys.stderr.write("opeartors not same type, instr EQ \n")
            sys.exit(wrong_operators_err)
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'LT'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr LQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr LQ \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr LQ \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr LQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr LQ \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr LQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr LQ \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr LQ \n")
            sys.exit(no_value_in_var)
        
        if(value2 == 'nil' or value3 == 'nil'):
            sys.stderr.write("value nil cant be compared, instr LQ \n")
            sys.exit(wrong_operators_err)

        if(type2 == 'int' and type3 == 'int'):
            if(int(value2) < int(value3)):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        elif(type2 == 'bool' and type3 == 'bool'):
            if(value2 == 'false' and value3 == 'true'):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        #TODO string
        elif(type2 == 'string' and type3 == 'string'):
            if(value2 < value3):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        else:
            sys.stderr.write("opeartors not same type, instr LQ \n")
            sys.exit(wrong_operators_err)
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'GT'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr RQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr RQ \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr RQ \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr RQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr RQ \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr RQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr RQ \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr RQ \n")
            sys.exit(no_value_in_var)
        
        if(value2 == 'nil' or value3 == 'nil'):
            sys.stderr.write("value nil cant be compared, instr RQ \n")
            sys.exit(wrong_operators_err)

        if(type2 == 'int' and type3 == 'int'):
            if(int(value2) > int(value3)):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        elif(type2 == 'bool' and type3 == 'bool'):
            if(value2 == 'true' and value3 == 'false'):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        #TODO string
        elif(type2 == 'string' and type3 == 'string'):
            if(value2 > value3):
                save_to_var(current_instruction['val1'], 'true', 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        else:
            sys.stderr.write("opeartors not same type, instr RQ \n")
            sys.exit(wrong_operators_err)
        
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'INT2CHAR'):
        if(not len(current_instruction) == 6):
            sys.stderr.write("wrong number of arguments, instr INT2CHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr INT2CHAR \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr INT2CHAR \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr INT2CHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr INT2CHAR \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])

        if(type2 not in 'int'):
            sys.stderr.write("value not int, instr INT2CHAR \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        if(value2 == None):
            sys.stderr.write("no value in symb, instr INT2CHAR \n")
            sys.exit(no_value_in_var)
        try:
            value2 = chr(int(value2))
        except ValueError:
            sys.stderr.write("value is out of range, instr INT2CHAR \n")
            sys.exit(running_err)
        
        save_to_var(current_instruction['val1'], value2, 'string')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'STRI2INT'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr STR2INT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr STR2INT \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr STR2INT \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr STR2INT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr STR2INT \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr STR2INT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value3 not compatible with type3, instr STR2INT \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'string' or type3 not in 'int'):
            sys.stderr.write("no value in symb, instr STR2INT \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr STR2INT \n")
            sys.exit(no_value_in_var)
        
        try:
            znak = value2[int(value3)]
        except IndexError:
            sys.stderr.write("index error, instr STR2INT \n")
            sys.exit(running_err)
        
        znak = ord(znak)
        save_to_var(current_instruction['val1'], str(znak), 'int')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'WRITE'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr WRITE \n")
            sys.exit(xml_structure_err)

        type1 = check_symb(current_instruction['val1'])
        if(not type1):
            sys.stderr.write("value1 not compatible with symb, instr WRITE \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in type1):
            sys.stderr.write("value1 not compatible with type, instr WRITE \n")
            sys.exit(xml_structure_err)
        type1 = get_type_from_symb(current_instruction['val1'])
        value1 = get_value_from_symb(current_instruction['val1'])
        if(value1 == None):
            sys.stderr.write("no value in symb, instr WRITE \n")
            sys.exit(no_value_in_var)
        if(type1 == 'int'):
            value1 = int(value1)
        if(type1 == 'nil' and value1 == 'nil'):
            value1 = ""
        print(value1, end = '')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'CONCAT'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr CONCAT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr CONCAT \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr CONCAT \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr CONCAT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr CONCAT \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr CONCAT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value3 not compatible with type3, instr CONCAT \n")
            sys.exit(xml_structure_err)


        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])
        
        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr CONCAT \n")
            sys.exit(no_value_in_var)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'string' or type3 not in 'string'):
            sys.stderr.write("value2 not compatible with type2, instr CONCAT \n")
            sys.exit(wrong_operators_err)

        save_to_var(current_instruction['val1'], value2 + value3, 'string')

        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'STRLEN'):
        if(not len(current_instruction) == 6):
            sys.stderr.write("wrong number of arguments, instr STRLEN \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr STRLEN \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr STRLEN \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr STRLEN \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr STRLEN \n")
            sys.exit(xml_structure_err)

        value2 = get_value_from_symb(current_instruction['val2'])

        if(value2 == None):
            sys.stderr.write("no value in symb, instr STRLEN \n")
            sys.exit(no_value_in_var)

        type2 = get_type_from_symb(current_instruction['val2'])

        if(type2 not in 'string'):
            sys.stderr.write("type2 not string, instr STRLEN \n")
            sys.exit(wrong_operators_err)


        save_to_var(current_instruction['val1'], len(value2), 'int')
        CURRENT_INSTRUCTION_NUMBER += 1

    elif(name == 'GETCHAR'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr GETCHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr GETCHAR \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr GETCHAR \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr GETCHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr GETCHAR \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr GETCHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value3 not compatible with type3, instr GETCHAR \n")
            sys.exit(xml_structure_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])

        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr GETCHAR \n")
            sys.exit(no_value_in_var)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 not in 'string' or type3 not in 'int'):
            sys.stderr.write("wrong operators, instr GETCHAR \n")
            sys.exit(wrong_operators_err)
        
        
        try:
            znak = value2[int(value3)]
        except IndexError:
            sys.stderr.write("index error, instr GETCHAR \n")
            sys.exit(running_err)
        
        save_to_var(current_instruction['val1'], str(znak), 'string')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'SETCHAR'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr SETCHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr SETCHAR \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr SETCHAR \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr SETCHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr SETCHAR \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr SETCHAR \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value3 not compatible with type3, instr SETCHAR \n")
            sys.exit(xml_structure_err)
        
        type1 = get_type_from_symb(current_instruction['val1'])
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type3 not in 'string' or type2 not in 'int' or type1 not in 'string'):
            sys.stderr.write("wrong operators, instr SETCHAR \n")
            sys.exit(wrong_operators_err)
        
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])
        value1 = get_value_from_symb(current_instruction['val1'])

        if(value2 == None or value3 == None or value1 == None):
            sys.stderr.write("no value in symb, instr SETCHAR \n")
            sys.exit(no_value_in_var)
        
        try:
            #kontrola indexu
            value1[int(value2)]
            value3[0]
            
            value1 = value1[:int(value2)] + value3[0] + value1[int(value2) + 1 :]


        except IndexError:
            sys.stderr.write("index error, instr SETCHAR \n")
            sys.exit(running_err)
        
        save_to_var(current_instruction['val1'], value1, 'string')
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'TYPE'):
        if(not len(current_instruction) == 6):
            sys.stderr.write("wrong number of arguments, instr TYPE \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr TYPE \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr TYPE \n")
            sys.exit(xml_structure_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr TYPE \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr TYPE \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        if(type2 == None):
            save_to_var(current_instruction['val1'], "", 'string')
        else:
            save_to_var(current_instruction['val1'], type2, 'string')
        
        CURRENT_INSTRUCTION_NUMBER += 1

    elif(name == 'JUMP'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr JUMP \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in "label"):
            sys.stderr.write("type1 not label, instr JUMP \n")
            sys.exit(xml_structure_err)
        label_name = current_instruction['val1']
        if(not check_label(label_name)):
            sys.stderr.write("wrong label name, instr JUMP \n")
            sys.exit(xml_structure_err)
        if(label_name not in labels.keys()):
            sys.stderr.write("no label found, instr JUMP \n")
            sys.exit(semantic_err)
        
        CURRENT_INSTRUCTION_NUMBER = labels.get(label_name) # musim preskocit ten dany label instrukci
    
    elif(name == 'JUMPIFEQ'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr JUMPIFEQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in "label"):
            sys.stderr.write("type1 not label, instr JUMPIFEQ \n")
            sys.exit(xml_structure_err)
        label_name = current_instruction['val1']
        if(not check_label(label_name)):
            sys.stderr.write("wrong label name, instr JUMPIFEQ \n")
            sys.exit(xml_structure_err)
        if(label_name not in labels.keys()):
            sys.stderr.write("no label found, instr JUMPIFEQ \n")
            sys.exit(semantic_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr JUMPIFEQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr JUMPIFEQ \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr JUMPIFEQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr JUMPIFEQ \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

                 
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])
        
        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr JUMPIFEQ \n")
            sys.exit(no_value_in_var)
        
        
        if(type2 != type3):
            sys.stderr.write("type2 and type3 not the same, instr JUMPIFEQ \n")
            sys.exit(wrong_operators_err)


        
        if(value2 == value3):
            CURRENT_INSTRUCTION_NUMBER = labels.get(label_name) # musim preskocit ten dany label instrukci
        else:
            CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'JUMPIFNEQ'):
        if(not len(current_instruction) == 8):
            sys.stderr.write("wrong number of arguments, instr JUMPIFNEQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in "label"):
            sys.stderr.write("type1 not label, instr JUMPIFNEQ \n")
            sys.exit(xml_structure_err)
        label_name = current_instruction['val1']
        if(not check_label(label_name)):
            sys.stderr.write("wrong label name, instr JUMPIFNEQ \n")
            sys.exit(xml_structure_err)
        if(label_name not in labels.keys()):
            sys.stderr.write("no label found, instr JUMPIFNEQ \n")
            sys.exit(semantic_err)
        type2 = check_symb(current_instruction['val2'])
        if(not type2):
            sys.stderr.write("value2 not compatible with symb, instr JUMPIFNEQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in type2):
            sys.stderr.write("value2 not compatible with type2, instr JUMPIFNEQ \n")
            sys.exit(xml_structure_err)
        type3 = check_symb(current_instruction['val3'])
        if(not type3):
            sys.stderr.write("value3 not compatible with symb, instr JUMPIFNEQ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type3'] not in type3):
            sys.stderr.write("value2 not compatible with type2, instr JUMPIFNEQ \n")
            sys.exit(xml_structure_err)
        
        type2 = get_type_from_symb(current_instruction['val2'])
        type3 = get_type_from_symb(current_instruction['val3'])

        if(type2 != type3):
            sys.stderr.write("type2 and type3 not the same, instr JUMPIFNEQ \n")
            sys.exit(wrong_operators_err) 
        value2 = get_value_from_symb(current_instruction['val2'])
        value3 = get_value_from_symb(current_instruction['val3'])
        if(value2 == None or value3 == None):
            sys.stderr.write("no value in symb, instr JUMPIFNEQ \n")
            sys.exit(no_value_in_var)
        if(value2 != value3):
            CURRENT_INSTRUCTION_NUMBER = labels.get(label_name) # musim preskocit ten dany label instrukci
        else:
            CURRENT_INSTRUCTION_NUMBER += 1

    elif(name == 'EXIT'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr EXIT \n")
            sys.exit(xml_structure_err)

        type1 = check_symb(current_instruction['val1'])
        if(not type1):
            sys.stderr.write("value1 not compatible with symb, instr EXIT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in type1):
            sys.stderr.write("value1 not compatible with type, instr EXIT \n")
            sys.exit(xml_structure_err)
        
        value1 = get_value_from_symb(current_instruction['val1'])
        if(value1 == None):
            sys.stderr.write("no value in symb, instr EXIT \n")
            sys.exit(no_value_in_var)
        
        type1 = get_type_from_symb(current_instruction['val1'])
        if(type1 not in 'int'):
            sys.stderr.write("not int value to return, instr EXIT \n")
            sys.exit(wrong_operators_err)

        if(int(value1) < 0 or int(value1) > 49):
            sys.stderr.write("value out of range, instr EXIT \n")
            sys.exit(division_by_zero)
        else:
            sys.exit(int(value1))
    
    elif(name == 'DPRINT'):
        if(not len(current_instruction) == 4):
            sys.stderr.write("wrong number of arguments, instr DPRINT \n")
            sys.exit(xml_structure_err)

        type1 = check_symb(current_instruction['val1'])
        if(not type1):
            sys.stderr.write("value1 not compatible with symb, instr DPRINT \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in type1):
            sys.stderr.write("value1 not compatible with type, instr DPRINT \n")
            sys.exit(xml_structure_err)
        type1 = get_type_from_symb(current_instruction['val1'])

        value1 = get_value_from_symb(current_instruction['val1'])
        if(value1 == None):
            sys.stderr.write("no value in symb, instr DPRINT \n")
            sys.exit(no_value_in_var)
        sys.stderr.write(value1 + "\n")
        CURRENT_INSTRUCTION_NUMBER += 1
    
    elif(name == 'BREAK'):
        if(not len(current_instruction) == 2):
            sys.stderr.write("wrong number of arguments, instr BREAK \n")
            sys.exit(xml_structure_err)

        sys.stderr.write("Pocet provedenych instrucki vcetne tehle:"+ str(instructions_done + 1) +"\n")
        sys.stderr.write("Aktualni cislo instrukce:"+ str(CURRENT_INSTRUCTION_NUMBER) +"\n")
        
        print("Aktualni stav Global Frame:", file=sys.stderr)
        print(GF, file=sys.stderr)

        if(not TF == None):
            print("Aktualni stav Temporary Frame:", file=sys.stderr)
            print(TF, file=sys.stderr)
        else:
            sys.stderr.write("Temporary Frame not defined \n")
        
        if(LF):
            print("Aktualni stav Local Frame:", file=sys.stderr)
            print(LF, file=sys.stderr)
        else:
            sys.stderr.write("Local Frame not defined \n")
        
        CURRENT_INSTRUCTION_NUMBER += 1

    elif(name == 'READ'):

        if(not len(current_instruction) == 6):
            sys.stderr.write("wrong number of arguments, instr READ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type1'] not in 'var'):
            sys.stderr.write("type1 not var, instr READ \n")
            sys.exit(xml_structure_err)
        if(not check_var(current_instruction['val1'])):
            sys.stderr.write("value1 not compatible with var, instr READ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['type2'] not in 'type'):
            sys.stderr.write("type2 not type, instr READ \n")
            sys.exit(xml_structure_err)
        if(current_instruction['val2'] not in 'int' and current_instruction['val2'] not in 'bool' and current_instruction['val2'] not in 'string' ):
            sys.stderr.write("type2 not type, instr READ \n")
            sys.exit(xml_structure_err)
        if(input_file == None):
            read_string = input()
        else:
            #print(file_input.readline())
            read_string = file_input.readline().rstrip('\n')
            #print("NACTENA HODNOTA:: "+read_string+"\n")

        if(current_instruction['val2'] == 'int'):
            if(re.fullmatch(r'^(\+|-)?([0-9])+', read_string)):
                save_to_var(current_instruction['val1'], read_string, 'int')
            else:
                save_to_var(current_instruction['val1'], '0', 'int')
        elif(current_instruction['val2'] == 'bool'):
            read_string = read_string.lower()
            if(re.fullmatch(r'^(true|false)$', read_string)):
                save_to_var(current_instruction['val1'], read_string, 'bool')
            else:
                save_to_var(current_instruction['val1'], 'false', 'bool')
        elif(current_instruction['val2'] == 'string'):

            if(re.fullmatch(r'^((\\\d\d\d)|([^#| \s|\\]))*$', str(read_string))):
                save_to_var(current_instruction['val1'], str(read_string), 'string')
            else:
                save_to_var(current_instruction['val1'], "", 'string') 

        CURRENT_INSTRUCTION_NUMBER += 1

    else:
        sys.stderr.write("wrong instruction name \n")
        sys.exit(xml_structure_err)
    
    instructions_done += 1


#konec
if(not input_file == None):
    file_input.close()
sys.exit(0)
#print(LF)

