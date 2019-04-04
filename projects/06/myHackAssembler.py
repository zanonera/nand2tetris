from itertools import dropwhile
import sys, getopt, os
import re 

#Hack language specification: symbols
hackSymbols = {
"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,
"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,
"SCREEN":16384, "KBD":24576,"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4
}

#Hack language specification: C-instruction
# dest = comp ; jmp
Cdest = {'000':'000',"M":"001","D":"010","MD":"011","A":"100","AM":"101","AD":"110","AMD":"111"}
Ccomp = {#a=0
"0":"0101010",
"1":"0111111",
"-1":"0111010",
"D":"0001100",
"A":"0110000",
"!D":"0001101",
"!A":"0110001",
"-D":"0001111",
"-A":"0110011",
"D+1":"0011111",
"A+1":"0110111",
"D-1":"0001110",
"A-1":"0110010",
"D+A":"0000010",
"D-A":"0010011",
"A-D":"0000111",
"D&A":"0000000",
"D|A":"0010101",
#a=1
"M":"1110000",
"!M":"1110001",
"-M":"1110011",
"M+1":"1110111",
"M-1":"1110010",
"D+M":"1000010",
"D-M":"1010011",
"M-D":"1000111",
"D&M":"1000000",
"D|M":"1010101"}
Cjmp = {'000':'000',"JGT":"001","JEQ":"010","JGE":"011","JLT":"100","JNE":"101","JLE":"110","JMP":"111"}

def rm_inline_comment(s):
    """ function to remove all the
        double slash inline comment
    """
    # remove all inline double slash (//) comment
    s = s.split('//')
    s = s[0].rstrip()
    s+="\n"
    return s

def rm_space(s):
    """ function to remove all the leading
        white spaces of a line
    """
    # remove all the leading whitespace
    return s.lstrip() 

def is_comment(s):
    """ function to check if a line
         starts with some character.
         Here // for comment
    """
    # return true if a line starts with //
    return s.startswith('//')

def is_space(s):
    """ function to check if a line
         is only white spaces
    """
    # return true if a line is all in whitespace
    return s.isspace() 

def is_address(s):
    """ function to check if a is a A
        instruction
    """
    # return true if a line starts with @
    return s.startswith('@') 

def is_loop(s):
    """ function to check if a is a
        label declaration (looping)
    """
    # return true if a line starts with (
    return s.startswith('(')     
    
def is_decimal(s):
    """ function to check if a line contains
        a decimal value
    """
    # return true if a line contains decimal
    return s.isnumeric() 
    
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hvi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('For help use "main.py -h"')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('Hack language assembler - Nand2Tetris Project')
         print('Uses the following syntax to assemble your code:')
         print('# main.py -i <inputfile.asm>')
         print('or')
         print('# main.py -i <inputfile.asm> -o <outputfile.hack>')
         sys.exit()
      elif opt == '-v':
         print('v0.1 - initial work')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
         #If you don't specify the output name it will use the input name and change the file format
         name=os.path.splitext(inputfile)
         outputfile=name[0]+".hack"
         print('Assembled file in:',outputfile)
      elif opt in ("-o", "--ofile"):
         # Uses the name specified in the -o argument
         outputfile = arg
      
   if outputfile:
      fileOut=open(outputfile,"w+")
   
   ##First pass loop to find and create the labels declaration in the dictionary, for the second pass loop ex. (LOOP)
   linha = 0
   if inputfile:
      with open(inputfile,'r') as fileIn:
         for curline in fileIn:
            curline = rm_space(curline)            ##remove leading white space at current line
            curline = rm_inline_comment(curline)   ##remove in line comments at current line
            if is_comment(curline):
               continue
            elif is_space(curline):
               continue   
            elif is_loop(curline):                 ##commands starting with ( (LABELS)
               curline = curline.strip()           ##remove all linespace in line
               curline = curline.strip('()')
               if curline not in hackSymbols:      ##symbols in hack language
                  hackSymbols[curline]=linha                     
            else:
               linha+=1                            ##just count actual code lines
      fileIn.close()
   else:
      print("You should specify at least a input file, like:")
      print('# main.py -i <inputfile.asm>')
   
   ##Second pass loop to decode the A instructions,C instructions, variables and labels
   varBaseAddress = 16  ##base address to start attributing to variables
   if inputfile:
      with open(inputfile,'r') as fileIn:
         for curline in fileIn:
            curline = rm_space(curline)            ##remove leading white space at current line
            curline = rm_inline_comment(curline)   ##remove in line comments at current line
            if is_comment(curline):
               continue
            elif is_space(curline):
               continue
            elif is_loop(curline):
               continue
            elif is_address(curline):              ##commands starting with @ (var, A and labels)
               curline = curline.strip('@')
               curline = curline.strip('()')
               curline = curline.strip()           ##remove all linespace in line
               if is_decimal(curline):
                  decimal=int(curline)
                  fileOut.write('0'+bin(decimal)[2:].zfill(15)+'\n')
               else:                               
                  if curline in hackSymbols:       ##symbols in hack language
                     decimal=hackSymbols[curline]
                     fileOut.write('0'+bin(decimal)[2:].zfill(15)+'\n')
                  else:                            ##variables
                     hackSymbols[curline]=varBaseAddress
                     varBaseAddress+=1
                     decimal=hackSymbols[curline]
                     fileOut.write('0'+bin(decimal)[2:].zfill(15)+'\n')
            else:
               str=curline
               if '=' in str:
                  if ';' in str:
                     str=re.split('[=;]',str)
                     dest=str[0].strip()
                     comp=str[1].strip()
                     jmp=str[2].strip()
                  else:
                     str=re.split('[=;]',str)
                     dest=str[0].strip()
                     comp=str[1].strip()
                     jmp='000'
               elif ';' in str:
                  str=re.split('[=;]',str)
                  dest='000'
                  comp=str[0].strip()
                  jmp=str[1].strip()
               curline=('111'+Ccomp[comp]+Cdest[dest]+Cjmp[jmp]+'\n')
               fileOut.write(curline)
      fileIn.close()
      fileOut.close()

   else:
      print("You should specify at least a input file, like:")
      print('# main.py -i <inputfile.asm>')
     
if __name__ == "__main__":
   main(sys.argv[1:])